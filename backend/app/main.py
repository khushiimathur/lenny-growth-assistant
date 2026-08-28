from fastapi import FastAPI
from app.api.messages import router as messages_router
from app.api.sessions import router as sessions_router
from app.routes.chat import router as chat_router
from app.config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.app_name,
    description="AI-powered product and growth assistant grounded in Lenny's Podcast transcripts.",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sessions_router)
app.include_router(messages_router)
app.include_router(chat_router)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "environment": settings.environment,
        "llm_provider": settings.llm_provider,
    }