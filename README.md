# AI Agent Platform

![frontend](/frontend.png)
A production-ready AI Agent Platform built with FastAPI, Async
SQLAlchemy, and SQLite.

This system supports: - Multi-Agent Management - Multi-Session
Conversations - Text Messaging - Voice Messaging (Speech-to-Text +
Text-to-Speech) - Persistent Conversation History - Full API Testing
with Postman - Dockerized Deployment

------------------------------------------------------------------------

# Complete Testing & Usage Guide

This section explains EXACTLY how to test every endpoint, what body to
send, and what response to expect.

netstat -ano | findstr LISTENING | findstr :8000
taskkill /PID 12345 /F
uvicorn app.main:app --reload


postman

Base URL: http://localhost:8000

Swagger Docs: http://localhost:8000/docs

------------------------------------------------------------------------

# 🔹 1️⃣ Create Agent

Endpoint: POST /agents/

Body (JSON): 
```json
{ 
  "name": "Math Tutor", 
  "system_prompt": "You are a helpful math teacher." 
}
```
Expected Response: 
```json
{
  "id": 1,
  "name": "Math Tutor",
  "system_prompt":"...",
  "created_at": "..." 
}
```
------------------------------------------------------------------------

# 🔹 2️⃣ Get All Agents

Endpoint: GET /agents/

No Body Required.

Expected Response: List of agents.

------------------------------------------------------------------------

# 🔹 3️⃣ Create Session

Endpoint: POST /agents/{agent_id}/sessions/

Example: POST /agents/1/sessions/

write the agent id

No Body Required.

Expected Response: 
```json
{ 
  "id": 1, 
  "agent_id": 1, 
  "created_at": "..." 
}
```

------------------------------------------------------------------------

# 🔹 4️⃣ Get Sessions for Agent

Endpoint: GET /agents/{agent_id}/sessions/

Example: GET /agents/1/sessions/

------------------------------------------------------------------------

# 🔹 5️⃣ Send Text Message

Endpoint: POST /sessions/{session_id}/messages/

Example: POST /sessions/1/messages/

write session id

Body (JSON): 
```json
{ 
  "content": "Explain Pythagoras theorem."
}
```
Expected Flow: 1. User message stored 2. Full session history retrieved
3. AI response generated 4. AI response stored 5. AI response returned

Expected Response: 
```json
{ 
  "id": 2, 
  "session_id": 1, 
  "role": "assistant",
  "content": "...", 
  "created_at": "..." 
}
```
------------------------------------------------------------------------

# 🔹 6️⃣ Send Voice Message

Endpoint: POST /sessions/{session_id}/messages/voice

Example: POST /sessions/1/messages/voice

IMPORTANT:

Body Type → form-data

Key: audio Type: File Value: Upload .mp3 file

DO NOT use raw JSON. DO NOT use binary. The key MUST be named "audio".

Expected Flow: 1. Audio received 2. Speech converted to text 3. Message
stored 4. AI response generated 5. Text converted to speech 6. Audio
stream returned

Response: Streaming audio (audio/mpeg)

------------------------------------------------------------------------


---



# Automated Testing (pytest)

The project includes a full test suite located in the `tests/` directory.

---

## Covered Test Files

- test_agents.py  
- test_sessions.py  
- test_messages.py  
- test_messages_voice.py  

---

## ▶ Run Tests

From project root:

