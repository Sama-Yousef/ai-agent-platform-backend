from fastapi import FastAPI
from .database import engine, Base
from . import models
from .routers import agents
from .routers import sessions
from dotenv import load_dotenv
from .routers import messages
import os

load_dotenv()
print("kay:    ",os.getenv("OPENAI_API_KEY"))
app = FastAPI()


app.include_router(agents.router)
app.include_router(sessions.router)
app.include_router(messages.router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"message": "AI Agent Platform Running"}