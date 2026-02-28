from pydantic import BaseModel
from datetime import datetime


class AgentCreate(BaseModel):
    name: str
    system_prompt: str


class AgentUpdate(BaseModel):
    name: str | None = None
    system_prompt: str | None = None


class AgentResponse(BaseModel):
    id: int
    name: str
    system_prompt: str
    created_at: datetime

    class Config:
        from_attributes = True


class SessionCreate(BaseModel):
    pass  


class SessionResponse(BaseModel):
    id: int
    agent_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class MessageCreate(BaseModel):
    content: str


class MessageResponse(BaseModel):
    id: int
    session_id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True