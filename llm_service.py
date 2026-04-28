import json

from openai import (
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    OpenAI,
)

from config import LLM_API_KEY, LLM_MODEL, LLM_BASE_URL


client = OpenAI(
    api_key=LLM_API_KEY,
    base_url=LLM_BASE_URL,
    timeout=60.0,
    max_retries=2,
)


def parse_json_output(output_text: str) -> dict:
    """
    尝试把模型输出解析成 JSON。
    """

    text = output_text.strip()

    # 有些模型可能会返回 ```json ... ```，这里做简单清理
    if text.startswith("```json"):
        text = text.removeprefix("```json").removesuffix("```").strip()
    elif text.startswith("```"):
        text = text.removeprefix("```").removesuffix("```").strip()

    return json.loads(text)


def analyze_jd_with_llm(jd_text: str) -> dict:
    """
    使用大模型分析岗位 JD。
    """

    prompt = f"""
你是一个 AI Agent 实习求职导师。

请分析下面这段岗位 JD，并严格返回 JSON，不要返回 Markdown，不要添加额外解释。

岗位 JD：
{jd_text}

请返回以下 JSON 结构：
{{
  "role_type": "岗位类型",
  "required_skills": ["必备技能1", "必备技能2"],
  "bonus_skills": ["加分技能1", "加分技能2"],
  "difficulty": "适合初学者 / 适合有一定基础的初学者 / 偏进阶",
  "learning_suggestions": ["学习建议1", "学习建议2"],
  "interview_questions": ["可能面试题1", "可能面试题2"]
}}
"""

    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "你是一个严格输出 JSON 的 AI Agent 求职导师。",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.2,
        )

        output_text = response.choices[0].message.content

        try:
            return parse_json_output(output_text)
        except json.JSONDecodeError:
            return {
                "error": "模型返回的不是合法 JSON",
                "raw_output": output_text,
            }

    except AuthenticationError:
        return {
            "error": "认证失败，请检查 .env 里的 LLM_API_KEY 是否正确。",
        }

    except RateLimitError:
        return {
            "error": "额度不足或触发速率限制，请检查代理平台余额或调用限制。",
        }

    except NotFoundError:
        return {
            "error": "接口地址、模型名或接口路径错误。请检查 LLM_BASE_URL 是否为真实 API 地址，并确认 LLM_MODEL 是否可用。",
        }

    except APITimeoutError:
        return {
            "error": "请求超时。可能是网络不稳定、模型响应慢，或代理线路不稳定。",
        }

    except APIConnectionError:
        return {
            "error": "网络连接失败，请检查网络、代理平台线路或稍后重试。",
        }


if __name__ == "__main__":
    sample_jd = """
我们正在招聘 AI Agent 实习生，要求熟悉 Python，了解 FastAPI 和大模型 API 调用。
加分项包括 RAG、LangChain、LangGraph、向量数据库、Function Calling 和 Docker。
"""

    result = analyze_jd_with_llm(sample_jd)
    print(json.dumps(result, ensure_ascii=False, indent=2))