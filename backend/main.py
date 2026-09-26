from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from orchestrator import analyze_question
from schemas import AnalysisRequest, AnalysisResponse


app = FastAPI(title="ForgeBridge API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "project": "ForgeBridge",
        "legacy_system": "AUTOFACTORY-2005",
    }


@app.post("/api/analyze", response_model=AnalysisResponse)
def analyze(request: AnalysisRequest):
    return analyze_question(request.question)