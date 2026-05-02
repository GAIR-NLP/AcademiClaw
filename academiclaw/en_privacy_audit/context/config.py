import os
# Set proxy environment variables for external API access
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7897'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7897'

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "sk-REDACTED_OPENCLAW_KEY")

LLM_MODEL = "gpt-5"

LLM_JUDGE_MODEL = "qwen3-max"

EMBEDDING_MODEL = "text-embedding-v4"

OPENAI_API_BASE = "https://api.opensii.ai/v1"