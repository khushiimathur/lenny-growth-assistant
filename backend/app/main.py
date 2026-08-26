from fastapi import FastAPI

from app.config import settings


app = FastAPI(
    title=settings.app_name,
    description="AI-powered product and growth assistant grounded in Lenny's Podcast transcripts.",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "environment": settings.environment,
        "llm_provider": settings.llm_provider,
    }