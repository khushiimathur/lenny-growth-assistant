from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ChatSession
from app.schemas.session import SessionCreate, SessionResponse


router = APIRouter(
    prefix="/api/sessions",
    tags=["sessions"],
)


@router.post(
    "",
    response_model=SessionResponse,
)
def create_session(
    payload: SessionCreate,
    db: Session = Depends(get_db),
):
    session = ChatSession(
        user_id=payload.user_id,
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session