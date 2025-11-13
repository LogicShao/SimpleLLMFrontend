"""
多提供商 LLM 客户端 - 主应用文件
重构版本，支持多个AI提供商和更好的模块化
"""

import gradio as gr

from api_service import api_service
from chat_manager import ChatManager, MessageProcessor
from config import (
    get_supported_models, DEFAULT_MODEL, SERVER_HOST, SERVER_PORT,
    CHATBOT_HEIGHT, MAX_INPUT_LINES, check_api_key
)


class LLMClient:
    """LLM客户端主类"""

    def __init__(self):
        self.chat_manager = ChatManager()
        self.message_processor = MessageProcessor()

    def create_interface(self):
        """创建Gradio界面"""
        with gr.Blocks(
                title="Cerebras LLM 客户端",
                theme=gr.themes.Soft(),
                css=self._get_custom_css()
        ) as demo:
            # 标题和描述
            gr.Markdown(self._get_header_markdown())

            # 控制面板
            with gr.Row():
                with gr.Column(scale=1, elem_classes="control-panel"):
                    model_dropdown = gr.Dropdown(
                        choices=get_supported_models(),
                        value=DEFAULT_MODEL,
                        label="选择模型",
                        info="选择要使用的LLM模型"
                    )

                    # 状态面板
                    status_panel = gr.Textbox(
                        label="系统状态",
                        value=self._get_initial_status(),
                        interactive=False,
                        max_lines=3,
                        show_copy_button=False
                    )

                with gr.Column(scale=3, elem_classes="chat-area"):
                    # 聊天界面 - 使用新的messages格式
                    chatbot = gr.Chatbot(
                        label="对话界面",
                        height=CHATBOT_HEIGHT,
                        type="messages",  # 修复警告，使用新的messages格式
                        show_copy_button=True,
                        avatar_images=(
                            "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",  # 用户头像
                            "https://cdn-icons-png.flaticon.com/512/4712/4712035.png"  # AI头像
                        )
                    )

            # 输入区域
            with gr.Row():
                msg = gr.Textbox(
                    label="输入消息",
                    placeholder="请输入您的问题...",
                    scale=4,
                    max_lines=MAX_INPUT_LINES,
                    show_copy_button=False
                )
                submit_btn = gr.Button("发送", variant="primary", scale=1, size="lg")

            # 控制按钮
            with gr.Row():
                clear_btn = gr.Button("🗑️ 清除对话", variant="secondary")
                export_btn = gr.Button("📥 导出对话", variant="secondary")

            # 绑定事件
            self._setup_event_handlers(
                demo, msg, chatbot, model_dropdown,
                submit_btn, clear_btn, export_btn, status_panel
            )

        return demo

    def _get_custom_css(self):
        """获取自定义CSS样式"""
        return """
        .gradio-container {
            width: 100% !important;
            max-width: none !important;
            margin: 0 auto;
        }
        .container {
            padding: 20px;
        }
        .chat-container {
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 20px;
            background: #fafafa;
        }
        .control-panel {
            min-width: 250px;
            max-width: 300px;
        }
        .chat-area {
            min-width: 600px;
            flex-grow: 1;
        }
        @media (max-width: 1024px) {
            .control-panel {
                min-width: 200px;
                max-width: 250px;
            }
            .chat-area {
                min-width: 400px;
            }
        }
        @media (max-width: 768px) {
            .control-panel, .chat-area {
                min-width: unset;
                max-width: unset;
                width: 100%;
            }
        }
        """

    def _get_header_markdown(self):
        """获取头部Markdown内容"""
        return """
        # 🚀 多提供商 LLM 客户端

        一个专业的PC端LLM聊天客户端，支持多个AI提供商。

        **支持的提供商**: Cerebras、DeepSeek、OpenAI
        **默认模型**: Qwen-3-235B-A22B-Thinking-2507
        **支持的模型**: Llama系列、Qwen系列、DeepSeek系列、GPT系列等
        """

    def _get_initial_status(self):
        """获取初始状态信息"""
        return api_service.get_provider_status()

    def _setup_event_handlers(
            self, demo, msg, chatbot, model_dropdown,
            submit_btn, clear_btn, export_btn, status_panel
    ):
        """设置事件处理器"""

        def user_message(user_msg, history, model):
            """处理用户消息"""
            if not user_msg.strip():
                return "", history

            # 添加用户消息到历史
            self.chat_manager.add_message("user", user_msg)

            # 更新Gradio界面
            new_history = history + [{"role": "user", "content": user_msg}]
            return "", new_history

        def bot_message(history, model):
            """获取机器人回复"""
            if not history:
                return history

            # 构建API消息 - 直接使用Gradio的history格式
            api_messages = []
            for msg in history:
                if msg["role"] in ["user", "assistant"]:
                    api_messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })

            # 调用API
            response = api_service.chat_completion(api_messages, model)

            # 添加助手回复到历史
            self.chat_manager.add_message("assistant", response)

            # 更新Gradio界面
            history.append({"role": "assistant", "content": response})
            return history

        def clear_conversation():
            """清除对话"""
            self.chat_manager.clear_history()
            return [], "对话已清除"

        def export_conversation():
            """导出对话"""
            if not self.chat_manager.history:
                return "没有对话内容可导出"

            export_text = "Cerebras LLM 对话记录\n" + "=" * 50 + "\n"
            for msg in self.chat_manager.history:
                role = "用户" if msg["role"] == "user" else "助手"
                export_text += f"{role}: {msg['content']}\n\n"

            return export_text

        def update_status():
            """更新状态信息"""
            provider_status = api_service.get_provider_status()
            history_count = self.chat_manager.get_history_length()
            return f"{provider_status} | 对话数: {history_count}"

        # 绑定事件
        msg.submit(
            user_message,
            [msg, chatbot, model_dropdown],
            [msg, chatbot],
            queue=False
        ).then(
            bot_message,
            [chatbot, model_dropdown],
            [chatbot]
        ).then(
            update_status,
            None,
            [status_panel]
        )

        submit_btn.click(
            user_message,
            [msg, chatbot, model_dropdown],
            [msg, chatbot],
            queue=False
        ).then(
            bot_message,
            [chatbot, model_dropdown],
            [chatbot]
        ).then(
            update_status,
            None,
            [status_panel]
        )

        clear_btn.click(
            clear_conversation,
            None,
            [chatbot, status_panel],
            queue=False
        )

        export_btn.click(
            export_conversation,
            None,
            [status_panel],
            queue=False
        )

        # 页面加载时更新状态
        demo.load(update_status, None, status_panel)


def main():
    """主函数"""
    print("[START] 启动 多提供商 LLM 客户端...")

    # 检查API配置
    if not check_api_key():
        print("\n⚠️  请先配置至少一个API密钥环境变量")
        print("   创建.env文件并添加以下变量之一:")
        print("   - CEREBRAS_API_KEY=your_api_key_here")
        print("   - DEEPSEEK_API_KEY=your_api_key_here")
        print("   - OPENAI_API_KEY=your_api_key_here")
        print("\n您仍然可以启动界面，但需要配置API密钥才能正常使用。")

    # 创建并启动应用
    client = LLMClient()
    demo = client.create_interface()

    # 启动服务器
    demo.launch(
        server_name=SERVER_HOST,
        server_port=SERVER_PORT,
        share=False,
        inbrowser=True,
        show_error=True
    )


if __name__ == "__main__":
    main()
