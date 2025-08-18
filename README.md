# Intelli-Core ("智脑核心")

Intelli-Core 是一个模块化的实验平台，旨在帮助用户学习、实现和测试从基础的 RAG (检索增强生成) 问答系统，到由主控程序协调的复杂多智能体 (Multi-Agent) 协作框架。

项目最终实现的场景允许用户输入一个复杂的任务，例如：**“请调研一下最近关于‘AI Agent’的最新研究，并生成一份总结报告。”** 系统将自动执行以下步骤：
1.  **任务分解**: 初始请求被分解为核心研究主题。
2.  **研究**: 一个专门的 **研究员 Agent** 使用搜索工具和私有知识库 (RAG) 来查找相关信息。
3.  **写作**: 一个专门的 **作家 Agent** 获取研究结果，并撰写一份结构清晰、语言流畅的报告。
4.  **编排**: 一个基于 LangGraph 构建的 **主控程序 (MCP)** 负责协调整个工作流，管理智能体之间的信息流转。

![Intelli-Core UI Demo](https://i.imgur.com/your-demo-image.gif) <!-- 占位符，未来可替换为项目动图 -->

---

## ✨ 核心功能

*   **🤖 多智能体框架**: 实现了一个完整的多智能体系统，包含专门的角色（���究员、作家）。
*   **🧠 智能编排**: 使用 LangGraph 创建了一个健壮的、有状态的工作流来协调智能体之间的协作。
*   **📚 RAG 知识库**: 集成了一个检索增强生成管道，使用持久化的向量数据库 (ChromaDB) 作为智能体可查询的私有知识库。
*   **🛠️ 工具增强的智能体**: 智能体配备了网络搜索、计算器和私有 RAG 知识库等工具，并能自主选择使用哪种工具。
*   **🔌 可插拔的 LLM 后端**: 可以轻松切换大语言模型提供商。系统已预先配置好 OpenAI (GPT 系列)，并可轻松适配 Google Gemini 等其他模型。
*   **🖥️ 交互式 UI**: 使用 Streamlit 构建了一个简洁直观的用户界面，方便用户与多智能体工作流进行交互和可视化。
*   **📄 便捷的数据加载**: 提供了一个脚本，可以轻松地将您自己的文本文档加载到智能体的知识库中。

---

## 🛠️ 技术栈

*   **编程语言**: Python 3.12+
*   **核心框架**: LangChain & LangGraph
*   **大语言模型**: LangChain OpenAI (可轻松替换)
*   **向量数据库**: ChromaDB (持久化)
*   **用户界面**: Streamlit
*   **环境管理**: uv (推荐)

---

## 🏗️ 项目结构

项目被组织成职责分明的独立模块：

```
/
├─── agent/         # 单��智能体的核心逻辑 (ReAct 框架)
├─── core/          # 基础配置、模型提供者、日志
├─── mcp/           # 主控程序：编排器、智能体管理器、任务分解器
├─── rag/           # RAG 管道：文档加载、文本分割、向量存储
├─── scripts/       # 工具脚本，例如：数据加载
├─── tools/         # 智能体可用的工具 (搜索、计算器、RAG)
├─── ui/            # Streamlit 用户界面
├─── chroma_db/     # 持久化向量数据库目录
├─── .env           # API 密钥和环境变量
└─── requirements.txt
```

---

## 🚀 快速开始

请按照以下步骤在您的本地机器上设置并运行 Intelli-Core 平台。

### 1. 环境要求

*   Python 3.12 或更高版本。
*   `uv` (推荐使用，可实现快速的环境和包管理)。您可以通过 `pip install uv` 来安装。

### 2. 克隆仓库

```bash
git clone https://github.com/your-username/intelli-core.git
cd intelli-core
```

### 3. 设置虚拟环境

使用 `uv` 创建并激活虚拟环境。

```bash
# 创建虚拟环境
uv venv

# 激活环境 (在 Linux/macOS 上)
source .venv/bin/activate
```

### 4. 安装依赖

安装所有必需的 Python 包。

```bash
uv pip install -r requirements.txt
```

### 5. 配置 API 密钥

应用需要 OpenAI 和 Google 搜索的 API 密钥。

```bash
# 1. 复制 .env 示例文件
cp .env.example .env

# 2. 使用文本编辑器打开 .env 文件
# nano .env
```

**3. 填入所需的值：**
*   `OPENAI_API_KEY`: 您在 [OpenAI Platform](https://platform.openai.com/api-keys) 上获取的 API 密钥。
*   `GOOGLE_API_KEY` & `GOOGLE_CSE_ID`: 为了启用网络搜索工具，您需要一个 Google API 密钥和一个自定义搜索引擎 ID。请参考[此文档](https://developers.google.com/custom-search/v1/overview)获取。

---

## 🏃‍♀️ 如何运行

### 1. (可选) 填充知识库

为了让 **研究员 Agent** 能够从您的私有文档中回答问题，您首先需要将它们加载到向量数据库中。

将您的 `.txt` 文件放在一个目录中（例如，创建一个 `data/` 文件夹），然后为每个文件运行数据加载脚本。

```bash
# 示例：加载一个名为 'my_document.txt' 的文档
python scripts/ingest_data.py path/to/your/my_document.txt
```

该脚本将处理文档并将其添加到 `chroma_db` 目录下的 `intelli-core-kb` 持久化集合中。

### 2. 启动应用

在项目的根目录下运行 Streamlit 应用。

```bash
streamlit run ui/app.py
```

您的浏览器应该会自动打开一个新标签页，并显示 Intelli-Core 的用户界面。如果没有，请访问您终端中显示的本地 URL (通常是 `http://localhost:8501`)。

### 3. 与系统交互

在 UI 界面的文本框中输入一个复杂的研究任务，然后点击“开始执行”。应用将分步显示智能体协作完成请求的过程，并在任务完成后展示最终的报告。