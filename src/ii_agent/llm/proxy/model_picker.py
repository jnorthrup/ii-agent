"""
Model Picker Configuration for II-Agent

This module provides predefined model lists for popular providers like OpenRouter.
Each provider has 4-5 recommended models for different use cases.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel


class ModelInfo(BaseModel):
    """Information about a model."""
    id: str
    name: str
    provider: str
    description: str
    context_window: int
    max_output_tokens: int
    input_cost_per_token: float = 0.0
    output_cost_per_token: float = 0.0
    capabilities: List[str] = []  # e.g., ["vision", "function_calling", "reasoning"]
    recommended_for: List[str] = []  # e.g., ["coding", "chat", "analysis"]


class ProviderModelPicker(BaseModel):
    """Model picker configuration for a provider."""
    provider_id: str
    provider_name: str
    models: List[ModelInfo]
    default_model: str


# Predefined model pickers for popular providers
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
            description="Large context window with strong reasoning",
            context_window=1048576,
            max_output_tokens=8192,
            input_cost_per_token=0.0000035,
            output_cost_per_token=0.0000105,
            capabilities=["vision", "long_context"],
            recommended_for=["analysis", "summarization", "research"],
        ),
        ModelInfo(
            id="meta-llama/llama-3-70b-instruct",
            name="Llama 3 70B",
            provider="Meta",
            description="Open source model with excellent performance",
            context_window=8192,
            max_output_tokens=4096,
            input_cost_per_token=0.0000008,
            output_cost_per_token=0.0000008,
            capabilities=["function_calling"],
            recommended_for=["coding", "chat", "cost_effective"],
        ),
        ModelInfo(
            id="mistralai/mistral-large",
            name="Mistral Large",
            provider="Mistral",
            description="European model with strong multilingual support",
            context_window=32000,
            max_output_tokens=8192,
            input_cost_per_token=0.000004,
            output_cost_per_token=0.000012,
            capabilities=["function_calling", "multilingual"],
            recommended_for=["multilingual", "coding", "analysis"],
        ),
    ],
)

ANTHROPIC_MODELS = ProviderModelPicker(
    provider_id="anthropic",
    provider_name="Anthropic",
    default_model="claude-sonnet-4-20250514",
    models=[
        ModelInfo(
            id="claude-sonnet-4-20250514",
            name="Claude Sonnet 4",
            provider="Anthropic",
            description="Latest Sonnet model with balanced performance",
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
            description="Most powerful model for complex tasks",
            context_window=200000,
            max_output_tokens=8192,
            input_cost_per_token=0.000015,
            output_cost_per_token=0.000075,
            capabilities=["vision", "function_calling", "reasoning"],
            recommended_for=["analysis", "research", "complex_tasks"],
        ),
        ModelInfo(
            id="claude-haiku-3-20240307",
            name="Claude Haiku 3",
            provider="Anthropic",
            description="Fast and cost-effective for simple tasks",
            context_window=200000,
            max_output_tokens=4096,
            input_cost_per_token=0.00000025,
            output_cost_per_token=0.00000125,
            capabilities=["vision", "function_calling"],
            recommended_for=["chat", "cost_effective", "simple_tasks"],
        ),
        ModelInfo(
            id="claude-3-5-haiku-20241022",
            name="Claude 3.5 Haiku",
            provider="Anthropic",
            description="Latest Haiku with improved capabilities",
            context_window=200000,
            max_output_tokens=8192,
            input_cost_per_token=0.000001,
            output_cost_per_token=0.000005,
            capabilities=["vision", "function_calling"],
            recommended_for=["chat", "cost_effective", "fast_response"],
        ),
    ],
)

OPENAI_MODELS = ProviderModelPicker(
    provider_id="openai",
    provider_name="OpenAI",
    default_model="gpt-4.1",
    models=[
        ModelInfo(
            id="gpt-4.1",
            name="GPT-4.1",
            provider="OpenAI",
            description="Latest GPT-4 model with improved capabilities",
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
            description="Fast multimodal model",
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
            recommended_for=["chat", "cost_effective", "simple_tasks"],
        ),
        ModelInfo(
            id="o1-preview",
            name="o1 Preview",
            provider="OpenAI",
            description="Reasoning model for complex problems",
            context_window=128000,
            max_output_tokens=4096,
            input_cost_per_token=0.000015,
            output_cost_per_token=0.00006,
            capabilities=["reasoning", "math", "science"],
            recommended_for=["reasoning", "math", "science", "complex_tasks"],
        ),
    ],
)


# All model pickers
MODEL_PICKERS: Dict[str, ProviderModelPicker] = {
    "openrouter": OPENROUTER_MODELS,
    "anthropic": ANTHROPIC_MODELS,
    "openai": OPENAI_MODELS,
}


def get_model_picker(provider_id: str) -> Optional[ProviderModelPicker]:
    """Get model picker for a provider."""
    return MODEL_PICKERS.get(provider_id)


def get_model_ids(provider_id: str) -> List[str]:
    """Get list of model IDs for a provider."""
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
