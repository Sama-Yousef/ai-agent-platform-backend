

import logging
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..database import AsyncSessionLocal
from .. import models, schemas
from ..services.openai_service import generate_chat_response
from ..services.voice_service import speech_to_text, text_to_speech

router = APIRouter(
    prefix="/sessions/{session_id}/messages",
    tags=["Messages"]
)

logging.basicConfig(level=logging.INFO)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


# ==============================
# 📩 TEXT MESSAGE ENDPOINT
# ==============================
@router.post("/", response_model=schemas.MessageResponse)
async def send_message(
    session_id: int,
    message: schemas.MessageCreate,
    db: AsyncSession = Depends(get_db)
):
    logging.info(f"Received message for session {session_id}: {message.content}")

    result = await db.execute(
        select(models.ChatSession).where(models.ChatSession.id == session_id)
    )
    chat_session = result.scalar_one_or_none()

    if not chat_session:
        raise HTTPException(status_code=404, detail="Session not found")

    user_message = models.Message(
        session_id=session_id,
        role="user",
        content=message.content
    )
    db.add(user_message)
    await db.commit()

    result = await db.execute(
        select(models.Message).where(models.Message.session_id == session_id)
    )
    history = result.scalars().all()

    formatted_messages = [
        {"role": msg.role, "content": msg.content}
        for msg in history
    ]

    agent = await db.get(models.Agent, chat_session.agent_id)

    try:
        ai_response_text = await generate_chat_response(
            agent.system_prompt,
            formatted_messages
        )
    except Exception as e:
        logging.error(f"OpenAI error: {e}", exc_info=True)
        ai_response_text = "⚠️ AI service unavailable (mock response)."

    ai_message = models.Message(
        session_id=session_id,
        role="assistant",
        content=ai_response_text
    )
    db.add(ai_message)
    await db.commit()
    await db.refresh(ai_message)

    return ai_message



@router.post("/voice")
async def send_voice_message(
    session_id: int,
    audio: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    logging.info(f"Voice message received for session {session_id}")

    
    result = await db.execute(
        select(models.ChatSession).where(models.ChatSession.id == session_id)
    )
    chat_session = result.scalar_one_or_none()

    if not chat_session:
        raise HTTPException(status_code=404, detail="Session not found")

    
    try:
        user_text = await speech_to_text(audio)
    except Exception as e:
        logging.error(f"STT error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Speech-to-text failed")

    user_message = models.Message(
        session_id=session_id,
        role="user",
        content=user_text
    )
    db.add(user_message)
    await db.commit()

    result = await db.execute(
        select(models.Message).where(models.Message.session_id == session_id)
    )
    history = result.scalars().all()

    formatted_messages = [
        {"role": msg.role, "content": msg.content}
        for msg in history
    ]

    agent = await db.get(models.Agent, chat_session.agent_id)

    # Generate AI response
    try:
        ai_response_text = await generate_chat_response(
            agent.system_prompt,
            formatted_messages
        )
    except Exception:
        ai_response_text = "⚠️ AI voice response (mock)."

    ai_message = models.Message(
        session_id=session_id,
        role="assistant",
        content=ai_response_text
    )
    db.add(ai_message)
    await db.commit()

    try:
        audio_bytes = await text_to_speech(ai_response_text)
    except Exception as e:
        logging.error(f"TTS error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Text-to-speech failed")

    return StreamingResponse(
        iter([audio_bytes]),
        media_type="audio/mpeg"
    )

