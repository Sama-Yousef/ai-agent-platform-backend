import pytest
from unittest.mock import patch

@pytest.mark.asyncio
@patch("app.services.openai_service.generate_chat_response")
async def test_send_voice_message(mock_generate, client):
    
    mock_generate.return_value = "Mocked AI Response"

    
    agent_resp = await client.post("/agents/", json={
        "name": "Voice Agent",
        "system_prompt": "You reply to voice."
    })
    agent_id = agent_resp.json()["id"]
    session_resp = await client.post(f"/agents/{agent_id}/sessions/")
    session_id = session_resp.json()["id"]

    
    files = {"audio": ("test.mp3", b"FAKE AUDIO CONTENT", "audio/mpeg")}
    resp = await client.post(f"/sessions/{session_id}/messages/voice", files=files)
    assert resp.status_code == 200
    assert resp.content  