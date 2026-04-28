import os
from dotenv import load_dotenv


load_dotenv()


LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "your_model_name_here")


def check_config():
    """
    检查必要配置是否存在。
    """

    if not LLM_API_KEY:
        raise ValueError("缺少 LLM_API_KEY，请在 .env 文件中配置。")

    return {
        "llm_model": LLM_MODEL,
        "has_api_key": True,
    }


if __name__ == "__main__":
    config = check_config()
    print(config)
