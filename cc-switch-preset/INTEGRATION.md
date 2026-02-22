# II-Agent Preset Integration Guide for CC Switch

## Overview

This package provides **cc-switch compatible presets** for ii-agent. The presets work with cc-switch's **automatic trait derivation system** - no manual trait configuration needed.

## How Automatic Trait Derivation Works

CC Switch automatically determines which apps a provider works with based on `transport.formats`:

```typescript
// From cc-switch/src/config/capabilities/slots.ts
export function deriveApps(endpoint: ProviderEndpoint): Record<string, boolean> {
  return {
    claude: fitsSlot(endpoint, APP_SLOTS.claude),      // accepts: ["anthropic"]
    codex: fitsSlot(endpoint, APP_SLOTS.codex),        // accepts: ["openai_responses"]
    gemini: fitsSlot(endpoint, APP_SLOTS.gemini),      // accepts: ["google"]
    opencode: fitsSlot(endpoint, APP_SLOTS.opencode),  // accepts: ["anthropic", "openai_chat", "google"]
    openclaw: fitsSlot(endpoint, APP_SLOTS.openclaw),  // accepts: ["anthropic", "openai_chat"]
  };
}
```

### Format to App Mapping

| Transport Formats | Claude | Codex | OpenCode | OpenClaw | Gemini |
|-------------------|--------|-------|----------|----------|--------|
| `["anthropic"]` | ✅ | ❌ | ✅ | ✅ | ❌ |
| `["openai_chat"]` | ❌ | ❌ | ✅ | ✅ | ❌ |
| `["openai_responses"]` | ❌ | ✅ | ✅ | ❌ | ❌ |
| `["anthropic", "openai_chat"]` | ✅ | ❌ | ✅ | ✅ | ❌ |
| `["openai_chat", "openai_responses"]` | ❌ | ✅ | ✅ | ✅ | ❌ |
| `["google"]` | ❌ | ❌ | ✅ | ❌ | ✅ |

**No manual traits needed** - just set the correct `transport.formats` and cc-switch handles the rest!

## Quick Integration

### Step 1: Copy Files

```bash
# Copy icon
cp iiagent.svg /path/to/cc-switch/src/icons/extracted/

# Copy presets
cp iiAgentProviderPresets.ts /path/to/cc-switch/src/config/
cp iiAgentEndpoints.ts /path/to/cc-switch/src/config/capabilities/
```

### Step 2: Add Icon

Edit `/path/to/cc-switch/src/icons/extracted/index.ts`:

```typescript
export const icons: Record<string, string> = {
  // ... existing icons
  iiagent: `<svg height="1em" width="1em" style="flex:none;line-height:1" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
<title>IIAgent</title>
<defs>
  <linearGradient id="ii-agent-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#6366F1"/>
    <stop offset="100%" stop-color="#8B5CF6"/>
  </linearGradient>
</defs>
<path d="M12 2L2 7l10 5 10-5-10-5z" fill="url(#ii-agent-gradient)"/>
<path d="M2 17l10 5 10-5M2 12l10 5 10-5" stroke="url(#ii-agent-gradient)" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="12" cy="12" r="3" fill="url(#ii-agent-gradient)"/>
</svg>`,
};
```

Edit `/path/to/cc-switch/src/icons/extracted/metadata.ts`:

```typescript
export const iconMetadata: Record<string, IconMetadata> = {
  // ... existing metadata
  iiagent: {
    name: "iiagent",
    displayName: "IIAgent",
    category: "ai-provider",
    keywords: ["iiagent", "ii-agent", "agent"],
    defaultColor: "#6366F1",
  },
};
```

### Step 3: Add Endpoints

Edit `/path/to/cc-switch/src/config/capabilities/endpoints.ts`:

```typescript
import { IIAGENT_ENDPOINTS } from "./iiAgentEndpoints";

export const ENDPOINTS: ProviderEndpoint[] = [
  // ... existing endpoints
  ...IIAGENT_ENDPOINTS,
];
```

### Step 4: Add Presets

Edit your provider presets file:

```typescript
import { iiAgentPresets } from "./iiAgentProviderPresets";

export const providerPresets: ProviderPreset[] = [
  // ... existing presets
  ...iiAgentPresets,
];
```

### Step 5: Rebuild

```bash
cd /path/to/cc-switch
pnpm install
pnpm build
```

## Available Presets

All presets have **automatic trait derivation** based on their `transport.formats`:

