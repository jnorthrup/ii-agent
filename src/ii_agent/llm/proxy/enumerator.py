"""Model enumeration utilities for discovering available models from providers."""

import asyncio
from typing import Dict, List, Optional, Any
import logging

import httpx

from .types import (
    RemoteModelInfo,
    ProviderProxyConfig,
    APIFormat,
)

logger = logging.getLogger(__name__)


class ModelEnumerator:
    """Enumerates available models from provider APIs."""

    def __init__(self, proxy_config: Optional[ProviderProxyConfig] = None):
        """Initialize the model enumerator.

        Args:
            proxy_config: Optional proxy configuration for requests.
        """
        self.proxy_config = proxy_config

    async def enumerate(
        self,
        base_url: str,
        api_key: str,
        api_format: APIFormat = APIFormat.OPENAI_CHAT,
        force_refresh: bool = False,
    ) -> List[RemoteModelInfo]:
        """Enumerate models from a provider endpoint.

        Args:
            base_url: The base URL for the API.
            api_key: The API key.
            api_format: The API format (OpenAI or Anthropic compatible).
            force_refresh: Whether to force refresh (ignore cache).

        Returns:
            List of available models.
        """
        return await self._fetch_models(
            base_url=base_url,
            api_key=api_key,
            api_format=api_format,
            force_refresh=force_refresh,
        )

    async def _fetch_models(
        self,
        base_url: str,
        api_key: str,
        api_format: APIFormat,
        force_refresh: bool = False,
    ) -> List[RemoteModelInfo]:
        """Fetch models from the provider API.

        Args:
            base_url: The base URL for the API.
            api_key: The API key.
            api_format: The API format.
            force_refresh: Whether to force refresh.

        Returns:
            List of available models.
        """
        models_url = f"{base_url.rstrip('/')}/models"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        # Add Anthropic-specific headers if needed
        if api_format == APIFormat.ANTHROPIC:
            headers["x-api-key"] = api_key
            headers["anthropic-version"] = "2023-06-01"

        # Configure proxy if enabled
        proxy = self._build_proxy_url()

        try:
            async with httpx.AsyncClient(proxy=proxy) as client:
                response = await client.get(models_url, headers=headers, timeout=30.0)
                response.raise_for_status()
                data = response.json()

                # Parse models based on API format
                return self._parse_models_response(data, api_format)

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching models: {e.response.status_code}")
            return []
        except httpx.RequestError as e:
            logger.error(f"Request error fetching models: {e}")
            return []
        except Exception as e:
            logger.error(f"Error enumerating models: {e}")
            return []

    def _build_proxy_url(self) -> Optional[str]:
        """Build proxy URL from configuration."""
        if not self.proxy_config or not self.proxy_config.enabled:
            return None

        if not self.proxy_config.proxy_host:
            return None

        proxy_type = self.proxy_config.proxy_type or "http"
        port = f":{self.proxy_config.proxy_port}" if self.proxy_config.proxy_port else ""

        if self.proxy_config.proxy_username and self.proxy_config.proxy_password:
            return (
                f"{proxy_type}://{self.proxy_config.proxy_username}:"
                f"{self.proxy_config.proxy_password}@{self.proxy_config.proxy_host}{port}"
            )
        else:
            return f"{proxy_type}://{self.proxy_config.proxy_host}{port}"

    def _parse_models_response(
        self, data: dict, api_format: APIFormat
    ) -> List[RemoteModelInfo]:
        """Parse models API response.

        Args:
            data: The API response data.
            api_format: The API format.

        Returns:
            List of RemoteModelInfo objects.
        """
        models = []

        if api_format == APIFormat.OPENAI_CHAT:
            # OpenAI format: {"data": [{"id": "...", ...}]}
            for model_data in data.get("data", []):
                model_info = self._parse_openai_model(model_data)
                if model_info:
                    models.append(model_info)
        elif api_format == APIFormat.ANTHROPIC:
            # Anthropic format: {"data": [...]} or {"models": [...]}
            model_list = data.get("models", data.get("data", []))
            for model_data in model_list:
                model_info = self._parse_anthropic_model(model_data)
                if model_info:
                    models.append(model_info)
        else:
            # Generic format: try to extract models
            model_list = data.get("models", data.get("data", []))
            for model_data in model_list:
                model_info = self._parse_generic_model(model_data)
                if model_info:
                    models.append(model_info)

        return models

    def _parse_openai_model(self, model_data: dict) -> Optional[RemoteModelInfo]:
        """Parse OpenAI-format model data."""
        model_id = model_data.get("id")
        if not model_id:
            return None

        return RemoteModelInfo(
            id=model_id,
            display_name=model_data.get("id", ""),
            description=model_data.get("description"),
            context_window=model_data.get("context_window"),
            max_output_tokens=model_data.get("max_output_tokens"),
            input_cost_per_token=model_data.get("input_cost_per_token"),
            output_cost_per_token=model_data.get("output_cost_per_token"),
        )

    def _parse_anthropic_model(self, model_data: dict) -> Optional[RemoteModelInfo]:
        """Parse Anthropic-format model data."""
        model_id = model_data.get("id") or model_data.get("name")
        if not model_id:
            return None

        return RemoteModelInfo(
            id=model_id,
            display_name=model_data.get("display_name", model_id),
            description=model_data.get("description"),
            context_window=model_data.get("context_window"),
            max_output_tokens=model_data.get("max_output_tokens"),
        )

    def _parse_generic_model(self, model_data: dict) -> Optional[RemoteModelInfo]:
        """Parse generic model data."""
        model_id = model_data.get("id") or model_data.get("name")
        if not model_id:
            return None

        return RemoteModelInfo(
            id=model_id,
            display_name=model_data.get("display_name", model_data.get("id", "")),
            description=model_data.get("description"),
        )


