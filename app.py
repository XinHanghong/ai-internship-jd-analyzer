from fastapi import FastAPI
from pydantic import BaseModel

from main import analyze_jd
from llm_service import analyze_jd_with_llm
from db import save_record, get_recent_records
from rag_answer_service import answer_with_rag
app = FastAPI(
    title="AI Internship JD Analyzer",
    description="一个用于分析 AI / Agent 实习岗位 JD 的 API 服务",
    version="1.0.0",
)


class AnalyzeRequest(BaseModel):
    jd_text: str
    mode: str = "rule"
    save: bool = False
class RagRequest(BaseModel):
    query: str
    top_k: int = 2
@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "AI Internship JD Analyzer API is running.",
    }


@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    mode = request.mode

    if mode == "llm":
        result = analyze_jd_with_llm(request.jd_text)
    else:
        mode = "rule"
        result = analyze_jd(request.jd_text)

    response = {
        "mode": mode,
        "result": result,
    }

    if request.save:
        record_id = save_record(mode, request.jd_text, result)
        response["saved"] = True
        response["record_id"] = record_id

    return response
@app.get("/history")
def history():
    records = get_recent_records()
    return {
        "records": records
    }
@app.post("/rag")
def rag_answer(request: RagRequest):
    result = answer_with_rag(
        query=request.query,
        top_k=request.top_k,
    )

    return result