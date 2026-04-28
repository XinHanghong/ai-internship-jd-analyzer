import json
import sys
from pathlib import Path


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

    参数:
        file_path: JD 文件路径，例如 "jd.txt"

    返回:
        文件中的文本内容

    如果文件不存在，会抛出 FileNotFoundError。
    """

    # 获取当前 main.py 所在的文件夹
    current_dir = Path(__file__).parent

    # 拼接出文件完整路径
    path = current_dir / file_path

    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {path}")

    text = path.read_text(encoding="utf-8")

    return text


def extract_keywords(text: str, keywords: list[str]) -> list[str]:
    """
    从文本中提取出现过的关键词。

    参数:
        text: 岗位 JD 文本
        keywords: 需要匹配的关键词列表

    返回:
        在文本中出现过的关键词列表
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

    参数:
        text: 岗位 JD 文本

    返回:
        包含字符数和行数的字典
    """

    return {
        "char_count": len(text),
        "line_count": len(text.splitlines()),
    }
def judge_difficulty(found_keywords: list[str]) -> str:
    """
    根据识别到的关键词判断岗位难度。

    参数:
        found_keywords: 已经在 JD 中找到的关键词列表

    返回:
        岗位难度判断结果
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

    参数:
        found_keywords: 已经在 JD 中找到的关键词列表

    返回:
        学习建议列表
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

    if "SQL" in found_keywords or "PostgreSQL" in found_keywords or "SQLite" in found_keywords:
        suggestions.append("学习数据库基础，掌握表、增删改查、SQLite 和 PostgreSQL 的基本使用。")

    if not suggestions:
        suggestions.append("这个 JD 暂时没有识别到 AI Agent 相关关键词，建议先巩固 Python 基础和 Git 使用。")

    return suggestions
def analyze_jd(text: str) -> dict:
    """
    分析岗位 JD 文本。

    参数:
        text: 岗位 JD 文本

    返回:
        分析结果字典
    """

    length_info = analyze_text_length(text)
    found_keywords = extract_keywords(text, TECH_KEYWORDS)
    difficulty = judge_difficulty(found_keywords)
    suggestions = generate_learning_suggestions(found_keywords)
    return {
        "length_info": length_info,
        "found_keywords": found_keywords,
        "keyword_count": len(found_keywords),
        "has_agent_keyword":"Agent" in found_keywords,
        "difficulty": difficulty,
        "suggestions": suggestions,
    }


def main():
    """
    程序入口函数。
    """

    if len(sys.argv) < 2:
        print("用法: python main.py jd.txt")
        return

    file_path = sys.argv[1]

    try:
        jd_text = read_jd_file(file_path)
        result = analyze_jd(jd_text)

        print(json.dumps(result, ensure_ascii=False, indent=2))

    except FileNotFoundError as error:
        print(f"错误：{error}")


if __name__ == "__main__":
    main()