# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a multi-provider LLM chat client built with Gradio that supports multiple AI providers including Cerebras,
DeepSeek, and OpenAI. The application provides a web-based interface for interacting with various large language models
through a unified interface.

## Architecture

### Core Components

- **MultiProviderAPIService** (`api_service.py`): Central service that manages multiple AI providers and routes requests
  based on model selection
- **Provider Factory Pattern** (`providers.py`): Abstract factory pattern for creating and managing different AI
  provider instances
- **Configuration Management** (`config.py`): Centralized configuration for providers, models, and API settings
- **Chat Management** (`chat_manager.py`): Handles conversation history and message format conversion between Gradio and
  API formats
- **Gradio Interface** (`main.py`): Web-based UI built with Gradio for user interaction

### Provider Architecture

The system uses an abstract `BaseProvider` class that all concrete providers implement:

- `CerebrasProvider`: Uses Cerebras Cloud SDK for Cerebras models
- `DeepSeekProvider`: Uses OpenAI SDK with DeepSeek's base URL
- `OpenAIProvider`: Uses OpenAI SDK for OpenAI models

Each provider implements the same interface (`is_available()`, `chat_completion()`) allowing seamless switching between
providers.

### Model-Provider Mapping

Models are automatically mapped to their respective providers:

- Cerebras models: llama-3.x, qwen-3.x, zai-glm-4.6, gpt-oss-120b
- DeepSeek models: deepseek-chat, deepseek-coder, deepseek-reasoner
- OpenAI models: gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-3.5-turbo

## Development Commands

### Setup and Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template and configure API keys
cp .env.example .env
# Edit .env file with your API keys
```

### Running the Application

```bash
# Start the Gradio web interface
python main.py
```

## Configuration

### Environment Variables

Configure API keys in `.env` file:

- `CEREBRAS_API_KEY`: For Cerebras models (https://cloud.cerebras.ai/)
- `DEEPSEEK_API_KEY`: For DeepSeek models (https://platform.deepseek.com/)
- `OPENAI_API_KEY`: For OpenAI models (https://platform.openai.com/)

At least one provider API key must be configured for the application to function.

### Provider Configuration

Providers are configured in `config.py`:

- Each provider has `api_key`, `base_url`, and `enabled` settings
- Provider-specific models are defined in `PROVIDER_MODELS`
- Default provider and model can be changed in configuration

## Key Implementation Patterns

### Message Format Conversion

The system handles two message formats:

- **API Format**: Standard OpenAI-compatible format for provider APIs
- **Gradio Format**: Gradio's messages format for UI display

`MessageProcessor` handles conversion between these formats automatically.

### Error Handling

- Providers gracefully handle missing API keys
- Clear error messages indicate which provider is unavailable
- Failed API calls return descriptive error messages

### State Management

- `ChatManager` maintains conversation history
- Provider status is monitored and displayed in real-time
- Conversation history can be cleared or exported

## Adding New Providers

To add a new AI provider:

1. Create a new provider class inheriting from `BaseProvider`
2. Implement `_initialize_client()`, `is_available()`, and `chat_completion()` methods
3. Register the provider in `ProviderFactory._providers`
4. Add provider configuration to `PROVIDER_CONFIG` in `config.py`
5. Define supported models in `PROVIDER_MODELS`

The factory pattern ensures new providers integrate seamlessly without modifying existing code.