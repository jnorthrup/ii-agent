"""Types for model proxy system."""

from typing import Literal, Optional, Dict, Any
from pydantic import BaseModel, Field


class ProviderCategory(str):
    """Provider category types."""
    OFFICIAL = "official"
    CN_OFFICIAL = "cn_official"
    AGGREGATOR = "aggregator"
    THIRD_PARTY = "third_party"
    CUSTOM = "custom"


class ProxyType(str):
    """Proxy type for provider configuration."""
    HTTP = "http"
    HTTPS = "https"
    SOCKS5 = "socks5"


class APIFormat(str):
    """API format for provider compatibility."""
    ANTHROPIC = "anthropic"
    OPENAI_CHAT = "openai_chat"


class ProviderProxyConfig(BaseModel):
    """Proxy configuration for a provider."""
    enabled: bool = Field(default=False, description="Whether proxy is enabled")
    proxy_type: Optional[ProxyType] = Field(default=None, description="Proxy type")
    proxy_host: Optional[str] = Field(default=None, description="Proxy host")
    proxy_port: Optional[int] = Field(default=None, description="Proxy port")
    proxy_username: Optional[str] = Field(default=None, description="Proxy username")
    proxy_password: Optional[str] = Field(default=None, description="Proxy password")


class ProviderTestConfig(BaseModel):
    """Test configuration for a provider."""
    enabled: bool = Field(default=False, description="Whether test config is enabled")
    test_model: Optional[str] = Field(default=None, description="Test model name")
    timeout_secs: Optional[int] = Field(default=None, description="Timeout in seconds")
    test_prompt: Optional[str] = Field(default=None, description="Test prompt")
    max_retries: Optional[int] = Field(default=None, description="Max retries")


class ProviderMeta(BaseModel):
    """Metadata for a provider."""
    test_config: Optional[ProviderTestConfig] = Field(default=None)
    proxy_config: Optional[ProviderProxyConfig] = Field(default=None)
    cost_multiplier: Optional[str] = Field(default=None)
    pricing_model_source: Optional[str] = Field(default=None)
    api_format: Optional[APIFormat] = Field(default=None)
    is_new_api: Optional[bool] = Field(default=None, description="Whether NewAPI compatible")


class Provider(BaseModel):
    """Provider configuration."""
    id: str = Field(description="Unique provider identifier")
    name: str = Field(description="Provider name")
    settings_config: Dict[str, Any] = Field(
        description="Provider settings (API keys, base URLs, etc.)"
    )
    website_url: Optional[str] = Field(default=None, description="Provider website URL")
    category: Optional[ProviderCategory] = Field(default=None, description="Provider category")
    notes: Optional[str] = Field(default=None, description="Provider notes")
    icon: Optional[str] = Field(default=None, description="Icon name")
    icon_color: Optional[str] = Field(default=None, description="Icon color (hex)")
    meta: Optional[ProviderMeta] = Field(default=None, description="Provider metadata")
    sort_index: Optional[int] = Field(default=None, description="Sort order")
    created_at: Optional[int] = Field(default=None, description="Creation timestamp")


class RemoteModelInfo(BaseModel):
    """Information about a remote model."""
    id: str = Field(description="Model identifier")
    provider: Optional[str] = Field(default=None, description="Provider ID")
    display_name: Optional[str] = Field(default=None, description="Display name")
    description: Optional[str] = Field(default=None, description="Model description")
    context_window: Optional[int] = Field(default=None, description="Context window size")
    max_output_tokens: Optional[int] = Field(default=None, description="Max output tokens")
    input_cost_per_token: Optional[float] = Field(default=None, description="Input cost")
    output_cost_per_token: Optional[float] = Field(default=None, description="Output cost")


class UniversalProvider(BaseModel):
    """Universal provider that can sync to multiple applications."""
    id: str = Field(description="Unique provider identifier")
    name: str = Field(description="Provider name")
    base_url: str = Field(description="Base URL for API")
    api_key: str = Field(description="API key")
    api_format: APIFormat = Field(default=APIFormat.ANTHROPIC, description="API format")
    enabled_apps: list[str] = Field(
        default_factory=list, description="List of enabled app IDs"
    )
    proxy_config: Optional[ProviderProxyConfig] = Field(default=None)
    meta: Optional[ProviderMeta] = Field(default=None)


class UniversalProvidersMap(BaseModel):
    """Map of universal providers."""
    providers: Dict[str, UniversalProvider] = Field(
        default_factory=dict, description="Providers indexed by ID"
    )
