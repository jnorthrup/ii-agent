# CC Switch Preset Package - Summary

## Purpose

Provide **unified, cc-switch compatible presets** for ii-agent with proper annotations and traits. CC Switch stays standalone while users can optionally add ii-agent presets.

## Files Created

### Core Preset Files

1. **`iiagent.svg`** (637 bytes)
   - Purple gradient icon (#6366F1 → #8B5CF6)
   - Compatible with cc-switch icon system

2. **`iiAgentProviderPresets.ts`** (7.5 KB)
   - 11 provider presets with unified traits
   - Annotations for capability-based routing
   - Follows cc-switch ProviderPreset interface exactly

3. **`iiAgentEndpoints.ts`** (4.2 KB)
   - ProviderEndpoint annotations
   - Transport definitions with API formats
   - Matches cc-switch endpoint system

4. **`slots.ts`** (2.8 KB)
   - Slot definitions for ii-agent
   - API format compatibility mappings
   - Utility functions for trait checking

### Documentation

5. **`README.md`** (3.0 KB)
   - Quick start guide
   - Installation steps
   - Usage examples

6. **`INTEGRATION.md`** (7.5 KB)
   - Detailed integration instructions
   - Trait system explanation
   - Troubleshooting guide

7. **`PACKAGE.md`** (6.9 KB)
   - Package overview
   - Architecture documentation
   - Benefits and features

8. **`openapi.yaml`** (17.2 KB)
   - OpenAPI 3.0 specification
   - Model proxy API documentation
   - REST endpoints for provider management

## Unified Traits System

Each preset includes **traits** for capability routing:

```typescript
traits: {
  claude: boolean;    // Works with Claude (requires anthropic format)
  codex: boolean;     // Works with Codex (requires openai_responses)
  gemini: boolean;    // Works with Gemini (requires google format)
  opencode: boolean;  // Works with OpenCode (multi-format)
  openclaw: boolean;  // Works with OpenClaw (anthropic/openai_chat)
}
```

## Provider Presets

| Preset ID | Category | Formats | Claude | Codex | OpenCode | OpenClaw |
|-----------|----------|---------|--------|-------|----------|----------|
| iiagent_anthropic | official | anthropic | ✅ | ❌ | ✅ | ✅ |
| iiagent_openai | official | openai_chat, openai_responses | ❌ | ✅ | ✅ | ✅ |
| iiagent_deepseek | cn_official | anthropic, openai_chat | ✅ | ❌ | ✅ | ✅ |
| iiagent_zhipu | cn_official | anthropic, openai_chat | ✅ | ❌ | ✅ | ✅ |
| iiagent_zhipu_en | cn_official | anthropic, openai_chat | ✅ | ❌ | ✅ | ✅ |
| iiagent_bailian | cn_official | anthropic, openai_chat | ✅ | ❌ | ✅ | ✅ |
| iiagent_kimi | cn_official | anthropic, openai_chat | ✅ | ❌ | ✅ | ✅ |
| iiagent_minimax | cn_official | anthropic, openai_chat | ✅ | ❌ | ✅ | ✅ |
| iiagent_minimax_en | cn_official | anthropic, openai_chat | ✅ | ❌ | ✅ | ✅ |
| iiagent_custom_anthropic | custom | anthropic, openai_chat | ✅ | ❌ | ✅ | ✅ |
| iiagent_custom_openai | custom | openai_chat, openai_responses | ❌ | ✅ | ✅ | ✅ |

## Key Features

✅ **Unified Annotations** - Follows cc-switch trait system exactly  
✅ **No Code Changes** - Works with existing cc-switch architecture  
✅ **Capability Routing** - Automatic app compatibility detection  
✅ **Transport Definitions** - API format and endpoint specifications  
✅ **Partner Support** - Promotion keys for Chinese providers  
✅ **Model Enumeration** - Supports /models endpoint detection  

## Integration Steps

### For Users

1. Copy preset files to cc-switch source
2. Add imports to endpoints.ts and provider presets
3. Add icon to icon index and metadata
4. Rebuild cc-switch

### For Developers

The preset uses cc-switch's existing interfaces:

- `ProviderEndpoint` - Endpoint annotations
- `ProviderPreset` - Provider templates  
- `Transport` - API transport definition
- `ApiFormat` - API format types
- `ProviderCategory` - Provider classification

## Architecture

```
┌─────────────────┐         ┌─────────────────┐
│   CC Switch     │         │    II-Agent     │
│                 │         │                 │
│  ┌───────────┐  │         │  ┌───────────┐  │
│  │  Presets  │◄─┼─────────┼─►│  Endpoints│  │
│  │  (unified)│  │         │  │  (unified)│  │
│  └───────────┘  │         │  └───────────┘  │
│        │        │         │        │        │
│        ▼        │         │        ▼        │
│  ┌───────────┐  │         │  ┌───────────┐  │
│  │   Slots   │  │         │  │   Slots   │  │
│  │ (unified) │  │         │  │ (unified) │  │
│  └───────────┘  │         │  └───────────┘  │
└─────────────────┘         └─────────────────┘
```

Both applications use the **same trait definitions** for capability routing.

## API Format Support

- **anthropic** - Anthropic Messages API (Claude, OpenCode, OpenClaw)
- **openai_chat** - OpenAI Chat Completions (Codex, OpenCode, OpenClaw)
- **openai_responses** - OpenAI Responses API (Codex, OpenCode, OpenClaw)
- **google** - Google Gemini API (Gemini, OpenCode)

## Configuration

### Endpoint Annotation

```typescript
{
  id: "iiagent_anthropic",
  name: "IIAgent - Anthropic",
  category: "official",
  transport: {
    formats: ["anthropic"],
    baseUrl: "https://api.anthropic.com",
    supportsModelsEndpoint: true,
  },
  traits: {
    claude: true,
    opencode: true,
    openclaw: true,
  },
}
```

### Provider Preset

```typescript
{
  id: "iiagent_anthropic",
  name: "IIAgent - Anthropic",
  category: "official",
  transport: { /* ... */ },
  traits: { /* ... */ },
  meta: {
    apiFormat: "anthropic",
    isNewApi: true,
  },
}
```

## Testing

```bash
# After integration, test in CC Switch:
pnpm dev  # in cc-switch directory

# Verify:
# 1. IIAgent presets appear in provider list
# 2. Trait-based filtering works correctly
# 3. Icon displays properly
# 4. Endpoint annotations route to correct apps
```

## Benefits

### For Users
- Single provider configuration format
- Consistent experience across tools
- Easy provider switching
- No manual config editing

### For Developers
- Clean separation of concerns
- No breaking changes
- Easy to maintain
- Clear integration boundaries

### For Maintainers
- Independent release cycles
- Optional integration
- Shared provider ecosystem
- Minimal coupling

## Support

- **II-Agent**: `src/ii_agent/llm/proxy/README.md`
- **CC Switch**: Check cc-switch repository
- **Integration**: See `INTEGRATION.md`

## License

Same as ii-agent. See main `LICENSE` file.
