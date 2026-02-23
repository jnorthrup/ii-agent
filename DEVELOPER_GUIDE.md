# II-Agent Developer Guide

This guide covers how to set up `ii-agent` locally and how to work on your own agents and tools.

## Local Setup (No Docker/gcloud)

The project uses `uv` for lightning-fast dependency management.

1. **Install uv**:

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2. **Sync Dependencies**:

    ```bash
    uv sync
    ```

3. **Configure Environment**:
    Create a `.env` file in the root directory:

    ```bash
    ANTHROPIC_API_KEY=your_key_here
    # Optional: for local LLMs via LMStudio
    # OPENAI_BASE_URL="http://localhost:1234/v1"
    # OPENAI_API_KEY="lmstudio"
    ```

4. **Run with Single User Harness (CLI)**:

    ```bash
    python cli.py --prompt "Create a simple python script that prints hello world"
    ```

## Development Workflow

### Adding New Tools

Tools are located in `src/ii_agent/tools`.

- Each tool should inherit from `LLMTool` or `BaseTool`.
- Add your tool to the desired list in `src/ii_agent/tools/tool_manager.py`.

### Working on Agents

Agents are located in `src/ii_agent/agents`.

- The `FunctionCallAgent` is the primary general-purpose agent.
- You can create specialized agents by inheriting from `BaseAgent`.

### Using Tart Sandbox (macOS)

If you are on macOS and want isolated VM execution:

1. Install [Tart](https://tart.run).
2. Run the CLI with `--mode tart`.

    ```bash
    python cli.py --mode tart --prompt "Check the system uptime"
    ```

    *Note: Requires a base image named `macos-sequoia` in Tart.*

## Architecture Overview

- **`src/ii_agent/llm`**: LLM client implementations (Anthropic, OpenAI, Gemini).
- **`src/ii_agent/sandbox`**: Execution environment isolation (Local, Docker, E2B, Tart).
- **`src/ii_agent/prompts`**: System prompt management and builders.
