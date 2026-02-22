# Model Proxy for ii-agent

A unified interface for managing LLM providers, inspired by the cc-switch architecture.

## Features

- **Provider Management**: CRUD operations for LLM providers
- **Provider Switching**: Switch between providers per application
- **Model Enumeration**: Discover available models from provider APIs
- **Proxy Support**: Configure HTTP/HTTPS/SOCKS5 proxies per provider
- **Multiple API Formats**: Support for OpenAI Chat and Anthropic API formats
- **Universal Providers**: Sync providers across multiple applications

## Module Structure

```
ii_agent/llm/proxy/
├── __init__.py         # Module exports
├── types.py            # Type definitions (Provider, RemoteModelInfo, etc.)
├── config.py           # Provider configuration storage
├── factory.py          # ModelProxyFactory for creating LLM clients
├── manager.py          # ProviderManager for CRUD operations
└── enumerator.py       # Model enumeration utilities
```

## Quick Start

### 1. Basic Provider Management

```python
from ii_agent.llm.proxy import ProviderManager, Provider, ProviderCategory

# Initialize manager
manager = ProviderManager()

# Add a provider
provider = Provider(
    id="anthropic",
    name="Anthropic",
    settings_config={"api_key": "sk-ant-..."},
    category=ProviderCategory.OFFICIAL,
    website_url="https://anthropic.com",
)
success, message = manager.add_provider(provider)

# Update provider
provider.settings_config["api_key"] = "new-key"
success, message = manager.update_provider(provider)

# Delete provider
success, message = manager.delete_provider("anthropic")
```

### 2. Provider Switching

```python
# Switch provider for an application
success, message = manager.switch_provider("anthropic", "ii-agent")

# Get current provider
current = manager.get_current_provider("ii-agent")
if current:
    print(f"Current provider: {current.name}")

# Get all providers
all_providers = manager.get_all_providers()
for pid, provider in all_providers.items():
    print(f"{pid}: {provider.name}")
```

### 3. Creating LLM Clients

```python
from ii_agent.llm.proxy import ModelProxyFactory

# Initialize factory
factory = ModelProxyFactory()

# Create client from provider
client = factory.create_client(
    provider_id="anthropic",
    model="claude-sonnet-4-20250514",
)

# Use the client
messages = [[{"text": "Hello!", "type": "text_prompt"}]]
response, metadata = client.generate(
    messages=messages,
    max_tokens=1024,
    system_prompt="You are a helpful assistant.",
)
```

### 4. Model Enumeration

```python
from ii_agent.llm.proxy import enumerate_models

# Enumerate models from OpenAI-compatible API
models = await enumerate_models(
    base_url="https://api.openai.com/v1",
    api_key="sk-...",
    api_format="openai_chat",
)

for model in models:
    print(f"{model.id}: {model.display_name}")
```

### 5. Proxy Configuration

```python
from ii_agent.llm.proxy import Provider, ProviderProxyConfig, ProviderMeta

# Configure proxy for a provider
proxy_config = ProviderProxyConfig(
    enabled=True,
    proxy_type="http",
    proxy_host="proxy.example.com",
    proxy_port=8080,
    proxy_username="user",
    proxy_password="pass",
)

provider = Provider(
    id="my-provider",
    name="My Provider",
    settings_config={"api_key": "sk-..."},
    meta=ProviderMeta(
        proxy_config=proxy_config,
        api_format="openai_chat",
    ),
)
```

### 6. Advanced: Direct Factory Usage

```python
from ii_agent.llm.proxy import ProviderConfig, ModelProxyFactory

# Use custom config directory
config = ProviderConfig(config_dir=Path("/custom/config/dir"))
factory = ModelProxyFactory(provider_config=config)

# Create client with overrides
client = factory.create_client(
    provider_id="my-provider",
    model="custom-model",
    override_config={
        "temperature": 0.7,
        "max_retries": 5,
    },
)
```

## API Reference

### Types

- `Provider`: Provider configuration
- `ProviderCategory`: Provider category (official, aggregator, third_party, custom)
- `ProviderMeta`: Provider metadata (proxy, test config, etc.)
- `ProviderProxyConfig`: Proxy configuration
- `ProviderTestConfig`: Test configuration for providers
- `RemoteModelInfo`: Remote model information
- `UniversalProvider`: Universal provider for multi-app sync
- `APIFormat`: API format enum (anthropic, openai_chat)
- `ProxyType`: Proxy type enum (http, https, socks5)

### ProviderManager

- `get_all_providers()`: Get all providers
- `get_provider(provider_id)`: Get specific provider
- `add_provider(provider)`: Add new provider
- `update_provider(provider)`: Update existing provider
- `upsert_provider(provider)`: Add or update provider
- `delete_provider(provider_id)`: Delete provider
- `switch_provider(provider_id, app_id)`: Switch provider for app
- `get_current_provider(app_id)`: Get current provider for app
- `enumerate_models(provider_id)`: Enumerate models for provider

### ModelProxyFactory

- `create_client(provider_id, model)`: Create LLM client from provider
- `create_client_from_provider(provider, model)`: Create client from Provider object
- `get_available_models(provider_id)`: Get available models (cached)

### Model Enumeration

- `enumerate_models(base_url, api_key, api_format)`: Async model enumeration
- `enumerate_models_sync(...)`: Synchronous version

## Configuration Storage

Provider configurations are stored in `~/.ii-agent/providers/providers.json` by default.

```json
{
  "anthropic": {
    "id": "anthropic",
    "name": "Anthropic",
    "settings_config": {
      "api_key": "sk-ant-..."
    },
    "category": "official",
    "website_url": "https://anthropic.com"
  },
  "_app_ii-agent": {
    "current_provider": "anthropic"
  }
}
```

## Migration from cc-switch

The model proxy is designed to be compatible with cc-switch concepts:

| cc-switch | ii-agent Model Proxy |
|-----------|---------------------|
| Provider | Provider |
| ProviderMeta | ProviderMeta |
| ProviderProxyConfig | ProviderProxyConfig |
| providersApi | ProviderManager |
| enumerate_models | enumerate_models |

## Future Enhancements

- [ ] Universal provider sync to multiple applications
- [ ] Provider testing utilities
- [ ] Model cost tracking
- [ ] Usage statistics integration
- [ ] WebDAV sync for provider configurations
- [ ] MCP server integration
