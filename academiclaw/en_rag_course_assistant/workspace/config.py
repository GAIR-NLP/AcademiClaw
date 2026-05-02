import os

# API 配置（默认 OpenAI；如配置 SII_* 则自动切换到 SII）
SII_API_KEY = os.getenv("SII_API_KEY", "")
SII_API_BASE_URL = os.getenv("SII_API_BASE_URL", "")
SII_MODEL = os.getenv("SII_MODEL", "")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "")
MODEL_NAME = os.getenv("OPENAI_MODEL", "")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

# 若存在 SII 配置，优先使用 SII 作为 OpenAI 兼容接口
if SII_API_KEY and SII_API_BASE_URL:
	OPENAI_API_KEY = SII_API_KEY
	OPENAI_API_BASE = SII_API_BASE_URL
	if SII_MODEL:
		MODEL_NAME = SII_MODEL

# 数据目录配置
DATA_DIR = os.getenv("DATA_DIR", "./context/data")

# 向量数据库配置
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./vector_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "course_materials")

# 文本处理配置
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1200"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1024"))

# RAG 配置
TOP_K = int(os.getenv("TOP_K", "5"))
