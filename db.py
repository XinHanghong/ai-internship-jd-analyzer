import json
import sqlite3
from datetime import datetime
from pathlib import Path


DB_PATH = Path(__file__).parent / "app.db"


def get_connection():
    """
    获取数据库连接。
    """

    return sqlite3.connect(DB_PATH)


def init_db():
    """
    初始化数据库表。
    如果 records 表不存在，就创建它。
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mode TEXT NOT NULL,
            jd_text TEXT NOT NULL,
            result_json TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()


def save_record(mode: str, jd_text: str, result: dict) -> int:
    """
    保存一次 JD 分析记录。

    参数:
        mode: 分析模式，例如 rule 或 llm
        jd_text: 原始 JD 文本
        result: 分析结果字典

    返回:
        新记录的 id
    """

    init_db()

    conn = get_connection()
    cursor = conn.cursor()

    result_json = json.dumps(result, ensure_ascii=False)
    created_at = datetime.now().isoformat(timespec="seconds")

    cursor.execute(
        """
        INSERT INTO records (mode, jd_text, result_json, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (mode, jd_text, result_json, created_at),
    )

    record_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return record_id