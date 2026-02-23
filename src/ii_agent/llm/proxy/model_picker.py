"""
Model Picker Configuration for II-Agent with Tauri Integration

This module provides predefined model lists for popular providers.
Each provider has exactly 5 recommended models for different use cases.
Compatible with Tauri backend integration.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class ModelInfo(BaseModel):
    """Information about a model for Tauri integration."""
    id: str = Field(..., description="Unique model identifier")
    name: str = Field(..., description="Display name")
    provider: str = Field(..., description="Provider name")
    description: str = Field(..., description="Short description")
    context_window: int = Field(..., description="Context window size in tokens")
    max_output_tokens: int = Field(..., description="Maximum output tokens")
    input_cost_per_token: float = Field(default=0.0, description="Cost per input token")
    output_cost_per_token: float = Field(default=0.0, description="Cost per output token")
    capabilities: List[str] = Field(default_factory=list, description="Model capabilities")
    recommended_for: List[str] = Field(default_factory=list, description="Recommended use cases")
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "anthropic/claude-3.5-sonnet",
                "name": "Claude 3.5 Sonnet",
                "provider": "Anthropic",
                "description": "Best overall performance",
                "context_window": 200000,
                "max_output_tokens": 8192,
                "capabilities": ["vision", "function_calling"],
                "recommended_for": ["coding", "chat"]
            }
        }


class ProviderModelPicker(BaseModel):
    """Model picker configuration for a provider - exactly 5 models."""
    provider_id: str = Field(..., description="Provider identifier")
    provider_name: str = Field(..., description="Provider display name")
    models: List[ModelInfo] = Field(..., min_length=5, max_length=5, description="Exactly 5 models")
    default_model: str = Field(..., description="Default model ID")
    
    class Config:
        populate_by_name = True


# ============================================================================
# OpenRouter - 5 Models
# ============================================================================
OPENROUTER_MODELS = ProviderModelPicker(
    provider_id="openrouter",
    provider_name="OpenRouter",
    default_model="anthropic/claude-3.5-sonnet",
    models=[
        ModelInfo(
            id="anthropic/claude-3.5-sonnet",
            name="Claude 3.5 Sonnet",
            provider="Anthropic",
            description="Best overall performance for most tasks",
            context_window=200000,
            max_output_tokens=8192,
            input_cost_per_token=0.000003,
            output_cost_per_token=0.000015,
            capabilities=["vision", "function_calling", "reasoning"],
            recommended_for=["coding", "chat", "analysis", "writing"],
        ),
        ModelInfo(
            id="openai/gpt-4o",
            name="GPT-4o",
            provider="OpenAI",
            description="Fast and capable multimodal model",
            context_window=128000,
            max_output_tokens=4096,
            input_cost_per_token=0.000005,
            output_cost_per_token=0.000015,
            capabilities=["vision", "function_calling"],
            recommended_for=["chat", "vision", "multilingual"],
        ),
        ModelInfo(
            id="google/gemini-pro-1.5",
            name="Gemini 1.5 Pro",
            provider="Google",
            description="Largest context window with strong reasoning",
            context_window=1048576,
            max_output_tokens=8192,
            input_cost_per_token=0.0000035,
            output_cost_per_token=0.0000105,
            capabilities=["vision", "long_context"],
            recommended_for=["analysis", "summarization", "research"],
        ),
        ModelInfo(
            id="meta-llama/llama-3.1-405b-instruct",
            name="Llama 3.1 405B",
            provider="Meta",
            description="Most powerful open source model",
            context_window=128000,
            max_output_tokens=4096,
            input_cost_per_token=0.000005,
            output_cost_per_token=0.000005,
            capabilities=["function_calling", "reasoning"],
            recommended_for=["coding", "analysis", "open_source"],
        ),
        ModelInfo(
            id="mistralai/mistral-large-2411",
            name="Mistral Large",
            provider="Mistral",
            description="European model with multilingual excellence",
            context_window=128000,
            max_output_tokens=8192,
            input_cost_per_token=0.000004,
            output_cost_per_token=0.000012,
            capabilities=["function_calling", "multilingual"],
            recommended_for=["multilingual", "coding", "european"],
        ),
    ],
)

# ============================================================================
# Anthropic - 5 Models
# ============================================================================
ANTHROPIC_MODELS = ProviderModelPicker(
    provider_id="anthropic",
    provider_name="Anthropic",
    default_model="claude-sonnet-4-20250514",
    models=[
        ModelInfo(
            id="claude-sonnet-4-20250514",
            name="Claude Sonnet 4",
            provider="Anthropic",
            description="Latest Sonnet with balanced performance",
            context_window=200000,
            max_output_tokens=8192,
            input_cost_per_token=0.000003,
            output_cost_per_token=0.000015,
            capabilities=["vision", "function_calling", "reasoning"],
            recommended_for=["coding", "chat", "analysis"],
        ),
        ModelInfo(
            id="claude-opus-4-20250514",
            name="Claude Opus 4",
            provider="Anthropic",
            description="Most powerful for complex tasks",
            context_window=200000,
            max_output_tokens=8192,
            input_cost_per_token=0.000015,
            output_cost_per_token=0.000075,
            capabilities=["vision", "function_calling", "reasoning"],
            recommended_for=["analysis", "research", "complex_tasks"],
        ),
        ModelInfo(
            id="claude-3-5-haiku-20241022",
            name="Claude 3.5 Haiku",
            provider="Anthropic",
            description="Fast and cost-effective",
            context_window=200000,
            max_output_tokens=8192,
            input_cost_per_token=0.000001,
            output_cost_per_token=0.000005,
            capabilities=["vision", "function_calling"],
            recommended_for=["chat", "cost_effective", "fast_response"],
        ),
        ModelInfo(
            id="claude-3-haiku-20240307",
            name="Claude Haiku 3",
            provider="Anthropic",
            description="Ultra-fast for simple tasks",
            context_window=200000,
            max_output_tokens=4096,
            input_cost_per_token=0.00000025,
            output_cost_per_token=0.00000125,
            capabilities=["vision", "function_calling"],
            recommended_for=["chat", "simple_tasks", "batch_processing"],
        ),
        ModelInfo(
            id="claude-3-opus-20240229",
            name="Claude Opus 3",
            provider="Anthropic",
            description="Previous generation flagship",
            context_window=200000,
            max_output_tokens=4096,
            input_cost_per_token=0.000015,
            output_cost_per_token=0.000075,
            capabilities=["vision", "function_calling", "reasoning"],
            recommended_for=["analysis", "legacy_support"],
        ),
    ],
)

# ============================================================================
# OpenAI - 5 Models
# ============================================================================
OPENAI_MODELS = ProviderModelPicker(
    provider_id="openai",
    provider_name="OpenAI",
    default_model="gpt-4.1",
    models=[
        ModelInfo(
            id="gpt-4.1",
            name="GPT-4.1",
            provider="OpenAI",
            description="Latest GPT-4 with improved capabilities",
            context_window=128000,
            max_output_tokens=4096,
            input_cost_per_token=0.000005,
            output_cost_per_token=0.000015,
            capabilities=["vision", "function_calling", "reasoning"],
            recommended_for=["coding", "chat", "analysis"],
        ),
        ModelInfo(
            id="gpt-4o",
            name="GPT-4o",
            provider="OpenAI",
            description="Fast multimodal flagship",
            context_window=128000,
            max_output_tokens=4096,
            input_cost_per_token=0.000005,
            output_cost_per_token=0.000015,
            capabilities=["vision", "function_calling"],
            recommended_for=["vision", "chat", "multilingual"],
        ),
        ModelInfo(
            id="gpt-4o-mini",
            name="GPT-4o Mini",
            provider="OpenAI",
            description="Cost-effective with strong performance",
            context_window=128000,
            max_output_tokens=4096,
            input_cost_per_token=0.00000015,
            output_cost_per_token=0.0000006,
            capabilities=["vision", "function_calling"],
            recommended_for=["chat", "cost_effective", "high_volume"],
        ),
        ModelInfo(
            id="o1",
            name="o1",
            provider="OpenAI",
            description="Advanced reasoning model",
            context_window=128000,
            max_output_tokens=4096,
            input_cost_per_token=0.000015,
            output_cost_per_token=0.00006,
            capabilities=["reasoning", "math", "science"],
            recommended_for=["reasoning", "math", "science", "complex_tasks"],
        ),
        ModelInfo(
            id="o3-mini",
            name="o3 Mini",
            provider="OpenAI",
            description="Fast reasoning model",
            context_window=128000,
            max_output_tokens=4096,
            input_cost_per_token=0.0000011,
            output_cost_per_token=0.0000044,
            capabilities=["reasoning", "coding"],
            recommended_for=["coding", "reasoning", "cost_effective"],
        ),
    ],
)

# ============================================================================
# Google - 5 Models
# ============================================================================
GOOGLE_MODELS = ProviderModelPicker(
    provider_id="google",
    provider_name="Google",
    default_model="gemini-2.5-pro",
    models=[
        ModelInfo(
            id="gemini-2.5-pro",
            name="Gemini 2.5 Pro",
            provider="Google",
            description="Latest Pro model with advanced reasoning",
            context_window=1048576,
            max_output_tokens=8192,
            input_cost_per_token=0.0000035,
            output_cost_per_token=0.0000105,
            capabilities=["vision", "long_context", "reasoning"],
            recommended_for=["analysis", "research", "multimodal"],
        ),
        ModelInfo(
            id="gemini-2.5-flash",
            name="Gemini 2.5 Flash",
            provider="Google",
            description="Fast and efficient model",
            context_window=1048576,
            max_output_tokens=8192,
            input_cost_per_token=0.0000003,
            output_cost_per_token=0.0000012,
            capabilities=["vision", "long_context"],
            recommended_for=["chat", "cost_effective", "high_volume"],
        ),
        ModelInfo(
            id="gemini-2.0-flash",
            name="Gemini 2.0 Flash",
            provider="Google",
            description="Previous generation fast model",
            context_window=1048576,
            max_output_tokens=8192,
            input_cost_per_token=0.00000015,
            output_cost_per_token=0.0000006,
            capabilities=["vision"],
            recommended_for=["chat", "legacy_support"],
        ),
        ModelInfo(
            id="gemini-2.0-flash-lite",
            name="Gemini 2.0 Flash Lite",
            provider="Google",
            description="Most cost-effective Google model",
            context_window=1048576,
            max_output_tokens=8192,
            input_cost_per_token=0.000000075,
            output_cost_per_token=0.0000003,
            capabilities=["vision"],
            recommended_for=["cost_effective", "batch_processing"],
        ),
        ModelInfo(
            id="gemini-1.5-pro",
            name="Gemini 1.5 Pro",
            provider="Google",
            description="Previous Pro with large context",
            context_window=1048576,
            max_output_tokens=8192,
            input_cost_per_token=0.0000035,
            output_cost_per_token=0.0000105,
            capabilities=["vision", "long_context"],
            recommended_for=["analysis", "legacy_support"],
        ),
    ],
)

# ============================================================================
# DeepSeek - 5 Models
# ============================================================================
DEEPSEEK_MODELS = ProviderModelPicker(
    provider_id="deepseek",
    provider_name="DeepSeek",
    default_model="deepseek-chat",
    models=[
        ModelInfo(
            id="deepseek-chat",
            name="DeepSeek Chat",
            provider="DeepSeek",
            description="Best for conversational tasks",
            context_window=128000,
            max_output_tokens=8192,
            input_cost_per_token=0.00000027,
            output_cost_per_token=0.0000011,
            capabilities=["function_calling", "coding"],
            recommended_for=["chat", "coding", "cost_effective"],
        ),
        ModelInfo(
            id="deepseek-coder",
            name="DeepSeek Coder",
            provider="DeepSeek",
            description="Specialized for code generation",
            context_window=128000,
            max_output_tokens=8192,
            input_cost_per_token=0.00000027,
            output_cost_per_token=0.0000011,
            capabilities=["coding", "function_calling"],
            recommended_for=["coding", "code_review", "debugging"],
        ),
        ModelInfo(
            id="deepseek-reasoner",
            name="DeepSeek Reasoner",
            provider="DeepSeek",
            description="Enhanced reasoning capabilities",
            context_window=64000,
            max_output_tokens=8192,
            input_cost_per_token=0.00000055,
            output_cost_per_token=0.0000022,
            capabilities=["reasoning", "math"],
            recommended_for=["reasoning", "math", "analysis"],
        ),
        ModelInfo(
            id="deepseek-v3",
            name="DeepSeek V3",
            provider="DeepSeek",
            description="Latest general purpose model",
            context_window=128000,
            max_output_tokens=8192,
            input_cost_per_token=0.00000027,
            output_cost_per_token=0.0000011,
            capabilities=["function_calling", "vision"],
            recommended_for=["chat", "analysis", "multimodal"],
        ),
        ModelInfo(
            id="deepseek-v2.5",
            name="DeepSeek V2.5",
            provider="DeepSeek",
            description="Previous generation balanced model",
            context_window=128000,
            max_output_tokens=8192,
            input_cost_per_token=0.00000014,
            output_cost_per_token=0.00000056,
            capabilities=["function_calling"],
            recommended_for=["cost_effective", "legacy_support"],
        ),
    ],
)


# ============================================================================
# All Model Pickers
# ============================================================================
MODEL_PICKERS: Dict[str, ProviderModelPicker] = {
    "openrouter": OPENROUTER_MODELS,
    "anthropic": ANTHROPIC_MODELS,
    "openai": OPENAI_MODELS,
    "google": GOOGLE_MODELS,
    "deepseek": DEEPSEEK_MODELS,
}


# ============================================================================
# Helper Functions for Tauri Integration
# ============================================================================

def get_model_picker(provider_id: str) -> Optional[ProviderModelPicker]:
    """Get model picker for a provider."""
    return MODEL_PICKERS.get(provider_id)


def get_model_ids(provider_id: str) -> List[str]:
    """Get list of model IDs for a provider (exactly 5)."""
    picker = get_model_picker(provider_id)
    if not picker:
        return []
    return [model.id for model in picker.models]


def get_default_model(provider_id: str) -> Optional[str]:
    """Get default model for a provider."""
    picker = get_model_picker(provider_id)
    if not picker:
        return None
    return picker.default_model


def get_models_array(provider_id: str) -> List[dict]:
    """
    Get models as array of dicts for Tauri/JSON serialization.
    Returns exactly 5 models.
    """
    picker = get_model_picker(provider_id)
    if not picker:
        return []
    return [model.model_dump() for model in picker.models]


def get_all_providers_info() -> List[dict]:
    """Get all providers with their model counts for Tauri."""
    return [
        {
            "provider_id": picker.provider_id,
            "provider_name": picker.provider_name,
            "model_count": len(picker.models),
            "default_model": picker.default_model,
        }
        for picker in MODEL_PICKERS.values()
    ]


# Export for Tauri commands
__all__ = [
    "ModelInfo",
    "ProviderModelPicker",
    "MODEL_PICKERS",
    "get_model_picker",
    "get_model_ids",
    "get_default_model",
    "get_models_array",
    "get_all_providers_info",
    "OPENROUTER_MODELS",
    "ANTHROPIC_MODELS",
    "OPENAI_MODELS",
    "GOOGLE_MODELS",
    "DEEPSEEK_MODELS",
]
