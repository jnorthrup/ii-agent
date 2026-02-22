#!/usr/bin/env python3
"""
Example usage of the ii-agent model proxy.

This script demonstrates how to use the model proxy to:
1. Add providers
2. Switch between providers
3. Create LLM clients
4. Enumerate models
"""

import asyncio
from pathlib import Path

from ii_agent.llm.proxy import (
    ProviderManager,
    Provider,
    ProviderCategory,
    ProviderMeta,
    ProviderProxyConfig,
    ModelProxyFactory,
    enumerate_models,
)


async def main():
    # Initialize the provider manager
    manager = ProviderManager()

    print("=== Model Proxy Example ===\n")

    # 1. Add providers
    print("1. Adding providers...")

    # Anthropic provider
    anthropic_provider = Provider(
        id="anthropic",
        name="Anthropic",
        settings_config={
            "api_key": "sk-ant-...",  # Replace with actual key
        },
        category=ProviderCategory.OFFICIAL,
        website_url="https://anthropic.com",
        icon="anthropic",
        icon_color="#D8A657",
    )
    success, message = manager.add_provider(anthropic_provider)
    print(f"   Anthropic: {message}")

    # OpenAI provider
    openai_provider = Provider(
        id="openai",
        name="OpenAI",
        settings_config={
            "api_key": "sk-...",  # Replace with actual key
        },
        category=ProviderCategory.OFFICIAL,
        website_url="https://openai.com",
        icon="openai",
        icon_color="#00A67E",
    )
    success, message = manager.add_provider(openai_provider)
    print(f"   OpenAI: {message}")

    # Custom provider with proxy
    custom_provider = Provider(
        id="custom-provider",
        name="Custom Provider",
        settings_config={
            "api_key": "sk-custom",
            "base_url": "https://api.custom-llm.com/v1",
        },
        category=ProviderCategory.CUSTOM,
        meta=ProviderMeta(
            api_format="openai_chat",
            proxy_config=ProviderProxyConfig(
                enabled=False,  # Set to True and configure if needed
                proxy_type="http",
                proxy_host="proxy.example.com",
                proxy_port=8080,
            ),
        ),
    )
    success, message = manager.add_provider(custom_provider)
    print(f"   Custom: {message}")

    # 2. List all providers
    print("\n2. All providers:")
    all_providers = manager.get_all_providers()
    for pid, provider in all_providers.items():
        current_marker = " (current)" if manager.get_current_provider("ii-agent") == provider else ""
        print(f"   - {provider.name} ({pid}){current_marker}")

    # 3. Switch provider
    print("\n3. Switching to Anthropic...")
    success, message = manager.switch_provider("anthropic", "ii-agent")
    print(f"   {message}")

    # 4. Create LLM client from provider
    print("\n4. Creating LLM client...")
    factory = ModelProxyFactory()
    try:
        client = factory.create_client(
            provider_id="anthropic",
            model="claude-sonnet-4-20250514",
        )
        print(f"   Created client for {client.model_name}")
    except Exception as e:
        print(f"   Note: {e}")

    # 5. Enumerate models (example with OpenAI)
    print("\n5. Enumerating models from OpenAI...")
    try:
        models = await enumerate_models(
            base_url="https://api.openai.com/v1",
            api_key="sk-...",  # Replace with actual key
            api_format="openai_chat",
        )
        print(f"   Found {len(models)} models:")
        for model in models[:5]:  # Show first 5
            print(f"     - {model.id}")
        if len(models) > 5:
            print(f"     ... and {len(models) - 5} more")
    except Exception as e:
        print(f"   Note: {e}")

    print("\n=== Example Complete ===")


if __name__ == "__main__":
    asyncio.run(main())
