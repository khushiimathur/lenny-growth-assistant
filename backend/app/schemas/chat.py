from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    session_id: str
    message: str = Field(
        min_length=1,
        max_length=2000,
    )


class Source(BaseModel):
    title: str
    guest: str
    youtube_url: str | None = None
    start_timestamp: str | None = None
    end_timestamp: str | None = None


class Artifact(BaseModel):
    type: str
    content: str


class ChatResponse(BaseModel):
    session_id: str
    answer: str
    sources: list[Source]
    artifact: Artifact | None = None