from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


JOBS_DIR = Path(__file__).parent / "data" / "jobs"


def load_job_documents() -> list[dict]:
    """
    读取 data/jobs 目录下的所有岗位 JD 文件。

    返回:
        [
            {
                "source": "jd_agent.txt",
                "content": "岗位内容..."
            }
        ]
    """

    documents = []

    if not JOBS_DIR.exists():
        raise FileNotFoundError(f"岗位目录不存在: {JOBS_DIR}")

    for file_path in JOBS_DIR.glob("*.txt"):
        content = file_path.read_text(encoding="utf-8")

        documents.append(
            {
                "source": file_path.name,
                "content": content,
            }
        )

    return documents


def search_jobs(query: str, top_k: int = 3) -> list[dict]:
    """
    根据用户问题检索最相关的岗位 JD。

    参数:
        query: 用户问题
        top_k: 返回最相关的前几个结果

    返回:
        相关岗位列表
    """

    documents = load_job_documents()

    if not documents:
        return []

    texts = [doc["content"] for doc in documents]

    # 把岗位文本和用户问题一起转成向量
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(texts + [query])

    # 前面是岗位向量，最后一个是问题向量
    document_vectors = vectors[:-1]
    query_vector = vectors[-1]

    # 计算问题和每个岗位之间的相似度
    similarities = cosine_similarity(query_vector, document_vectors).flatten()

    ranked_results = []

    for index, score in enumerate(similarities):
        ranked_results.append(
            {
                "source": documents[index]["source"],
                "score": round(float(score), 4),
                "content": documents[index]["content"],
            }
        )

    # 按相似度从高到低排序
    ranked_results.sort(key=lambda item: item["score"], reverse=True)

    return ranked_results[:top_k]


if __name__ == "__main__":
    query = "我刚学完 Python，想找 AI Agent 实习，应该看哪些岗位？"

    results = search_jobs(query, top_k=3)

    print(f"查询问题: {query}")
    print("-" * 60)

    for item in results:
        print(f"文件: {item['source']}")
        print(f"相似度: {item['score']}")
        print("内容:")
        print(item["content"])
        print("-" * 60)