import logging
import httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("local_proxy")

app = FastAPI(title="II-Agent OpenRouter Proxy")

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

@app.get("/v1/models")
async def list_models(request: Request):
    """
    Proxies the models list from OpenRouter.
    This facilitates the 'Auto-discover' feature in II-Agent.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    logger.info("Fetching models from OpenRouter...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{OPENROUTER_BASE_URL}/models",
                headers={"Authorization": auth_header}
            )
            response.raise_for_status()
            data = response.json()
            
            # Simple transformation if needed, but II-Agent expects standard OpenAI format
            # OpenRouter returns { "data": [...] } which is correct.
            return JSONResponse(content=data)
        except httpx.HTTPStatusError as e:
            logger.error(f"Error fetching models: {e}")
            return JSONResponse(status_code=e.response.status_code, content=e.response.json())
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    """
    Proxies chat completion requests to OpenRouter.
    """
    auth_header = request.headers.get("Authorization")
    body = await request.json()
    
    logger.info(f"Proxying chat completion for model: {body.get('model')}")
    
    async with httpx.AsyncClient() as client:
        try:
            # Note: We stream if the request asks for it, but for simplicity here we handle non-streaming
            # If the agent uses streaming, we would need to stream the response back.
            # OpenRouter's API is mostly OpenAI compatible.
            response = await client.post(
                f"{OPENROUTER_BASE_URL}/chat/completions",
                headers={
                    "Authorization": auth_header,
                    "HTTP-Referer": "http://localhost:3000", # Required by OpenRouter
                    "X-Title": "II-Agent Benchmark"
                },
                json=body,
                timeout=None
            )
            response.raise_for_status()
            return JSONResponse(content=response.json())
        except httpx.HTTPStatusError as e:
            logger.error(f"Error in chat completion: {e}")
            return JSONResponse(status_code=e.response.status_code, content=e.response.json())
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
async def catch_all(request: Request, path: str):
    """
    Catch-all for other OpenAI-compatible endpoints.
    """
    logger.info(f"Catch-all for path: {path}")
    return JSONResponse(content={"message": "Not implemented in local proxy", "path": path}, status_code=501)

if __name__ == "__main__":
    print(__doc__)
    uvicorn.run(app, host="0.0.0.0", port=8081)

"""
# Local Proxy for II-Agent Benchmark
----------------------------------
This script provides a local OpenAI-compatible proxy that routes requests to OpenRouter.
It specifically implements the /v1/models endpoint to facilitate model discovery in II-Agent.

## Self-Documentation:
1.  **Dependencies**: Requires `fastapi`, `uvicorn`, and `httpx`.
    `pip install fastapi uvicorn httpx`
2.  **Running**:
    `python scripts/local_proxy.py`
3.  **II-Agent Configuration**:
    - **Provider**: OpenAI
    - **Base URL**: `http://localhost:8081/v1`
    - **API Key**: Use your OpenRouter API Key.
4.  **Feature Demo**:
    - Go to Settings -> API Keys.
    - Add or Edit an OpenAI config.
    - Set Base URL to `http://localhost:8081/v1`.
    - Click **"Auto-discover Models from Proxy"**.
    - Watch it fetch the models from OpenRouter through this script!
"""
