from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..database import AsyncSessionLocal
from .. import models, schemas

router = APIRouter(prefix="/agents/{agent_id}/sessions", tags=["Sessions"])


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@router.post("/", response_model=schemas.SessionResponse)
async def create_session(agent_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Agent).where(models.Agent.id == agent_id))
    agent = result.scalar_one_or_none()

    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    new_session = models.ChatSession(agent_id=agent_id)

    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)

    return new_session


@router.get("/", response_model=list[schemas.SessionResponse])
async def list_sessions(agent_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.ChatSession).where(models.ChatSession.agent_id == agent_id)
    )
    sessions = result.scalars().all()

    return sessions