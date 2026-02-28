import pytest

@pytest.mark.asyncio
async def test_send_message(client):
    
    agent_resp = await client.post("/agents/", json={
        "name": "Message Agent",
        "system_prompt": "You reply messages."
    })
    agent_id = agent_resp.json()["id"]
    session_resp = await client.post(f"/agents/{agent_id}/sessions/")
    session_id = session_resp.json()["id"]

    
    msg_resp = await client.post(f"/sessions/{session_id}/messages/", json={
        "content": "Hello AI"
    })
    data = msg_resp.json()   
    print("Response content:", data)  
    assert msg_resp.status_code == 200
    data = msg_resp.json()
    assert data["role"] == "assistant"
    assert "content" in data