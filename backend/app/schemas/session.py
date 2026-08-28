from datetime import datetime

from pydantic import BaseModel


class SessionCreate(BaseModel):
    user_id: str | None = None


class SessionResponse(BaseModel):
    id: str
    user_id: str | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }