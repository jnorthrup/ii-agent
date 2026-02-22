"""Model proxy factory for creating LLM clients from provider configurations."""

from typing import Optional, Dict, Any
import logging

from ii_agent.core.config.llm_config import LLMConfig, APITypes
from ii_agent.llm.base import LLMClient
from ii_agent.llm.openai import OpenAIDirectClient, OpenAIResponsesClient
from ii_agent.llm.anthropic import AnthropicDirectClient
from ii_agent.llm.gemini import GeminiDirectClient

from .types import Provider, APIFormat, ProviderProxyConfig
from .config import ProviderConfig

logger = logging.getLogger(__name__)


class ModelProxyFactory:
    """Factory for creating LLM clients from provider configurations."""

    def __init__(self, provider_config: Optional[ProviderConfig] = None):
        """Initialize the factory.

        Args:
            provider_config: Optional provider configuration instance.
        """
        self.provider_config = provider_config or ProviderConfig()

    def create_client(
        self,
        provider_id: str,
        model: str,
        override_config: Optional[Dict[str, Any]] = None,
    ) -> LLMClient:
        """Create an LLM client from a provider configuration.

        Args:
            provider_id: The provider ID to use.
            model: The model name to use.
            override_config: Optional configuration overrides.

        Returns:
            An LLMClient instance.

        Raises:
            ValueError: If provider not found or configuration is invalid.
        """
        provider = self.provider_config.get(provider_id)
        if provider is None:
            raise ValueError(f"Provider {provider_id} not found")

        llm_config = self._provider_to_llm_config(provider, model, override_config)
        return self._create_client_from_config(llm_config)

    def create_client_from_provider(
        self,
        provider: Provider,
        model: str,
        override_config: Optional[Dict[str, Any]] = None,
    ) -> LLMClient:
        """Create an LLM client directly from a Provider object.

        Args:
            provider: The Provider object.
            model: The model name to use.
            override_config: Optional configuration overrides.

        Returns:
            An LLMClient instance.
        """
        llm_config = self._provider_to_llm_config(provider, model, override_config)
        return self._create_client_from_config(llm_config)

    def _provider_to_llm_config(
        self,
        provider: Provider,
        model: str,
        override_config: Optional[Dict[str, Any]] = None,
    ) -> LLMConfig:
        """Convert a Provider to an LLMConfig.

        Args:
            provider: The Provider object.
            model: The model name.
            override_config: Optional configuration overrides.

        Returns:
            An LLMConfig instance.
        """
        settings = provider.settings_config or {}
        meta = provider.meta or ProviderMeta()

        # Determine API type from settings or metadata
        api_type = self._determine_api_type(provider, meta)

        # Extract API key
        api_key = settings.get("api_key")

        # Extract base URL
        base_url = settings.get("base_url")

        # Build LLMConfig
        config_dict = {
            "model": model,
            "api_key": api_key,
            "base_url": base_url,
            "api_type": api_type,
            "max_retries": settings.get("max_retries", 10),
            "temperature": settings.get("temperature", 0.0),
            "thinking_tokens": settings.get("thinking_tokens", 16000),
        }

        # Add Vertex AI settings if present
        if settings.get("vertex_project_id"):
            config_dict["vertex_project_id"] = settings["vertex_project_id"]
        if settings.get("vertex_region"):
            config_dict["vertex_region"] = settings["vertex_region"]

        # Add Azure settings if present
        if settings.get("azure_endpoint"):
            config_dict["azure_endpoint"] = settings["azure_endpoint"]
        if settings.get("azure_api_version"):
            config_dict["azure_api_version"] = settings["azure_api_version"]

        # Apply overrides
        if override_config:
            config_dict.update(override_config)

        return LLMConfig(**config_dict)

    def _determine_api_type(
        self, provider: Provider, meta: ProviderMeta
    ) -> APITypes:
        """Determine the API type from provider configuration.

        Args:
            provider: The Provider object.
            meta: The ProviderMeta object.

        Returns:
            The appropriate APITypes value.
        """
        # Check metadata for explicit API format
        if meta.api_format:
            if meta.api_format == APIFormat.OPENAI_CHAT:
                return APITypes.OPENAI
            elif meta.api_format == APIFormat.ANTHROPIC:
                return APITypes.ANTHROPIC

        # Check provider ID/name for hints
        provider_id = provider.id.lower()
        provider_name = provider.name.lower()

        if "anthropic" in provider_id or "anthropic" in provider_name:
            return APITypes.ANTHROPIC
        elif "openai" in provider_id or "openai" in provider_name:
            return APITypes.OPENAI
        elif "gemini" in provider_id or "gemini" in provider_name:
            return APITypes.GEMINI
        elif "custom" in provider_id or provider.category == "custom":
            return APITypes.CUSTOM

        # Default to OpenAI format for unknown providers
        return APITypes.OPENAI

    def _create_client_from_config(self, llm_config: LLMConfig) -> LLMClient:
        """Create an LLM client from an LLMConfig.

        Args:
            llm_config: The LLMConfig object.

        Returns:
            An LLMClient instance.
        """
        from ii_agent.utils.constants import is_gpt5_family

        if llm_config.api_type == APITypes.ANTHROPIC:
            return AnthropicDirectClient(llm_config=llm_config)
        elif llm_config.api_type == APITypes.OPENAI:
            if is_gpt5_family(llm_config.model):
                return OpenAIResponsesClient(llm_config=llm_config)
            else:
                return OpenAIDirectClient(llm_config=llm_config)
        elif llm_config.api_type == APITypes.GEMINI:
            return GeminiDirectClient(llm_config=llm_config)
        elif llm_config.api_type == APITypes.CUSTOM:
            # Custom endpoints use OpenAI-compatible API
            return OpenAIDirectClient(llm_config=llm_config)
        else:
            raise ValueError(f"Unsupported API type: {llm_config.api_type}")

    def get_available_models(
        self,
        provider_id: str,
    ) -> list[str]:
        """Get available models for a provider.

        Args:
            provider_id: The provider ID.

        Returns:
            List of available model names.
        """
        # TODO: Implement model enumeration
        # This would call the provider's models endpoint
        logger.warning("Model enumeration not yet implemented")
        return []


# Singleton instance
_factory: Optional[ModelProxyFactory] = None


def get_model_proxy_factory(
    provider_config: Optional[ProviderConfig] = None,
) -> ModelProxyFactory:
    """Get or create model proxy factory singleton."""
    global _factory
    if _factory is None:
        _factory = ModelProxyFactory(provider_config)
    return _factory