```bash
pytest
````

---

## ▶ Run with Verbose Output

```bash
pytest -v
```


## ✔ What Is Tested?

* Agent creation & retrieval
* Session creation & listing
* Text message workflow
* Voice message endpoint
* Database interactions
* API response validation

---

## Test Configuration

* Tests use isolated database configuration
* Managed through `conftest.py`
* Each test runs independently
* No impact on production database






# 📂 Project Structure



````
ai-agent-platform/
│
├── .dockerignore
├── .env
├── ai_agent.db
├── docker-compose.yml
├── Dockerfile
├── front.html
├── README.md
├── requirements.txt
├── check_tables.py
│
├── app/
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   │
│   ├── routers/
│   │   ├── agents.py
│   │   ├── messages.py
│   │   └── sessions.py
│   │
│   └── services/
│       ├── openai_service.py
│       └── voice_service.py
│
└── tests/
    ├── conftest.py
    ├── test_agents.py
    ├── test_sessions.py
    ├── test_messages.py
    └── test_messages_voice.py

````







# Postman Complete Testing Workflow


---

## 1️⃣ Setup Environment

1. Open Postman.
2. Create a new environment.
3. Add a variable:

| Key     | Value                 |
|---------|---------------------|
| baseUrl | http://localhost:8000 |

4. Select this environment when running requests.

---

## 2️⃣ API Endpoints & Steps

### **1. List Agents (GET)**

- **Endpoint:** `{{baseUrl}}/agents`
- **Purpose:** Retrieve the list of all agents.
- **Steps in Postman:**
  1. Create a new GET request in the collection.
  2. Enter the endpoint above.
  3. Click **Send**.
  4. Check the response for all available agents.

---

### **2. Create Agent (POST)**

- **Endpoint:** `{{baseUrl}}/agents`
- **Purpose:** Create a new agent.
- **Body (JSON):**
```json
{
  "name": "Agent Name",
  "description": "Agent Description"
}
```
- **Steps in Postman:**
  1. Create a new POST request.
  2. Select Body → raw → JSON.
  3. Paste the JSON above and customize the agent info.
  4. Click **Send**.
  5. Response will contain the created agent details.

---

### **3. Create Session (GET)**

- **Endpoint:** `{{baseUrl}}/sessions/create?agent_id=<agent_id>`
- **Purpose:** Start a new session for an agent.
- **Steps in Postman:**
  1. Create a new GET request.
  2. Replace `<agent_id>` with the ID from Create Agent response.
  3. Click **Send**.
  4. Response will contain `session_id`.

---

### **4. Send Message (GET)**

- **Endpoint:** `{{baseUrl}}/message/send?session_id=<session_id>&message=Hello`
- **Purpose:** Send a text message to the session.
- **Body (JSON):**
```json
{
  "content": "Hello!"
}
```
- **Steps in Postman:**
  1. Create a GET request.
  2. Replace `<session_id>` with the ID from Create Session.
  3. Replace `message` query with your text.
  4. Click **Send**.
  5. Response will contain the agent’s reply.

---

### **5. Send Voice (POST)**

- **Endpoint:** `{{baseUrl}}/voice/send`
- **Purpose:** Send an audio message to the agent.
- **Steps in Postman:**
  1. Create a POST request.
  2. Go to Body → form-data.
  3. Add key: `audio` → type: File → choose your audio file.
  4. Add key: `session_id` → type: Text → the session ID.
  5. Click **Send**.
  6. Response will contain transcription or agent reply.

---

## 3️⃣ Full Postman Workflow

1. Create Environment → set `baseUrl`.
2. Create Collection with requests in this order:
   - Create Agent
   - Create Session
   - Send Text Message
   - Send Voice Message
3. Run requests in sequence to test the full flow.

---

🔗 **Postman Share Link:**  
[Access the collection here](https://s-sama-yousef-1804038.postman.co/workspace/Sama-Yousef-'s-Team's-Workspace~9188c577-4084-4f43-8515-d967ad012a82/collection/52777735-f59a20c4-2d9e-4781-9aed-b192d0dc8019?action=share&creator=52777735&active-environment=52777735-74778fad-5a8d-40c1-9cc1-6d825277318f&live=9owk6lap8c)

------------------------------------------------------------------------

# 🐳 Docker Setup (Full Explanation)

## 1️⃣ Build Docker Image

docker build -t ai-agent .

## 2️⃣ Run Container

docker run -p 8000:8000 ai-agent

Server will be available at: http://localhost:8000

------------------------------------------------------------------------

# 🐳 Dockerfile Recommended Structure

FROM python:3.11

WORKDIR /app

COPY requirements.txt . RUN pip install --no-cache-dir -r
requirements.txt

COPY . .

CMD \["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"\]

------------------------------------------------------------------------

# 🔐 Environment Variables

Create .env file:

OPENAI_API_KEY=your_api_key_here

------------------------------------------------------------------------

# Database

Default: SQLite (ai_agent.db)

No external database required. Data persists inside container unless
volume is mounted.

Optional Volume Example:

docker run -p 8000:8000 -v \$(pwd):/app ai-agent

------------------------------------------------------------------------

# 📈 Architecture Summary

Agent → ChatSession → Message

Routers: - agents.py - sessions.py - messages.py

Services: - openai_service.py - voice_service.py

Async database handling via SQLAlchemy AsyncSession.

------------------------------------------------------------------------

# Final Project Capabilities

# Feature Status

| Feature                 | Status |
|-------------------------|--------|
| Agent CRUD              | ✅     |
| Session Management      | ✅     |
| Text Messaging          | ✅     |
| Voice Messaging         | ✅     |
| AI Integration          | ✅     |
| Async Architecture      | ✅     |
| Database Persistence    | ✅     |
| Postman Test Flow       | ✅     |
| Docker Deployment       | ✅     |





