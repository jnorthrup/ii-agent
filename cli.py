import argparse
import asyncio
import logging
import os
import uuid
from typing import List, Dict, Any

from dotenv import load_dotenv
from pydantic import SecretStr

from ii_agent.agents.function_call import FunctionCallAgent
from ii_agent.core.config.llm_config import APITypes, LLMConfig
from ii_agent.core.storage.models.settings import Settings, SandboxConfig
from ii_agent.core.config.client_config import ClientConfig
from ii_agent.llm import get_client
from ii_agent.llm.message_history import MessageHistory
from ii_agent.prompts.system_prompt import SystemPromptBuilder
from ii_agent.tools.tool_manager import get_system_tools
from ii_agent.utils.constants import WorkSpaceMode
from ii_agent.utils.workspace_manager import WorkspaceManager
from ii_agent.utils.sandbox_manager import SandboxManager

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ii-agent-cli")

async def run_cli(prompt: str, mode: WorkSpaceMode, model: str):
    # 1. Setup Config
    # Detect provider properly, avoiding placeholders
    def get_valid_env(key):
        val = os.getenv(key)
        if val and not val.endswith("-your-key-here"):
            return val
        return None

    anthropic_key = get_valid_env("ANTHROPIC_API_KEY")
    openai_key = get_valid_env("OPENAI_API_KEY")
    gemini_key = get_valid_env("GEMINI_API_KEY")

    api_key = anthropic_key or openai_key or gemini_key
    api_type = APITypes.ANTHROPIC
    
    if openai_key and not anthropic_key:
        api_type = APITypes.OPENAI
    elif gemini_key and not anthropic_key and not openai_key:
        api_type = APITypes.GEMINI
    elif anthropic_key:
        api_type = APITypes.ANTHROPIC

    # If model is the default, try to get from env first
    env_model = os.getenv("LLM_CONFIGS__default__model") or os.getenv("LLM_CONFIGS__anthropic__model")
    effective_model = model if model != "claude-3-5-sonnet-latest" or not env_model else env_model

    llm_config = LLMConfig(
        model=effective_model,
        api_key=SecretStr(api_key) if api_key else None,
        api_type=api_type,
        base_url=os.getenv("OPENAI_BASE_URL")
    )

    # 2. Initialize Components
    client = get_client(llm_config)
    system_prompt_builder = SystemPromptBuilder(workspace_mode=mode, sequential_thinking=False)
    
    session_id_uuid = uuid.uuid4()
    session_id = str(session_id_uuid)
    
    from ii_agent.core.config.search_config import SearchConfig
    from ii_agent.core.config.media_config import MediaConfig
    from ii_agent.core.config.audio_config import AudioConfig
    from ii_agent.core.config.database_config import ThirdPartyIntegrationConfig

    settings = Settings(
        sandbox_config=SandboxConfig(mode=mode),
        client_config=ClientConfig(mode=mode.value if mode != WorkSpaceMode.TART else "remote"),
        search_config=SearchConfig(),
        media_config=MediaConfig(),
        audio_config=AudioConfig(),
        third_party_integration_config=ThirdPartyIntegrationConfig()
    )
    
    sandbox_manager = SandboxManager(session_id_uuid, settings)
    
    print(f"[*] Starting sandbox in {mode} mode...")
    await sandbox_manager.start_sandbox()
    
    # Update settings with sandbox host url
    host_url = sandbox_manager.get_host_url()
    if settings.client_config:
        settings.client_config.server_url = host_url
        print(f"[*] Sandbox host URL: {host_url}")

    workspace_root = os.getenv("WORKSPACE_ROOT", "./data/workspace")
    workspace_manager = WorkspaceManager(workspace_root, session_id, settings)
    
    message_queue = asyncio.Queue()
    agent_logger = logging.getLogger(f"agent-{session_id}")
    
    # Correct signature for get_system_tools
    tools = get_system_tools(
        client=client,
        workspace_manager=workspace_manager,
        sandbox_manager=sandbox_manager,
        message_queue=message_queue,
        system_prompt_builder=system_prompt_builder,
        settings=settings
    )
    
    from ii_agent.llm.context_manager.llm_summarizing import LLMSummarizingContextManager
    from ii_agent.llm.token_counter import TokenCounter
    from ii_agent.utils.constants import TOKEN_BUDGET
    
    context_manager = LLMSummarizingContextManager(
        client=client,
        token_counter=TokenCounter(),
        logger=logger,
        token_budget=TOKEN_BUDGET,
    )
    history = MessageHistory(context_manager=context_manager)
    
    agent = FunctionCallAgent(
        system_prompt_builder=system_prompt_builder,
        client=client,
        tools=tools,
        init_history=history,
        workspace_manager=workspace_manager,
        message_queue=message_queue,
        logger_for_agent_logs=agent_logger,
        interactive_mode=False
    )

    # 3. Start processing events (background)
    processing_task = agent.start_message_processing()

    # 4. Run Agent
    print(f"\n[Agent] Instruction: {prompt}")
    print("-" * 50)
    
    try:
        result = await agent.run_agent_async(instruction=prompt)
        print("-" * 50)
        print(f"[Agent Result] {result}")
    except Exception as e:
        print(f"[!] Error during agent execution: {e}")
    finally:
        # Cleanup
        processing_task.cancel()
        print("[*] Cleaning up sandbox...")
        await sandbox_manager.cleanup_sandbox()

def main():
    parser = argparse.ArgumentParser(description="II-Agent Single User Harness (CLI)")
    parser.add_argument("--prompt", type=str, required=True, help="Instruction for the agent")
    parser.add_argument("--mode", type=str, choices=["local", "docker", "e2b", "tart"], default="local", help="Sandbox mode")
    parser.add_argument("--model", type=str, default="claude-3-5-sonnet-latest", help="LLM model name")
    
    args = parser.parse_args()
    
    mode = WorkSpaceMode(args.mode)
    asyncio.run(run_cli(args.prompt, mode, args.model))

if __name__ == "__main__":
    main()
