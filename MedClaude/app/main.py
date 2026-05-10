"""
MedCore+ Diagnostic AI — FastAPI Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import structlog

from app.config import Settings
from app.services.rag_pipeline import RAGPipeline
from app.security.input_guard import InputGuard
from app.security.output_filter import OutputFilter

log = structlog.get_logger()
settings = Settings()

app = FastAPI(
    title="MedCore+ Diagnostic AI",
    version="1.0.0",
    description="Clinical-grade AI diagnostic assistant. All outputs require clinician review.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_methods=["POST", "GET"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.on_event("startup")
async def startup():
    log.info("medcore.startup", env=settings.env, model=settings.model)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "medcore-diagnostic-ai"}


# Routes registered in app/routes/
from app.routes import diagnose, reports, triage  # noqa: E402
app.include_router(diagnose.router, prefix="/api/v1")
app.include_router(reports.router, prefix="/api/v1")
app.include_router(triage.router, prefix="/api/v1")
