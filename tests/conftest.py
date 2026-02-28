import pytest_asyncio
from httpx import AsyncClient
from httpx import ASGITransport
from app.main import app


@pytest_asyncio.fixture(scope="module")
async def client():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as c:
        yield c