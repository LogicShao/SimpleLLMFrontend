"""
提供商模块 - 定义AI提供商接口和具体实现
"""

from abc import ABC, abstractmethod
from typing import List, Dict

from cerebras.cloud.sdk import Cerebras
from openai import OpenAI

from config import get_provider_config


class BaseProvider(ABC):
    """AI提供商抽象基类"""

    def __init__(self, provider_name: str):
        self.provider_name = provider_name
        self.client = None
        self._initialize_client()

    @abstractmethod
    def _initialize_client(self):
        """初始化客户端"""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """检查提供商是否可用"""
        pass

    @abstractmethod
    def chat_completion(self, messages: List[Dict], model: str) -> str:
        """
        调用聊天完成API

        Args:
            messages: 消息列表
            model: 模型名称

        Returns:
            str: API回复内容，或错误信息
        """
        pass


class CerebrasProvider(BaseProvider):
    """Cerebras提供商实现"""

    def __init__(self):
        super().__init__("cerebras")

    def _initialize_client(self):
        """初始化Cerebras客户端"""
        config = get_provider_config(self.provider_name)
        api_key = config.get("api_key")

        if not api_key:
            return

        try:
            self.client = Cerebras(api_key=api_key)
        except Exception as e:
            print(f"初始化Cerebras客户端失败: {e}")

    def is_available(self) -> bool:
        """检查Cerebras服务是否可用"""
        return self.client is not None

    def chat_completion(self, messages: List[Dict], model: str) -> str:
        """调用Cerebras聊天完成API"""
        if not self.is_available():
            return f"错误: 无法初始化{self.provider_name}客户端。请检查{self.provider_name.upper()}_API_KEY环境变量。"

        try:
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=model,
            )
            return chat_completion.choices[0].message.content

        except Exception as e:
            error_msg = f"{self.provider_name} API调用失败: {str(e)}"
            print(error_msg)
            return error_msg


class DeepSeekProvider(BaseProvider):
    """DeepSeek提供商实现"""

    def __init__(self):
        super().__init__("deepseek")

    def _initialize_client(self):
        """初始化DeepSeek客户端"""
        config = get_provider_config(self.provider_name)
        api_key = config.get("api_key")
        base_url = config.get("base_url")

        if not api_key:
            return

        try:
            self.client = OpenAI(
                api_key=api_key,
                base_url=base_url
            )
        except Exception as e:
            print(f"初始化DeepSeek客户端失败: {e}")

    def is_available(self) -> bool:
        """检查DeepSeek服务是否可用"""
        return self.client is not None

    def chat_completion(self, messages: List[Dict], model: str) -> str:
        """调用DeepSeek聊天完成API"""
        if not self.is_available():
            return f"错误: 无法初始化{self.provider_name}客户端。请检查{self.provider_name.upper()}_API_KEY环境变量。"

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                stream=False
            )
            return response.choices[0].message.content

        except Exception as e:
            error_msg = f"{self.provider_name} API调用失败: {str(e)}"
            print(error_msg)
            return error_msg


class OpenAIProvider(BaseProvider):
    """OpenAI提供商实现"""

    def __init__(self):
        super().__init__("openai")

    def _initialize_client(self):
        """初始化OpenAI客户端"""
        config = get_provider_config(self.provider_name)
        api_key = config.get("api_key")
        base_url = config.get("base_url")

        if not api_key:
            return

        try:
            self.client = OpenAI(
                api_key=api_key,
                base_url=base_url
            )
        except Exception as e:
            print(f"初始化OpenAI客户端失败: {e}")

    def is_available(self) -> bool:
        """检查OpenAI服务是否可用"""
        return self.client is not None

    def chat_completion(self, messages: List[Dict], model: str) -> str:
        """调用OpenAI聊天完成API"""
        if not self.is_available():
            return f"错误: 无法初始化{self.provider_name}客户端。请检查{self.provider_name.upper()}_API_KEY环境变量。"

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                stream=False
            )
            return response.choices[0].message.content

        except Exception as e:
            error_msg = f"{self.provider_name} API调用失败: {str(e)}"
            print(error_msg)
            return error_msg


class ProviderFactory:
    """提供商工厂类"""

    _providers = {
        "cerebras": CerebrasProvider,
        "deepseek": DeepSeekProvider,
        "openai": OpenAIProvider
    }

    @classmethod
    def create_provider(cls, provider_name: str) -> BaseProvider:
        """
        创建提供商实例

        Args:
            provider_name: 提供商名称

        Returns:
            BaseProvider: 提供商实例
        """
        provider_class = cls._providers.get(provider_name)
        if not provider_class:
            raise ValueError(f"不支持的提供商: {provider_name}")

        return provider_class()

    @classmethod
    def get_available_providers(cls) -> List[str]:
        """获取可用的提供商列表"""
        from config import get_enabled_providers
        return get_enabled_providers()

    @classmethod
    def register_provider(cls, provider_name: str, provider_class):
        """注册新的提供商"""
        if not issubclass(provider_class, BaseProvider):
            raise ValueError("提供商类必须继承自BaseProvider")
        cls._providers[provider_name] = provider_class
