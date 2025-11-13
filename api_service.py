"""
API服务模块 - 处理多提供商API调用
"""

from config import get_model_provider
from providers import ProviderFactory


class MultiProviderAPIService:
    """多提供商API服务类"""

    def __init__(self):
        self.providers = {}
        self._initialize_providers()

    def _initialize_providers(self):
        """初始化所有提供商"""
        available_providers = ProviderFactory.get_available_providers()

        for provider_name in available_providers:
            try:
                provider = ProviderFactory.create_provider(provider_name)
                if provider.is_available():
                    self.providers[provider_name] = provider
                    print(f"[SUCCESS] {provider_name} 提供商初始化成功")
                else:
                    print(f"[FAILED] {provider_name} 提供商初始化失败")
            except Exception as e:
                print(f"[ERROR] 初始化 {provider_name} 提供商时出错: {e}")

    def is_available(self, provider_name=None):
        """
        检查API服务是否可用

        Args:
            provider_name: 指定提供商，None表示检查是否有任何提供商可用

        Returns:
            bool: 服务是否可用
        """
        if provider_name:
            return provider_name in self.providers and self.providers[provider_name].is_available()

        # 检查是否有任何提供商可用
        return len(self.providers) > 0

    def get_available_providers(self):
        """获取可用的提供商列表"""
        return list(self.providers.keys())

    def chat_completion(self, messages, model):
        """
        调用聊天完成API

        Args:
            messages: 消息列表
            model: 模型名称

        Returns:
            str: API回复内容，或错误信息
        """
        # 根据模型确定提供商
        provider_name = get_model_provider(model)

        if not provider_name:
            return f"错误: 不支持模型 '{model}'。请检查模型名称是否正确。"

        if provider_name not in self.providers:
            return f"错误: 提供商 '{provider_name}' 未配置或不可用。请检查{provider_name.upper()}_API_KEY环境变量。"

        provider = self.providers[provider_name]

        if not provider.is_available():
            return f"错误: {provider_name} 提供商不可用。请检查配置。"

        try:
            return provider.chat_completion(messages, model)

        except Exception as e:
            error_msg = f"{provider_name} API调用失败: {str(e)}"
            print(error_msg)
            return error_msg

    def get_provider_status(self):
        """获取所有提供商的状态信息"""
        status_info = []
        for provider_name, provider in self.providers.items():
            status = "[OK] 可用" if provider.is_available() else "[FAIL] 不可用"
            status_info.append(f"{provider_name}: {status}")

        if not status_info:
            return "[FAIL] 没有可用的提供商"

        return " | ".join(status_info)


# 全局API服务实例
api_service = MultiProviderAPIService()
