from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..database import AsyncSessionLocal
from .. import models, schemas

router = APIRouter(prefix="/agents", tags=["Agents"])


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@router.post("/", response_model=schemas.AgentResponse)
async def create_agent(agent: schemas.AgentCreate, db: AsyncSession = Depends(get_db)):
    new_agent = models.Agent(
        name=agent.name,
        system_prompt=agent.system_prompt
    )

    db.add(new_agent)
    await db.commit()
    await db.refresh(new_agent)

    return new_agent


@router.get("/", response_model=list[schemas.AgentResponse])
async def list_agents(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Agent))
    agents = result.scalars().all()
    return agents