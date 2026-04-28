import os
from dotenv import load_dotenv


load_dotenv()


LLM_API_KEY = os.getenv("LLM_API_KEY", "").strip()
LLM_MODEL = os.getenv("LLM_MODEL", "").strip()
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "").strip()


def check_config():
    if not LLM_API_KEY:
        raise ValueError("缺少 LLM_API_KEY，请在 .env 文件中配置。")

    if not LLM_MODEL:
        raise ValueError("缺少 LLM_MODEL，请在 .env 文件中配置。")

    if not LLM_BASE_URL:
        raise ValueError("缺少 LLM_BASE_URL，请在 .env 文件中配置。")

    return {
        "llm_model": LLM_MODEL,
        "llm_base_url": LLM_BASE_URL,
        "has_api_key": True,
    }


if __name__ == "__main__":
    config = check_config()
    print(config)