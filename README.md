# 多提供商 LLM 客户端

一个基于Gradio的多提供商LLM聊天客户端，支持Cerebras、DeepSeek和OpenAI等多种AI提供商。

## 功能特性

- 🚀 支持多个AI提供商（Cerebras、DeepSeek、OpenAI）
- 🎨 美观的Gradio Web界面
- 🔄 支持多轮对话历史
- 📱 响应式设计，支持移动端
- 🔧 支持多种模型选择
- ⚡ 实时提供商状态显示
- 📋 一键复制回复内容

## 支持的提供商和模型

### Cerebras

- `llama-3.3-70b`
- `llama-3.1-8b`
- `llama-3.1-70b`
- `llama-3.2-3b`
- `llama-3.2-1b`
- `qwen-3-235b-a22b-instruct-2507` (默认)
- `qwen-3-235b-a22b-thinking-2507`
- `zai-glm-4.6`
- `gpt-oss-120b`
- `qwen-3-32b`

### DeepSeek

- `deepseek-chat`
- `deepseek-coder`
- `deepseek-reasoner`

### OpenAI

- `gpt-4o`
- `gpt-4o-mini`
- `gpt-4-turbo`
- `gpt-3.5-turbo`

## 安装和运行

### 1. 克隆项目

```bash
git clone <repository-url>
cd SimpleLLMFront
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置API密钥

在运行应用之前，您需要配置至少一个AI提供商的API密钥。推荐使用 `.env` 文件方式：

#### 方法一：使用.env文件（推荐）

```bash
# 复制示例文件
cp .env.example .env

# 编辑.env文件，填入您的API密钥
# 在Windows上可以使用记事本或其他编辑器编辑
```

编辑 `.env` 文件，将相应的API密钥替换为您的真实API密钥：

```env
# Cerebras API密钥（从 https://cloud.cerebras.ai/ 获取）
CEREBRAS_API_KEY=your_cerebras_api_key_here

# DeepSeek API密钥（从 https://platform.deepseek.com/ 获取）
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# OpenAI API密钥（从 https://platform.openai.com/ 获取）
OPENAI_API_KEY=your_openai_api_key_here
```

#### 方法二：设置环境变量

##### Windows (命令提示符)

```cmd
set CEREBRAS_API_KEY=your_api_key_here
set DEEPSEEK_API_KEY=your_api_key_here
set OPENAI_API_KEY=your_api_key_here
```

##### Windows (PowerShell)

```powershell
$env:CEREBRAS_API_KEY="your_api_key_here"
$env:DEEPSEEK_API_KEY="your_api_key_here"
$env:OPENAI_API_KEY="your_api_key_here"
```

##### Linux/Mac

```bash
export CEREBRAS_API_KEY=your_api_key_here
export DEEPSEEK_API_KEY=your_api_key_here
export OPENAI_API_KEY=your_api_key_here
```

### 4. 运行应用

```bash
python main.py
```

应用将在 `http://localhost:7860` 启动，并自动在默认浏览器中打开。

## 使用说明

1. **配置API密钥**：确保已正确设置至少一个提供商的API密钥
2. **选择模型**：从下拉菜单中选择要使用的LLM模型（系统会自动选择对应的提供商）
3. **开始对话**：在输入框中输入问题，点击"发送"或按Enter键
4. **查看历史**：所有对话历史都会保存在聊天界面中
5. **清除对话**：点击"清除对话"按钮可以重置对话历史

## 界面说明

- **模型选择**：选择不同的LLM模型（支持Cerebras、DeepSeek、OpenAI）
- **聊天界面**：显示对话历史，支持复制回复
- **输入框**：输入您的问题
- **发送按钮**：提交问题
- **清除按钮**：重置对话历史
- **状态栏**：显示所有提供商的状态信息

## 故障排除

### 常见问题

1. **API密钥未设置**
    - 错误信息："没有配置任何有效的API密钥"
    - 解决方案：创建 `.env` 文件并填入至少一个提供商的API密钥

2. **提供商不可用**
    - 错误信息："提供商 'xxx' 未配置或不可用"
    - 解决方案：检查对应提供商的API密钥是否正确配置

3. **API调用失败**
    - 错误信息："xxx API调用失败: ..."
    - 解决方案：检查API密钥是否正确，网络连接是否正常

4. **端口被占用**
    - 错误信息："Address already in use"
    - 解决方案：修改 `main.py` 中的 `server_port` 参数

### 开发说明

- 主要文件：`main.py`
- 提供商管理：`providers.py`
- API服务：`api_service.py`
- 配置管理：`config.py`
- 依赖管理：`requirements.txt`
- 环境配置：通过 `.env` 文件（使用python-dotenv）或环境变量
- 示例配置：`.env.example`

## 技术栈

- **前端框架**：Gradio
- **后端API**：Cerebras Cloud SDK、OpenAI SDK
- **提供商架构**：抽象工厂模式
- **环境管理**：python-dotenv
- **Python版本**：3.8+

## 许可证

MIT License