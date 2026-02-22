"""Provider manager for CRUD operations and provider switching."""

from typing import Dict, List, Optional, Tuple
import logging
import httpx

from .types import (
    Provider,
    ProviderCategory,
    ProviderMeta,
    ProviderProxyConfig,
    RemoteModelInfo,
    UniversalProvider,
    UniversalProvidersMap,
    APIFormat,
)
from .config import ProviderConfig
from .factory import ModelProxyFactory

logger = logging.getLogger(__name__)


class ProviderManager:
    """Manages provider CRUD operations and switching."""

    def __init__(self, config: Optional[ProviderConfig] = None):
        """Initialize the provider manager.

        Args:
            config: Optional provider configuration instance.
        """
        self.config = config or ProviderConfig()
        self.factory = ModelProxyFactory(self.config)

    # ========================================================================
    # Provider CRUD Operations
    # ========================================================================

    def get_all_providers(self) -> Dict[str, Provider]:
        """Get all providers."""
        return self.config.get_all()

    def get_provider(self, provider_id: str) -> Optional[Provider]:
        """Get a specific provider by ID."""
        return self.config.get(provider_id)

    def add_provider(self, provider: Provider) -> Tuple[bool, str]:
        """Add a new provider.

        Args:
            provider: The provider to add.

        Returns:
            Tuple of (success, message).
        """
        if self.config.get(provider.id):
            return False, f"Provider {provider.id} already exists"

        success = self.config.add(provider)
        if success:
            return True, f"Provider {provider.name} added successfully"
        return False, "Failed to add provider"

    def update_provider(self, provider: Provider) -> Tuple[bool, str]:
        """Update an existing provider.

        Args:
            provider: The provider to update.

        Returns:
            Tuple of (success, message).
        """
        if not self.config.get(provider.id):
            return False, f"Provider {provider.id} does not exist"

        success = self.config.update(provider)
        if success:
            return True, f"Provider {provider.name} updated successfully"
        return False, "Failed to update provider"

    def upsert_provider(self, provider: Provider) -> Tuple[bool, str]:
        """Add or update a provider.

        Args:
            provider: The provider to upsert.

        Returns:
            Tuple of (success, message).
        """
        success = self.config.upsert(provider)
        if success:
            return True, f"Provider {provider.name} saved successfully"
        return False, "Failed to save provider"

    def delete_provider(self, provider_id: str) -> Tuple[bool, str]:
        """Delete a provider.

        Args:
            provider_id: The provider ID to delete.

        Returns:
            Tuple of (success, message).
        """
        provider = self.config.get(provider_id)
        if not provider:
            return False, f"Provider {provider_id} does not exist"

        success = self.config.delete(provider_id)
        if success:
            return True, f"Provider {provider.name} deleted successfully"
        return False, "Failed to delete provider"

    # ========================================================================
    # Provider Switching
    # ========================================================================

    def get_current_provider(self, app_id: str) -> Optional[Provider]:
        """Get current provider for an app.

        Args:
            app_id: The application ID.

        Returns:
            The current provider or None if not set.
        """
        current_id = self.config.get_current(app_id)
        if current_id:
            return self.config.get(current_id)
        return None

    def switch_provider(self, provider_id: str, app_id: str) -> Tuple[bool, str]:
        """Switch to a different provider for an app.

        Args:
            provider_id: The provider ID to switch to.
            app_id: The application ID.

        Returns:
            Tuple of (success, message).
        """
        provider = self.config.get(provider_id)
        if not provider:
            return False, f"Provider {provider_id} does not exist"

        success = self.config.set_current(app_id, provider_id)
        if success:
            return True, f"Switched to {provider.name}"
        return False, "Failed to switch provider"

    def update_sort_order(
        self, updates: List[Dict[str, int]]
    ) -> Tuple[bool, str]:
        """Update provider sort order.

        Args:
            updates: List of {id, sort_index} dictionaries.

        Returns:
            Tuple of (success, message).
        """
        success = self.config.update_sort_order(updates)
        if success:
            return True, "Sort order updated"
        return False, "Failed to update sort order"

    def import_default_providers(self) -> Tuple[bool, str]:
        """Import default providers.

        Returns:
            Tuple of (success, message).
        """
        success = self.config.import_default()
        if success:
            return True, "Default providers imported"
        return False, "Failed to import default providers"

    # ========================================================================
    # Model Enumeration
    # ========================================================================

    async def enumerate_models(
        self,
        provider_id: str,
        force_refresh: bool = False,
    ) -> List[RemoteModelInfo]:
        """Enumerate available models for a provider.

        Args:
            provider_id: The provider ID.
            force_refresh: Whether to force refresh from API.

        Returns:
            List of available models.
        """
        provider = self.config.get(provider_id)
        if not provider:
            raise ValueError(f"Provider {provider_id} not found")

        settings = provider.settings_config or {}
        meta = provider.meta or ProviderMeta()

        api_key = settings.get("api_key")
        base_url = settings.get("base_url")
        api_format = meta.api_format or APIFormat.ANTHROPIC

        # Get proxy config if enabled
        proxy_config = None
        if meta.proxy_config and meta.proxy_config.enabled:
            proxy_config = meta.proxy_config

        return await self._fetch_models(
            base_url=base_url,
            api_key=api_key,
            api_format=api_format,
            proxy_config=proxy_config,
            force_refresh=force_refresh,
        )

    async def _fetch_models(
        self,
        base_url: Optional[str],
        api_key: Optional[str],
        api_format: APIFormat,
        proxy_config: Optional[ProviderProxyConfig] = None,
        force_refresh: bool = False,
    ) -> List[RemoteModelInfo]:
        """Fetch models from provider API.

        Args:
            base_url: The base URL for the API.
            api_key: The API key.
            api_format: The API format (OpenAI or Anthropic).
            proxy_config: Optional proxy configuration.
            force_refresh: Whether to force refresh.

        Returns:
            List of available models.
        """
        if not base_url:
            # Use default URLs based on API format
            if api_format == APIFormat.OPENAI_CHAT:
                base_url = "https://api.openai.com/v1"
            else:
                base_url = "https://api.anthropic.com/v1"

        models_url = f"{base_url.rstrip('/')}/models"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        # Add Anthropic-specific header if needed
        if api_format == APIFormat.ANTHROPIC:
            headers["x-api-key"] = api_key or ""
            headers["anthropic-version"] = "2023-06-01"

        # Configure proxy if enabled
        proxy = None
        if proxy_config and proxy_config.enabled:
            proxy = self._build_proxy_url(proxy_config)

        try:
            async with httpx.AsyncClient(proxy=proxy) as client:
                response = await client.get(models_url, headers=headers, timeout=30.0)
                response.raise_for_status()
                data = response.json()

                # Parse models based on API format
                return self._parse_models_response(data, api_format)

        except httpx.HTTPError as e:
            logger.error(f"Failed to fetch models: {e}")
            return []
        except Exception as e:
            logger.error(f"Error enumerating models: {e}")
            return []

    def _build_proxy_url(self, proxy_config: ProviderProxyConfig) -> str:
        """Build proxy URL from configuration."""
        if not proxy_config.enabled or not proxy_config.proxy_host:
            return None

        proxy_type = proxy_config.proxy_type or "http"
        port = f":{proxy_config.proxy_port}" if proxy_config.proxy_port else ""

        if proxy_config.proxy_username and proxy_config.proxy_password:
            return (
                f"{proxy_type}://{proxy_config.proxy_username}:"
                f"{proxy_config.proxy_password}@{proxy_config.proxy_host}{port}"
            )
        else:
            return f"{proxy_type}://{proxy_config.proxy_host}{port}"

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
                models.append(
                    RemoteModelInfo(
                        id=model_data.get("id", ""),
                        display_name=model_data.get("id", ""),
                        description=model_data.get("description"),
                        context_window=model_data.get("context_window"),
                        max_output_tokens=model_data.get("max_output_tokens"),
                    )
                )
        else:
            # Anthropic or other format: assume list of models
            model_list = data.get("models", data.get("data", []))
            for model_data in model_list:
                models.append(
                    RemoteModelInfo(
                        id=model_data.get("id", model_data.get("name", "")),
                        display_name=model_data.get("display_name", model_data.get("id")),
                        description=model_data.get("description"),
                    )
                )

        return models

    # ========================================================================
    # Universal Provider Operations
    # ========================================================================

    def get_universal_providers(self) -> UniversalProvidersMap:
        """Get all universal providers."""
        # TODO: Implement universal provider storage
        return UniversalProvidersMap(providers={})

    def get_universal_provider(
        self, provider_id: str
    ) -> Optional[UniversalProvider]:
        """Get a universal provider by ID."""
        all_providers = self.get_universal_providers()
        return all_providers.providers.get(provider_id)

    def upsert_universal_provider(
        self, provider: UniversalProvider
    ) -> Tuple[bool, str]:
        """Add or update a universal provider.

        Args:
            provider: The universal provider to upsert.

        Returns:
            Tuple of (success, message).
        """
        # TODO: Implement universal provider storage
        return False, "Universal providers not yet implemented"

    def delete_universal_provider(self, provider_id: str) -> Tuple[bool, str]:
        """Delete a universal provider.

        Args:
            provider_id: The provider ID to delete.

        Returns:
            Tuple of (success, message).
        """
        # TODO: Implement universal provider storage
        return False, "Universal providers not yet implemented"

    async def sync_universal_provider(self, provider_id: str) -> Tuple[bool, str]:
        """Sync a universal provider to enabled applications.

        Args:
            provider_id: The provider ID to sync.

        Returns:
            Tuple of (success, message).
        """
        provider = self.get_universal_provider(provider_id)
        if not provider:
            return False, f"Universal provider {provider_id} not found"

        # TODO: Implement sync to applications
        return True, f"Synced {provider.name} to {len(provider.enabled_apps)} apps"


# Singleton instance
_manager: Optional[ProviderManager] = None


def get_provider_manager(config: Optional[ProviderConfig] = None) -> ProviderManager:
    """Get or create provider manager singleton."""
    global _manager
    if _manager is None:
        _manager = ProviderManager(config)
    return _manager
