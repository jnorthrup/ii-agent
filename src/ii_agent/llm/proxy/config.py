"""Provider configuration management."""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
import logging

from .types import Provider, ProviderCategory, ProviderMeta

logger = logging.getLogger(__name__)


class ProviderConfig:
    """Manages provider configurations."""

    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize provider configuration.

        Args:
            config_dir: Directory to store configuration. Defaults to ~/.ii-agent/providers/
        """
        if config_dir is None:
            config_dir = Path.home() / ".ii-agent" / "providers"
        self.config_dir = config_dir
        self.config_file = self.config_dir / "providers.json"
        self._ensure_config_dir()

    def _ensure_config_dir(self) -> None:
        """Ensure configuration directory exists."""
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def _load_config(self) -> Dict[str, dict]:
        """Load configuration from file."""
        if not self.config_file.exists():
            return {}
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse provider config: {e}")
            return {}
        except Exception as e:
            logger.error(f"Failed to load provider config: {e}")
            return {}

    def _save_config(self, config: Dict[str, dict]) -> bool:
        """Save configuration to file."""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Failed to save provider config: {e}")
            return False

    def get_all(self) -> Dict[str, Provider]:
        """Get all providers."""
        config = self._load_config()
        return {k: Provider(**v) for k, v in config.items()}

    def get(self, provider_id: str) -> Optional[Provider]:
        """Get a specific provider by ID."""
        config = self._load_config()
        if provider_id in config:
            return Provider(**config[provider_id])
        return None

    def add(self, provider: Provider) -> bool:
        """Add a new provider."""
        config = self._load_config()
        if provider.id in config:
            logger.warning(f"Provider {provider.id} already exists")
            return False
        config[provider.id] = provider.model_dump()
        return self._save_config(config)

    def update(self, provider: Provider) -> bool:
        """Update an existing provider."""
        config = self._load_config()
        if provider.id not in config:
            logger.warning(f"Provider {provider.id} does not exist")
            return False
        config[provider.id] = provider.model_dump()
        return self._save_config(config)

    def upsert(self, provider: Provider) -> bool:
        """Add or update a provider."""
        config = self._load_config()
        config[provider.id] = provider.model_dump()
        return self._save_config(config)

    def delete(self, provider_id: str) -> bool:
        """Delete a provider."""
        config = self._load_config()
        if provider_id not in config:
            logger.warning(f"Provider {provider_id} does not exist")
            return False
        del config[provider_id]
        return self._save_config(config)

    def get_current(self, app_id: str) -> Optional[str]:
        """Get current provider for an app."""
        config = self._load_config()
        app_config = config.get(f"_app_{app_id}", {})
        return app_config.get("current_provider")

    def set_current(self, app_id: str, provider_id: str) -> bool:
        """Set current provider for an app."""
        config = self._load_config()
        if f"_app_{app_id}" not in config:
            config[f"_app_{app_id}"] = {}
        config[f"_app_{app_id}"]["current_provider"] = provider_id
        return self._save_config(config)

    def update_sort_order(self, updates: List[Dict[str, int]]) -> bool:
        """Update provider sort order."""
        config = self._load_config()
        for update in updates:
            provider_id = update.get("id")
            sort_index = update.get("sort_index")
            if provider_id and sort_index is not None and provider_id in config:
                config[provider_id]["sort_index"] = sort_index
        return self._save_config(config)

    def import_default(self) -> bool:
        """Import default providers."""
        default_providers = {
            "anthropic": Provider(
                id="anthropic",
                name="Anthropic",
                settings_config={"api_key": ""},
                website_url="https://anthropic.com",
                category=ProviderCategory.OFFICIAL,
                icon="anthropic",
                icon_color="#D8A657",
            ),
            "openai": Provider(
                id="openai",
                name="OpenAI",
                settings_config={"api_key": ""},
                website_url="https://openai.com",
                category=ProviderCategory.OFFICIAL,
                icon="openai",
                icon_color="#00A67E",
            ),
        }
        config = self._load_config()
        for pid, provider in default_providers.items():
            if pid not in config:
                config[pid] = provider.model_dump()
        return self._save_config(config)


# Singleton instance
_provider_config: Optional[ProviderConfig] = None


def get_provider_config(config_dir: Optional[Path] = None) -> ProviderConfig:
    """Get or create provider config singleton."""
    global _provider_config
    if _provider_config is None:
        _provider_config = ProviderConfig(config_dir)
    return _provider_config
