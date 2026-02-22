/**
 * IIAgent Slot Definitions for CC Switch
 * 
 * Documents how cc-switch's automatic trait derivation works.
 * The deriveApps() function automatically determines app compatibility from transport.formats.
 * 
 * No manual traits needed - just set the correct transport.formats and cc-switch handles the rest.
 */

export type ApiFormat =
  | "anthropic"
  | "openai_chat"
  | "openai_responses"
  | "google";

/**
 * App slot definitions (from cc-switch/src/config/capabilities/slots.ts)
 * 
 * These define which API formats each app accepts:
 * - claude: ["anthropic"]
 * - codex: ["openai_responses"]
 * - gemini: ["google"]
 * - opencode: ["anthropic", "openai_chat", "google"]
 * - openclaw: ["anthropic", "openai_chat"]
 */
export const APP_SLOTS: Record<string, { acceptsFormats: Set<ApiFormat> }> = {
  claude: { acceptsFormats: new Set(["anthropic"]) },
  codex: { acceptsFormats: new Set(["openai_responses"]) },
  gemini: { acceptsFormats: new Set(["google"]) },
  opencode: { acceptsFormats: new Set(["anthropic", "openai_chat", "google"]) },
  openclaw: { acceptsFormats: new Set(["anthropic", "openai_chat"]) },
};

/**
 * IIAgent slot - supports both Anthropic and OpenAI formats
 */
export const IIAGENT_SLOT = {
  acceptsFormats: new Set(["anthropic", "openai_chat", "openai_responses"]),
};

/**
 * Automatic trait derivation (from cc-switch)
 * 
 * cc-switch automatically derives app compatibility from transport.formats:
 * 
 * ```typescript
 * export function deriveApps(endpoint: ProviderEndpoint): Record<string, boolean> {
 *   return {
 *     claude: fitsSlot(endpoint, APP_SLOTS.claude),
 *     codex: fitsSlot(endpoint, APP_SLOTS.codex),
 *     gemini: fitsSlot(endpoint, APP_SLOTS.gemini),
 *     opencode: fitsSlot(endpoint, APP_SLOTS.opencode),
 *     openclaw: fitsSlot(endpoint, APP_SLOTS.openclaw),
 *   };
 * }
 * 
 * export function fitsSlot(endpoint: ProviderEndpoint, slot: Slot): boolean {
 *   for (const fmt of endpoint.transport.formats) {
 *     if (slot.acceptsFormats.has(fmt)) return true;
 *   }
 *   return false;
 * }
 * ```
 * 
 * Examples:
 * - formats: ["anthropic"] → claude: true, opencode: true, openclaw: true
 * - formats: ["openai_chat"] → opencode: true, openclaw: true
 * - formats: ["openai_chat", "openai_responses"] → codex: true, opencode: true, openclaw: true
 * - formats: ["anthropic", "openai_chat"] → claude: true, opencode: true, openclaw: true
 */

export interface ProviderEndpoint {
  id: string;
  name: string;
  category: "official" | "cn_official" | "aggregator" | "partner" | "custom";
  transport: {
    formats: Set<ApiFormat>;
    baseUrl: string;
    supportsModelsEndpoint: boolean;
  };
  icon?: string;
  iconColor?: string;
  websiteUrl?: string;
  apiKeyUrl?: string;
  isPartner?: boolean;
  partnerPromotionKey?: string;
}

export function fitsSlot(endpoint: ProviderEndpoint, slot: { acceptsFormats: Set<ApiFormat> }): boolean {
  for (const fmt of endpoint.transport.formats) {
    if (slot.acceptsFormats.has(fmt)) return true;
  }
  return false;
}

export function deriveApps(endpoint: ProviderEndpoint): Record<string, boolean> {
  return {
    claude: fitsSlot(endpoint, APP_SLOTS.claude),
    codex: fitsSlot(endpoint, APP_SLOTS.codex),
    gemini: fitsSlot(endpoint, APP_SLOTS.gemini),
    opencode: fitsSlot(endpoint, APP_SLOTS.opencode),
    openclaw: fitsSlot(endpoint, APP_SLOTS.openclaw),
  };
}

/**
 * Check if endpoint is universal (works with claude, codex, and opencode)
 */
export function isUniversal(endpoint: ProviderEndpoint): boolean {
  const apps = deriveApps(endpoint);
  return apps.claude && apps.codex && apps.opencode;
}

/**
 * Get ii-agent endpoints filtered by app
 */
export function iiAgentFlowTo(
  endpoints: ProviderEndpoint[],
  appId: string,
): ProviderEndpoint[] {
  const slot = appId === "ii-agent" ? IIAGENT_SLOT : APP_SLOTS[appId];
  if (!slot) return [];
  return endpoints.filter((ep) => fitsSlot(ep, slot));
}
