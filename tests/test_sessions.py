import pytest

@pytest.mark.asyncio
async def test_create_session(client):
    agent_resp = await client.post("/agents/", json={
        "name": "Session Agent",
        "system_prompt": "You are a session tester."
    })
    agent_id = agent_resp.json()["id"]

    session_resp = await client.post(f"/agents/{agent_id}/sessions/")
    assert session_resp.status_code == 200
    data = session_resp.json()
    assert data["agent_id"] == agent_id