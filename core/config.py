import os
from dotenv import load_dotenv
from pathlib import Path

# 定位到项目根目录
# Path(__file__) -> /path/to/project/core/config.py
# .parent -> /path/to/project/core
# .parent -> /path/to/project
env_path = Path(__file__).parent.parent / '.env'

# 加载 .env 文件
load_dotenv(dotenv_path=env_path)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")

# 你可以在这里添加更多的配置
# 例如，默认的模型名称
DEFAULT_LLM_MODEL = "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"
DEFAULT_EMBEDDING_MODEL = "Qwen/Qwen3-Embedding-4B"

class settings:
    # 从环境变量中获取 API Key
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")

    # 你可以在这里添加更多的配置
    # 例如，默认的模型名称
    DEFAULT_LLM_MODEL = "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"
    DEFAULT_EMBEDDING_MODEL = "Qwen/Qwen3-Embedding-4B"
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

