import pytest

@pytest.mark.asyncio
async def test_create_agent(client):
    response = await client.post("/agents/", json={
        "name": "Test Agent",
        "system_prompt": "You are a test assistant."
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Agent"