| Preset | Formats | Auto-Derived Apps |
|--------|---------|-------------------|
| IIAgent - Anthropic | `["anthropic"]` | Claude, OpenCode, OpenClaw |
| IIAgent - OpenAI | `["openai_chat", "openai_responses"]` | Codex, OpenCode, OpenClaw |
| IIAgent - DeepSeek | `["anthropic", "openai_chat"]` | Claude, OpenCode, OpenClaw |
| IIAgent - Zhipu GLM | `["anthropic", "openai_chat"]` | Claude, OpenCode, OpenClaw |
| IIAgent - Zhipu GLM en | `["anthropic", "openai_chat"]` | Claude, OpenCode, OpenClaw |
| IIAgent - Bailian | `["anthropic", "openai_chat"]` | Claude, OpenCode, OpenClaw |
| IIAgent - Kimi | `["anthropic", "openai_chat"]` | Claude, OpenCode, OpenClaw |
| IIAgent - MiniMax | `["anthropic", "openai_chat"]` | Claude, OpenCode, OpenClaw |
| IIAgent - MiniMax en | `["anthropic", "openai_chat"]` | Claude, OpenCode, OpenClaw |
| IIAgent - Custom Anthropic | `["anthropic", "openai_chat"]` | Claude, OpenCode, OpenClaw |
| IIAgent - Custom OpenAI | `["openai_chat", "openai_responses"]` | Codex, OpenCode, OpenClaw |

## Preset Structure

Each preset follows cc-switch's interface:

```typescript
{
  id: "iiagent_anthropic",
  name: "IIAgent - Anthropic",
  category: "official" | "cn_official" | "custom",
  transport: {
    formats: ["anthropic"],  // ← Determines app compatibility
    baseUrl: "https://api.anthropic.com",
    supportsModelsEndpoint: true,
  },
  icon: "iiagent",
  iconColor: "#6366F1",
  websiteUrl: "https://github.com/ii-agent/ii-agent",
  apiKeyUrl: "https://console.anthropic.com/settings/keys",
  isPartner?: boolean,
  partnerPromotionKey?: string,
  meta?: {
    apiFormat: "anthropic" | "openai_chat",
    isNewApi: true,
  },
}
```

**No traits field needed** - app compatibility is derived automatically from `transport.formats`.

## Endpoint Annotations

Each endpoint includes transport definition:

```typescript
{
  id: "iiagent_anthropic",
  name: "IIAgent - Anthropic",
  category: "official",
  transport: t(["anthropic"], "https://api.anthropic.com", true),
  icon: "iiagent",
  iconColor: "#6366F1",
  websiteUrl: "https://github.com/ii-agent/ii-agent",
  apiKeyUrl: "https://console.anthropic.com/settings/keys",
}
```

The `t()` helper creates the transport object:

```typescript
const t = (
  formats: ApiFormat[],
  baseUrl: string,
  supportsModelsEndpoint = true,
): Transport => ({
  formats: new Set(formats),
  baseUrl,
  supportsModelsEndpoint,
});
```

## Universal Providers

Endpoints that support both `anthropic` and `openai_chat`/`openai_responses` formats are automatically marked as universal:

```typescript
export function isUniversal(endpoint: ProviderEndpoint): boolean {
  const apps = deriveApps(endpoint);
  return apps.claude && apps.codex && apps.opencode;
}
```

From ii-agent presets:
- `iiagent_deepseek` - Universal (has both formats)
- `iiagent_zhipu` - Universal
- `iiagent_kimi` - Universal
- `iiagent_minimax` - Universal
- `iiagent_custom_anthropic` - Universal
- `iiagent_custom_openai` - Universal

## Testing

After integration:

```bash
cd /path/to/cc-switch
pnpm dev
```

Verify:
1. IIAgent presets appear in provider list
2. **App compatibility is automatically derived** (no manual traits)
3. Universal providers show all apps enabled
4. Icon displays correctly

## Model Proxy API

II-Agent's model proxy provides REST API:

```bash
GET  /api/v1/providers           # List providers
POST /api/v1/providers           # Add provider
POST /api/v1/providers/{id}/switch  # Switch for app
GET  /api/v1/providers/{id}/models  # Enumerate models
```

See `openapi.yaml` for complete specification.

## Troubleshooting

### Presets Not Showing

1. Verify import statement
2. Check presets are spread into main array
3. Ensure TypeScript types match

### App Compatibility Wrong

1. Check `transport.formats` is correct
2. Verify format names match exactly (e.g., "anthropic" not "Anthropic")
3. Check APP_SLOTS definitions in slots.ts

### Icon Not Displaying

1. Verify SVG copied to correct directory
2. Check icon name matches in index.ts and metadata.ts
3. Rebuild and clear cache

## Support

- II-Agent: `src/ii_agent/llm/proxy/README.md`
- CC Switch: Check cc-switch repository
- Integration: See `slots.ts` for derivation logic
