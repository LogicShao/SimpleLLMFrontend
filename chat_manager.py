"""
聊天管理模块 - 管理对话历史和消息处理
支持Gradio messages格式
"""

from typing import List, Dict, Any


class ChatManager:
    """聊天管理器"""

    def __init__(self):
        self.history = []

    def add_message(self, role: str, content: str):
        """添加消息到历史"""
        self.history.append({"role": role, "content": content})

    def get_messages_for_api(self) -> List[Dict[str, str]]:
        """获取用于API调用的消息格式"""
        return self.history.copy()

    def get_gradio_messages(self) -> List[Dict[str, Any]]:
        """获取Gradio messages格式的消息"""
        gradio_messages = []
        for msg in self.history:
            if msg["role"] == "user":
                gradio_messages.append({
                    "role": "user",
                    "content": msg["content"]
                })
            elif msg["role"] == "assistant":
                gradio_messages.append({
                    "role": "assistant",
                    "content": msg["content"]
                })
        return gradio_messages

    def clear_history(self):
        """清空对话历史"""
        self.history.clear()

    def get_history_length(self) -> int:
        """获取历史消息数量"""
        return len(self.history)


class MessageProcessor:
    """消息处理器"""

    @staticmethod
    def convert_to_api_messages(gradio_messages: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """将Gradio messages格式转换为API消息格式"""
        api_messages = []
        for msg in gradio_messages:
            if msg["role"] in ["user", "assistant"]:
                api_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        return api_messages

    @staticmethod
    def convert_from_api_messages(api_messages: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """将API消息格式转换为Gradio messages格式"""
        gradio_messages = []
        for msg in api_messages:
            if msg["role"] in ["user", "assistant"]:
                gradio_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        return gradio_messages

    @staticmethod
    def extract_user_messages(gradio_messages: List[Dict[str, Any]]) -> List[str]:
        """从Gradio消息中提取用户消息"""
        return [msg["content"] for msg in gradio_messages if msg["role"] == "user"]

    @staticmethod
    def extract_assistant_messages(gradio_messages: List[Dict[str, Any]]) -> List[str]:
        """从Gradio消息中提取助手消息"""
        return [msg["content"] for msg in gradio_messages if msg["role"] == "assistant"]
