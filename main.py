import json
import sys
from pathlib import Path

from db import save_record
from llm_service import analyze_jd_with_llm


TECH_KEYWORDS = [
    "Python",
    "FastAPI",
    "RAG",
    "LangChain",
    "LangGraph",
    "LlamaIndex",
    "Agent",
    "大模型",
    "向量数据库",
    "Git",
    "Docker",
    "SQL",
    "PostgreSQL",
    "SQLite",
    "Embedding",
    "向量检索",
    "Function Calling",
    "ReAct",
    "MCP",
]


def read_jd_file(file_path: str) -> str:
    """
    读取岗位 JD 文件内容。
    """

    current_dir = Path(__file__).parent
    full_path = current_dir / file_path

    if not full_path.exists():
        raise FileNotFoundError(f"文件不存在: {full_path}")

    return full_path.read_text(encoding="utf-8")


def extract_keywords(text: str, keywords: list[str]) -> list[str]:
    """
    从文本中提取关键词。
    """

    text_lower = text.lower()
    found_keywords = []

    for keyword in keywords:
        if keyword.lower() in text_lower:
            found_keywords.append(keyword)

    return found_keywords


def analyze_text_length(text: str) -> dict:
    """
    分析文本长度。
    """

    return {
        "char_count": len(text),
        "line_count": len(text.splitlines()),
    }


def judge_difficulty(found_keywords: list[str]) -> str:
    """
    根据关键词判断岗位难度。
    """

    advanced_keywords = [
        "RAG",
        "LangChain",
        "LangGraph",
        "LlamaIndex",
        "向量数据库",
        "Embedding",
        "向量检索",
        "Function Calling",
        "ReAct",
        "MCP",
        "Docker",
    ]

    advanced_count = 0

    for keyword in found_keywords:
        if keyword in advanced_keywords:
            advanced_count += 1

    if advanced_count >= 5:
        return "偏进阶"
    elif advanced_count >= 2:
        return "适合有一定基础的初学者"
    else:
        return "适合初学者"


def generate_learning_suggestions(found_keywords: list[str]) -> list[str]:
    """
    根据识别到的关键词生成学习建议。
    """

    suggestions = []

    if "Python" in found_keywords:
        suggestions.append("继续加强 Python 工程化能力，例如项目结构、异常处理、文件读取、API 调用和日志。")

    if "FastAPI" in found_keywords:
        suggestions.append("学习 FastAPI，掌握 GET、POST、Pydantic、接口文档和基础后端服务开发。")

    if "RAG" in found_keywords:
        suggestions.append("学习 RAG 基础，包括文本切分、Embedding、向量数据库、检索和基于资料生成回答。")

    if "Agent" in found_keywords:
        suggestions.append("学习 Agent 基础，包括工具调用、任务拆解、Observation、ReAct 和多步骤执行。")

    if "LangChain" in found_keywords or "LangGraph" in found_keywords:
        suggestions.append("了解 LangChain / LangGraph，重点掌握工具调用、状态管理和多步骤工作流。")

    if "向量数据库" in found_keywords or "向量检索" in found_keywords or "Embedding" in found_keywords:
        suggestions.append("补充向量检索基础，理解 Embedding、相似度搜索、Chroma / Qdrant 等向量数据库。")

    if "Function Calling" in found_keywords:
        suggestions.append("学习 Function Calling，理解大模型如何选择并调用外部工具函数。")

    if "ReAct" in found_keywords:
        suggestions.append("阅读 ReAct 思路，理解 Thought、Action、Observation 的循环执行方式。")

    if "MCP" in found_keywords:
        suggestions.append("了解 MCP 的基本概念，知道 Agent 如何连接外部工具、资源和服务。")

    if "Docker" in found_keywords:
        suggestions.append("了解 Docker 基础，能够为 Python / FastAPI 项目编写简单 Dockerfile。")

    if "Git" in found_keywords:
        suggestions.append("学习 Git 基础，掌握 init、add、commit、branch 和 push。")

    if "SQL" in found_keywords or "PostgreSQL" in found_keywords or "SQLite" in found_keywords:
        suggestions.append("学习数据库基础，掌握表、增删改查、SQLite 和 PostgreSQL 的基本使用。")

    if not suggestions:
        suggestions.append("这个 JD 暂时没有识别到 AI Agent 相关关键词，建议先巩固 Python 基础和 Git 使用。")

    return suggestions


def analyze_jd(text: str) -> dict:
    """
    规则版 JD 分析。
    """

    length_info = analyze_text_length(text)
    found_keywords = extract_keywords(text, TECH_KEYWORDS)
    difficulty = judge_difficulty(found_keywords)
    suggestions = generate_learning_suggestions(found_keywords)

    return {
        "length_info": length_info,
        "found_keywords": found_keywords,
        "keyword_count": len(found_keywords),
        "has_agent_keyword": "Agent" in found_keywords,
        "difficulty": difficulty,
        "suggestions": suggestions,
    }


def main():
    """
    程序入口。
    支持规则分析、LLM 分析，以及保存分析记录。
    """

    if len(sys.argv) < 2:
        print("用法:")
        print("  python main.py jd.txt")
        print("  python main.py jd.txt --rule")
        print("  python main.py jd.txt --llm")
        print("  python main.py jd.txt --rule --save")
        print("  python main.py jd.txt --llm --save")
        return

    file_path = sys.argv[1]

    mode = "rule"

    if "--llm" in sys.argv:
        mode = "llm"

    if "--rule" in sys.argv:
        mode = "rule"

    should_save = "--save" in sys.argv

    try:
        jd_text = read_jd_file(file_path)

        if mode == "llm":
            result = analyze_jd_with_llm(jd_text)
        else:
            result = analyze_jd(jd_text)

        output = {
            "mode": mode,
            "result": result,
        }

        if should_save:
            record_id = save_record(mode, jd_text, result)
            output["saved"] = True
            output["record_id"] = record_id

        print(json.dumps(output, ensure_ascii=False, indent=2))

    except FileNotFoundError as error:
        print(f"错误: {error}")


if __name__ == "__main__":
    main()