async def enumerate_models(
    base_url: str,
    api_key: str,
    api_format: str = "openai_chat",
    proxy_config: Optional[Dict[str, Any]] = None,
    force_refresh: bool = False,
) -> List[RemoteModelInfo]:
    """Convenience function to enumerate models from a provider.

    Args:
        base_url: The base URL for the API.
        api_key: The API key.
        api_format: The API format ("openai_chat" or "anthropic").
        proxy_config: Optional proxy configuration dict.
        force_refresh: Whether to force refresh.

    Returns:
        List of available models.
    """
    # Convert proxy_config dict to ProviderProxyConfig if provided
    proxy_cfg = None
    if proxy_config:
        proxy_cfg = ProviderProxyConfig(**proxy_config)

    # Convert api_format string to APIFormat enum
    api_fmt = APIFormat.OPENAI_CHAT
    if api_format == "anthropic":
        api_fmt = APIFormat.ANTHROPIC

    enumerator = ModelEnumerator(proxy_config=proxy_cfg)
    return await enumerator.enumerate(
        base_url=base_url,
        api_key=api_key,
        api_format=api_fmt,
        force_refresh=force_refresh,
    )


def enumerate_models_sync(
    base_url: str,
    api_key: str,
    api_format: str = "openai_chat",
    proxy_config: Optional[Dict[str, Any]] = None,
    force_refresh: bool = False,
) -> List[RemoteModelInfo]:
    """Synchronous version of enumerate_models.

    Args:
        base_url: The base URL for the API.
        api_key: The API key.
        api_format: The API format ("openai_chat" or "anthropic").
        proxy_config: Optional proxy configuration dict.
        force_refresh: Whether to force refresh.

    Returns:
        List of available models.
    """
    return asyncio.run(
        enumerate_models(
            base_url=base_url,
            api_key=api_key,
            api_format=api_format,
            proxy_config=proxy_config,
            force_refresh=force_refresh,
        )
    )
