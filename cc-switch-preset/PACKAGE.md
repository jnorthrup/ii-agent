# CC Switch Preset Package for II-Agent

## Purpose

This package enables **CC Switch** to stay standalone while providing ii-agent preset configurations for users who want to manage LLM providers across both applications.

## Intent

- **CC Switch remains standalone** - No code changes required in CC Switch core
- **Optional integration** - Users can choose to add ii-agent presets
- **Launcher assistance** - Helps users configure providers consistently across tools
- **Shared provider management** - Use the same LLM providers in CC Switch and ii-agent

## What's Included

```
cc-switch-preset/
├── README.md                    # Quick start guide
├── INTEGRATION.md               # Detailed integration instructions
├── iiagent.svg                  # IIAgent icon for CC Switch UI
├── iiAgentProviderPresets.ts    # Provider preset definitions
└── openapi.yaml                 # OpenAPI 3.0 spec for model proxy API
```

## Quick Start

### For Users

1. **Copy preset files to CC Switch:**
   ```bash
   cp -r cc-switch-preset/* /path/to/cc-switch/src/
   ```

2. **Follow integration guide** in `INTEGRATION.md`

3. **Launch CC Switch** - ii-agent presets will appear in provider list

### For Developers

The preset package provides:

1. **Icon** (`iiagent.svg`)
   - 24x24 SVG icon
   - Gradient purple theme (#6366F1 → #8B5CF6)
   - Compatible with CC Switch icon system

2. **Provider Presets** (`iiAgentProviderPresets.ts`)
   - 6 pre-configured providers
   - Anthropic, OpenAI, DeepSeek, Zhipu GLM
   - Custom OpenAI and Anthropic templates
   - Template variables for user input

3. **OpenAPI Specification** (`openapi.yaml`)
   - Complete REST API documentation
   - Provider CRUD operations
   - Model enumeration endpoints
   - Universal provider sync

4. **Documentation**
   - Installation guide
   - Configuration examples
   - Troubleshooting tips

## Provider Presets

| Name | Category | API Format | Default Model |
|------|----------|------------|---------------|
| IIAgent - Anthropic | official | anthropic | claude-sonnet-4-20250514 |
| IIAgent - OpenAI | official | openai_chat | gpt-4.1 |
| IIAgent - DeepSeek | cn_official | anthropic | DeepSeek-V3.2 |
| IIAgent - Zhipu GLM | cn_official | anthropic | glm-4.7 |
| IIAgent - Custom OpenAI | custom | openai_chat | user-defined |
| IIAgent - Custom Anthropic | custom | anthropic | user-defined |

## Model Proxy Features

The ii-agent model proxy (documented in `src/ii_agent/llm/proxy/`) provides:

- ✅ Provider CRUD operations
- ✅ Provider switching per application
- ✅ Model enumeration from APIs
- ✅ HTTP/HTTPS/SOCKS5 proxy support
- ✅ Multiple API formats (OpenAI, Anthropic)
- ✅ Universal provider sync
- ✅ JSON-based configuration storage

## Architecture

```
┌─────────────────┐         ┌─────────────────┐
│   CC Switch     │         │    II-Agent     │
│                 │         │                 │
│  ┌───────────┐  │         │  ┌───────────┐  │
│  │  Presets  │◄─┼─────────┼─►│   Proxy   │  │
│  │  (shared) │  │         │  │  System   │  │
│  └───────────┘  │         │  └───────────┘  │
│                 │         │                 │
│  Config:        │         │  Config:        │
│  ~/.cc-switch/  │         │  ~/.ii-agent/   │
└─────────────────┘         └─────────────────┘
```

Both applications can:
- Share the same provider configurations
- Use the same API keys
- Switch between providers independently
- Enumerate models from the same endpoints

## Usage Example

After integration, users can:

1. **Add a provider in CC Switch:**
   - Select "IIAgent - Anthropic" preset
   - Enter API key
   - Provider saved to `~/.cc-switch/config.json`

2. **Use same provider in ii-agent:**
   - Provider automatically available via model proxy
   - Or import from CC Switch config
   - Use in ii-agent workflows

3. **Switch providers:**
   - CC Switch manages provider for CC apps
   - II-Agent manages provider for agent tasks
   - Both use same underlying API

## Benefits

### For Users
- Single source of truth for provider configs
- Consistent provider management
- Easy to switch between tools
- No manual config file editing

### For Developers
- Clean separation of concerns
- CC Switch remains independent
- ii-agent maintains its own system
- Optional integration path

### For Maintainers
- No breaking changes to either project
- Presets can be updated independently
- Easy to add new providers
- Clear integration boundaries

## API Endpoints

The model proxy exposes these endpoints (see `openapi.yaml`):

```
GET    /api/v1/providers              # List all providers
POST   /api/v1/providers              # Add provider
GET    /api/v1/providers/{id}         # Get provider
PUT    /api/v1/providers/{id}         # Update provider
DELETE /api/v1/providers/{id}         # Delete provider
POST   /api/v1/providers/{id}/switch  # Switch for app
GET    /api/v1/providers/{id}/models  # Enumerate models
POST   /api/v1/providers/import-default # Import defaults
PUT    /api/v1/providers/sort         # Update sort order
GET    /api/v1/universal-providers    # Get universal providers
POST   /api/v1/universal-providers    # Create/Update universal
POST   /api/v1/universal-providers/{id}/sync # Sync to apps
```

## Configuration Format

Providers are stored as JSON:

```json
{
  "anthropic": {
    "id": "anthropic",
    "name": "Anthropic",
    "settingsConfig": {
      "api_key": "sk-ant-...",
      "base_url": "https://api.anthropic.com"
    },
    "category": "official",
    "icon": "anthropic",
    "iconColor": "#D8A657",
    "meta": {
      "apiFormat": "anthropic"
    }
  },
  "_app_ii-agent": {
    "current_provider": "anthropic"
  }
}
```

## Testing

Test the integration:

```bash
# 1. Start ii-agent server
python -m ii_agent.server

# 2. Test model proxy API
curl http://localhost:8000/api/v1/providers

# 3. Launch CC Switch
pnpm dev  # in cc-switch directory

# 4. Verify ii-agent presets appear
# Look for "IIAgent - *" in provider list
```

## Future Enhancements

Potential improvements:

- [ ] Automatic config sync between applications
- [ ] Shared provider test utilities
- [ ] Unified model cost tracking
- [ ] Cross-application usage statistics
- [ ] WebDAV sync for provider configs
- [ ] MCP server integration

## Support

- **II-Agent Issues**: Check `docs/` and `src/ii_agent/llm/proxy/README.md`
- **CC Switch Issues**: Check CC Switch documentation
- **Integration Issues**: See `INTEGRATION.md`

## License

Same license as ii-agent. See main `LICENSE` file.
