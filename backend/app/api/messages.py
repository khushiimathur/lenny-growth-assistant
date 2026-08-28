from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ChatSession, Message
from app.schemas.message import MessageCreate, MessageResponse


router = APIRouter(
    prefix="/api/sessions/{session_id}/messages",
    tags=["messages"],
)


@router.post(
    "",
    response_model=list[MessageResponse],
)
def send_message(
    session_id: str,
    payload: MessageCreate,
    db: Session = Depends(get_db),
):
    session = (
        db.query(ChatSession)
        .filter(ChatSession.id == session_id)
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found",
        )

    user_message = Message(
        session_id=session_id,
        role="user",
        content=payload.content,
    )

    assistant_message = Message(
        session_id=session_id,
        role="assistant",
        content="Mock response — LLM integration coming next.",
    )

    db.add(user_message)
    db.add(assistant_message)
    db.commit()

    db.refresh(user_message)
    db.refresh(assistant_message)

    return [user_message, assistant_message]

@router.get(
    "",
    response_model=list[MessageResponse],
)
def get_messages(
    session_id: str,
    db: Session = Depends(get_db),
):
    session = (
        db.query(ChatSession)
        .filter(ChatSession.id == session_id)
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found",
        )

    return (
        db.query(Message)
        .filter(Message.session_id == session_id)
        .order_by(Message.created_at.asc())
        .all()
    )