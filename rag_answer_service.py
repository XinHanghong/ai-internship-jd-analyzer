import json

from openai import (
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    RateLimitError,
    OpenAI,
)

from config import LLM_API_KEY, LLM_MODEL, LLM_BASE_URL
from rag_service import search_jobs


client = OpenAI(
    api_key=LLM_API_KEY,
    base_url=LLM_BASE_URL,
    timeout=120.0,
    max_retries=2,
)


def build_context(retrieved_jobs: list[dict]) -> str:
    """
    把检索到的岗位 JD 拼接成上下文。
    """

    context_parts = []

    for index, job in enumerate(retrieved_jobs, start=1):
        context_parts.append(
            f"""
资料 {index}
来源文件：{job["source"]}
相似度：{job["score"]}

内容：
{job["content"]}
"""
        )

    return "\n".join(context_parts)


def parse_json_output(output_text: str) -> dict:
    """
    尝试从模型输出中解析 JSON。
    兼容 <think>、Markdown 代码块、前后解释文字等情况。
    """

    text = output_text.strip()

    if "</think>" in text:
        text = text.split("</think>", 1)[1].strip()

    if text.startswith("```json"):
        text = text.removeprefix("```json").strip()

    if text.startswith("```"):
        text = text.removeprefix("```").strip()

    if text.endswith("```"):
        text = text.removesuffix("```").strip()

    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1 and start < end:
        text = text[start:end + 1]

    return json.loads(text)


def answer_with_rag(query: str, top_k: int = 2) -> dict:
    """
    基于岗位 JD 检索结果，让大模型生成求职建议。
    """

    retrieved_jobs = search_jobs(query, top_k=top_k)
    context = build_context(retrieved_jobs)

    prompt = f"""
你是一个 AI Agent 实习求职导师。

请你基于下面检索到的岗位 JD 资料回答用户问题。
你只能基于资料回答，不要编造岗位要求。

请严格遵守以下要求：
1. 只能返回 JSON
2. 不要返回 Markdown
3. 不要使用代码块
4. 不要输出 <think> 或任何思考过程
5. 不要添加任何解释性文字
6. 返回内容必须能被 Python 的 json.loads() 直接解析

用户问题：
{query}

检索到的岗位资料：
{context}

返回结构：
{{
  "summary": "总体建议",
  "recommended_roles": ["推荐岗位1", "推荐岗位2"],
  "matched_skills": ["用户当前可能匹配的技能"],
  "missing_skills": ["还需要补充的技能"],
  "learning_plan": ["学习建议1", "学习建议2"],
  "interview_focus": ["面试重点1", "面试重点2"]
}}
"""

    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "你是一个严格输出 JSON 的 AI Agent 求职导师。不要输出思考过程。",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.2,
        )

        output_text = response.choices[0].message.content.strip()

        try:
            answer = parse_json_output(output_text)
        except json.JSONDecodeError:
            answer = {
                "error": "模型返回的不是合法 JSON",
                "raw_output": output_text,
            }

        return {
            "query": query,
            "retrieved_sources": [job["source"] for job in retrieved_jobs],
            "retrieved_jobs": retrieved_jobs,
            "answer": answer,
        }

    except AuthenticationError:
        return {
            "error": "认证失败，请检查 API Key。"
        }

    except RateLimitError:
        return {
            "error": "额度不足或触发速率限制，请检查平台余额。"
        }

    except APITimeoutError:
        return {
            "error": "请求超时，请稍后重试。"
        }

    except APIConnectionError:
        return {
            "error": "网络连接失败，请检查网络或代理平台线路。"
        }


if __name__ == "__main__":
    query = "我刚学完 Python，想找 AI Agent 实习，应该看哪些岗位？"

    result = answer_with_rag(query, top_k=2)

    print(json.dumps(result, ensure_ascii=False, indent=2))