"""
配置模块 - 管理应用配置、提供商和模型列表
"""

import os

from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 提供商配置
PROVIDER_CONFIG = {
    "cerebras": {
        "api_key": os.environ.get("CEREBRAS_API_KEY"),
        "base_url": "https://api.cerebras.ai",
        "enabled": True
    },
    "deepseek": {
        "api_key": os.environ.get("DEEPSEEK_API_KEY"),
        "base_url": "https://api.deepseek.com",
        "enabled": True
    },
    "openai": {
        "api_key": os.environ.get("OPENAI_API_KEY"),
        "base_url": "https://api.openai.com/v1",
        "enabled": True
    }
}

# 提供商支持的模型映射
PROVIDER_MODELS = {
    "cerebras": [
        # Llama系列
        "llama-3.3-70b",
        "llama-3.1-8b",
        "llama-3.1-70b",
        "llama-3.2-3b",
        "llama-3.2-1b",

        # 其他模型
        "qwen-3-235b-a22b-instruct-2507",
        "qwen-3-235b-a22b-thinking-2507",
        "zai-glm-4.6",
        "gpt-oss-120b",
        "qwen-3-32b"
    ],
    "deepseek": [
        "deepseek-chat",
        "deepseek-coder",
        "deepseek-reasoner"
    ],
    "openai": [
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4-turbo",
        "gpt-3.5-turbo"
    ]
}

# 默认提供商和模型
DEFAULT_PROVIDER = "cerebras"
DEFAULT_MODEL = "qwen-3-235b-a22b-thinking-2507"

# 服务器配置
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 7860

# 界面配置
CHATBOT_HEIGHT = 500
MAX_INPUT_LINES = 5


# 获取所有支持的模型
def get_supported_models():
    """获取所有启用的提供商支持的模型列表"""
    all_models = []
    for provider, config in PROVIDER_CONFIG.items():
        if config["enabled"] and config["api_key"]:
            all_models.extend(PROVIDER_MODELS.get(provider, []))
    return all_models


# 获取启用的提供商列表
def get_enabled_providers():
    """获取已配置且启用的提供商列表"""
    enabled_providers = []
    for provider, config in PROVIDER_CONFIG.items():
        if config["enabled"] and config["api_key"]:
            enabled_providers.append(provider)
    return enabled_providers


# 检查API密钥配置
def check_api_key(provider=None):
    """
    检查API密钥是否配置

    Args:
        provider: 指定提供商，None表示检查所有提供商

    Returns:
        bool: 是否至少有一个提供商配置了API密钥
    """
    if provider:
        config = PROVIDER_CONFIG.get(provider, {})
        if not config.get("api_key"):
            print(f"警告: {provider.upper()}_API_KEY 环境变量未设置")
            print(f"请创建.env文件并添加: {provider.upper()}_API_KEY=your_api_key_here")
            return False
        return True

    # 检查所有提供商
    has_valid_provider = False
    for provider, config in PROVIDER_CONFIG.items():
        if config["enabled"] and config["api_key"]:
            has_valid_provider = True
            break

    if not has_valid_provider:
        print("警告: 没有配置任何有效的API密钥")
        print("请至少配置以下环境变量之一:")
        for provider in PROVIDER_CONFIG:
            print(f"  - {provider.upper()}_API_KEY")
        return False

    return True


# 获取提供商配置
def get_provider_config(provider):
    """获取指定提供商的配置"""
    return PROVIDER_CONFIG.get(provider, {})


# 获取模型对应的提供商
def get_model_provider(model):
    """根据模型名称获取对应的提供商"""
    for provider, models in PROVIDER_MODELS.items():
        if model in models:
            return provider
    return None
