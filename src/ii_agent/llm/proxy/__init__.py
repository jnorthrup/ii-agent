"""Model proxy module for ii-agent.

This module provides a unified interface for managing LLM providers,
similar to the cc-switch architecture. It supports:

- Provider CRUD operations
- Provider switching per application
- Model enumeration from provider APIs
- Proxy configuration support
- Universal providers for multi-app sync

Example usage:
    from ii_agent.llm.proxy import ProviderManager, ModelProxyFactory

    # Get provider manager
    manager = ProviderManager()

    # Add a provider
    from ii_agent.llm.proxy.types import Provider, ProviderCategory
    provider = Provider(
        id="my-provider",
        name="My Provider",
        settings_config={"api_key": "sk-..."},
        category=ProviderCategory.CUSTOM,
    )
    success, message = manager.add_provider(provider)

    # Switch provider for an app
    success, message = manager.switch_provider("my-provider", "ii-agent")

    # Create LLM client from provider
    factory = ModelProxyFactory()
    client = factory.create_client(
        provider_id="my-provider",
        model="claude-sonnet-4-20250514",
    )

    # Enumerate models
    from ii_agent.llm.proxy.enumerator import enumerate_models
    models = await enumerate_models(
        base_url="https://api.openai.com/v1",
        api_key="sk-...",
        api_format="openai_chat",
    )
"""

from .types import (
    Provider,
    ProviderCategory,
    ProviderMeta,
    ProviderProxyConfig,
    ProviderTestConfig,
    RemoteModelInfo,
    UniversalProvider,
    UniversalProvidersMap,
    APIFormat,
    ProxyType,
)

from .config import ProviderConfig, get_provider_config

from .factory import ModelProxyFactory, get_model_proxy_factory

from .manager import ProviderManager, get_provider_manager

from .enumerator import (
    ModelEnumerator,
    enumerate_models,
    enumerate_models_sync,
)

__all__ = [
    # Types
    "Provider",
    "ProviderCategory",
    "ProviderMeta",
    "ProviderProxyConfig",
    "ProviderTestConfig",
    "RemoteModelInfo",
    "UniversalProvider",
    "UniversalProvidersMap",
    "APIFormat",
    "ProxyType",
    # Config
    "ProviderConfig",
    "get_provider_config",
    # Factory
    "ModelProxyFactory",
    "get_model_proxy_factory",
    # Manager
    "ProviderManager",
    "get_provider_manager",
    # Enumerator
    "ModelEnumerator",
    "enumerate_models",
    "enumerate_models_sync",
]
