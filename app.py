from fastapi import FastAPI
from pydantic import BaseModel

from main import analyze_jd
from llm_service import analyze_jd_with_llm


app = FastAPI(
    title="AI Internship JD Analyzer",
    description="一个用于分析 AI / Agent 实习岗位 JD 的 API 服务",
    version="1.0.0",
)


class AnalyzeRequest(BaseModel):
    jd_text: str
    mode: str = "rule"


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "AI Internship JD Analyzer API is running.",
    }


@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    if request.mode == "llm":
        result = analyze_jd_with_llm(request.jd_text)
    else:
        result = analyze_jd(request.jd_text)

    return {
        "mode": request.mode,
        "result": result,
    }