from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.agent.router import detect_intent
from app.database import get_db
from app.knowledge.rag import RAGService
from app.models import ChatSession, Message
from app.schemas.chat import ChatRequest, ChatResponse


router = APIRouter()

rag_service = RAGService()


@router.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):

    # ---------------------------------------
    # 1. Get existing session or create one
    # ---------------------------------------

    if request.session_id:

        session = (
            db.query(ChatSession)
            .filter(
                ChatSession.id == request.session_id
            )
            .first()
        )

        if not session:
            raise HTTPException(
                status_code=404,
                detail="Session not found",
            )

    else:

        session = ChatSession()

        db.add(session)
        db.commit()
        db.refresh(session)

    # ---------------------------------------
    # 2. Load conversation history
    # ---------------------------------------

    previous_messages = (
        db.query(Message)
        .filter(
            Message.session_id == session.id
        )
        .order_by(Message.created_at.asc())
        .limit(10)
        .all()

    )

    history = [
        {
            "role": message.role,
            "content": message.content,
        }
        for message in previous_messages
    ]

    # ---------------------------------------
    # 3. Generate RAG answer
    # ---------------------------------------

    intent = detect_intent(request.message)

    result = rag_service.answer(
        question=request.message,
        history=history,
        top_k=3,
    )

    artifact = None

    if intent in ["markdown", "html", "ship30"]:

        artifact_content = rag_service.generate_artifact(
            artifact_type=intent,
            question=request.message,
            grounded_answer=result["answer"],
        )

        artifact = {
            "type": "markdown" if intent == "ship30" else intent,
            "content": artifact_content,
        }
    # ---------------------------------------
    # 4. Save user message
    # ---------------------------------------

    user_message = Message(
        session_id=session.id,
        role="user",
        content=request.message,
    )

    # ---------------------------------------
    # 5. Save assistant message
    # ---------------------------------------

    assistant_message = Message(
        session_id=session.id,
        role="assistant",
        content=result["answer"],
    )

    db.add(user_message)
    db.add(assistant_message)
    db.commit()

    # ---------------------------------------
    # 6. Return response
    # ---------------------------------------

    return ChatResponse(
        session_id=session.id,
        answer=result["answer"],
        sources=result["sources"],
        artifact=artifact,
    )