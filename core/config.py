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
DEFAULT_LLM_MODEL = "deepseek-chat"
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"

class settings:
    # 从环境变量中获取 API Key
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")

    # 你可以在这里添加更多的配置
    # 例如，默认的模型名称
    DEFAULT_LLM_MODEL = "deepseek-chat"
    DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"

