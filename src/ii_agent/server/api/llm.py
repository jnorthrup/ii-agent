from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from pydantic import SecretStr

from ii_agent.core.config.llm_config import APITypes, LLMConfig
from ii_agent.llm.openai import OpenAIDirectClient

llm_router = APIRouter(prefix="/api/llm", tags=["llm"])

@llm_router.get("/models")
async def list_models(
    provider: str = Query(...),
    api_key: Optional[str] = Query(None),
    base_url: Optional[str] = Query(None),
):
    """List models for a given provider and base_url."""
    if provider != "openai":
        # Currently only OpenAI-compatible proxies support model listing via /v1/models in this context
        return []

    try:
        config = LLMConfig(
            api_type=APITypes.OPENAI,
            api_key=SecretStr(api_key) if api_key else None,
            base_url=base_url,
            model="placeholder", # Not needed for listing
        )
        client = OpenAIDirectClient(config)
        models = client.list_models()
        return models
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
