# IIAgent Preset Package for CC Switch

Unified provider presets for ii-agent integration with CC Switch. Uses automatic trait derivation based on `transport.formats`.

## Files

```
cc-switch-preset/
├── iiagent.svg                      # IIAgent icon
├── iiAgentProviderPresets.ts        # Provider presets (11 total)
├── iiAgentEndpoints.ts              # Endpoint annotations
├── slots.ts                         # Slot definitions and derivation logic
├── IIAGENT_CAPABILITY_MATRIX.md     # Provider capability documentation
├── INTEGRATION.md                   # Integration guide
├── PACKAGE.md                       # Package overview
└── SUMMARY.md                       # Quick summary
```

## Quick Start

### 1. Copy Files

```bash
cp iiagent.svg /path/to/cc-switch/src/icons/extracted/
cp iiAgentProviderPresets.ts /path/to/cc-switch/src/config/
cp iiAgentEndpoints.ts /path/to/cc-switch/src/config/capabilities/
```

### 2. Add Icon

Edit `src/icons/extracted/index.ts` and `metadata.ts` to add `iiagent` icon.

### 3. Add Endpoints

```typescript
// src/config/capabilities/endpoints.ts
import { IIAGENT_ENDPOINTS } from "./iiAgentEndpoints";

export const ENDPOINTS: ProviderEndpoint[] = [
  // ... existing
  ...IIAGENT_ENDPOINTS,
];
```

### 4. Add Presets

```typescript
// Provider presets file
import { iiAgentPresets } from "./iiAgentProviderPresets";

export const providerPresets: ProviderPreset[] = [
  // ... existing
  ...iiAgentPresets,
];
```

### 5. Rebuild

```bash
pnpm install && pnpx build
```

## Presets

11 provider presets with automatic trait derivation:

| Preset | Formats | Universal | Apps |
|--------|---------|-----------|------|
| IIAgent - Anthropic | `["anthropic"]` | ❌ | Claude, OpenCode, OpenClaw |
| IIAgent - OpenAI | `["openai_chat", "openai_responses"]` | ❌ | Codex, OpenCode, OpenClaw |
| IIAgent - DeepSeek | `["anthropic", "openai_chat"]` | ✅ | All apps |
| IIAgent - Zhipu GLM | `["anthropic", "openai_chat"]` | ✅ | All apps |
| IIAgent - Zhipu GLM en | `["anthropic", "openai_chat"]` | ✅ | All apps |
| IIAgent - Bailian | `["anthropic", "openai_chat"]` | ✅ | All apps |
| IIAgent - Kimi | `["anthropic", "openai_chat"]` | ✅ | All apps |
| IIAgent - MiniMax | `["anthropic", "openai_chat"]` | ✅ | All apps |
| IIAgent - MiniMax en | `["anthropic", "openai_chat"]` | ✅ | All apps |
| IIAgent - Custom Anthropic | `["anthropic", "openai_chat"]` | ✅ | All apps |
| IIAgent - Custom OpenAI | `["openai_chat", "openai_responses"]` | ❌ | Codex, OpenCode, OpenClaw |

## Automatic Trait Derivation

No manual traits needed. CC Switch derives app compatibility from `transport.formats`:

```typescript
// formats: ["anthropic"] → claude, opencode, openclaw
// formats: ["openai_chat", "openai_responses"] → codex, opencode, openclaw
// formats: ["anthropic", "openai_chat"] → all apps (universal)
```

See `slots.ts` for derivation logic.

## Documentation

- **IIAGENT_CAPABILITY_MATRIX.md** - Provider capability documentation (matches cc-switch style)
- **INTEGRATION.md** - Detailed integration guide
- **slots.ts** - Slot definitions and API

## Support

- II-Agent model proxy: `src/ii_agent/llm/proxy/README.md`
- CC Switch capabilities: `docs/PROVIDER_CAPABILITY_MATRIX.md`

## License

Same as ii-agent. See main `LICENSE`.
