import streamlit as st
from pathlib import Path
import sys
import uuid

# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from core.config import settings
from mcp.orchestrator import main_orchestrator
from tools.rag_tool import DEFAULT_COLLECTION_NAME

# --- Streamlit UI Configuration ---
st.set_page_config(page_title="Intelli-Core Multi-Agent Demo", layout="wide")

# --- Sidebar ---
with st.sidebar:
    st.header("配置")
    # Check for Google API Key
    if settings.GOOGLE_API_KEY and "YOUR_GOOGLE_API_KEY" not in settings.GOOGLE_API_KEY:
        st.success("✅ Google API Key 已配置。")
    else:
        st.error("❌ Google API Key 未配置。")
        st.info("请在项目根目录下创建 `.env` 文件并填入你的 `GOOGLE_API_KEY`。")

    # Check for Google Search API Keys
    if settings.GOOGLE_API_KEY and settings.GOOGLE_CSE_ID:
        st.success("✅ Google Search API 已配置。")
    else:
        st.warning("⚠️ Google Search API 未配置。")
        st.info("研究员 Agent 的搜索工具将不可用。")

    st.divider()
    st.header("知识库")
    st.info(
        f"研究员 Agent 会使用一个名为 `{DEFAULT_COLLECTION_NAME}` 的持久化向量数据库作为其私有知识库。"
        "你需要运行一个独立的脚本来加载文档到此知识库中。"
    )

# --- Main Page ---
st.title("🧠 Intelli-Core: 多智能体协作系统")
st.write(
    "输入一个复杂的研究任务，系统将自动进行任务分解、信息研究和报告撰写。"
)

# --- User Input ---
st.header("请输入您的研究任务")
prompt = st.text_area(
    "例如: '请调研一下最近关于‘AI Agent’的最新研究，并生成一份总结报告。'",
    height=100
)

if st.button("开始执行"):
    if not prompt:
        st.warning("请输入任务内容。")
    else:
        st.header("任务执行追踪")
        
        # Each run needs a unique thread_id for the orchestrator's memory
        thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}
        
        try:
            # Use placeholders to show the process step-by-step
            with st.status("🚀 任务开始...", expanded=True) as status:
                
                # Stream the orchestrator's execution
                for step in main_orchestrator.stream({"user_request": prompt}, config=config):
                    node_name = list(step.keys())[0]
                    state_update = step[node_name]
                    
                    if node_name == "decomposer":
                        status.update(label="分解任务中...")
                        st.write(f"**[任务分解]** 识别出的核心主题: `{state_update['topic']}`")
                    
                    elif node_name == "researcher":
                        status.update(label="研究员 Agent 正在收集中...")
                        st.write(f"**[研究员]** 已完成信息收集。")
                        with st.expander("查看研究员的发现"):
                            st.markdown(state_update['research_findings'])
                    
                    elif node_name == "writer":
                        status.update(label="作家 Agent 正在撰写报告...")
                        st.write(f"**[作家]** 已完成报告撰写。")

                status.update(label="✅ 任务完成！", state="complete")

            # Display the final report
            st.header("最终报告")
            final_state = main_orchestrator.get_state(config)
            final_report = final_state.values.get('final_report', "未能生成报告。")
            st.markdown(final_report)

        except Exception as e:
            st.error(f"执行任务时发生错误: {e}")
