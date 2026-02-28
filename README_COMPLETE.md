# 🧠 AI Agent Platform

A production-ready AI Agent Platform built with FastAPI, Async
SQLAlchemy, and SQLite.

This system supports: - Multi-Agent Management - Multi-Session
Conversations - Text Messaging - Voice Messaging (Speech-to-Text +
Text-to-Speech) - Persistent Conversation History - Full API Testing
with Postman - Dockerized Deployment

------------------------------------------------------------------------

# 🚀 Complete Testing & Usage Guide

This section explains EXACTLY how to test every endpoint, what body to
send, and what response to expect.

Base URL: http://localhost:8000

Swagger Docs: http://localhost:8000/docs

------------------------------------------------------------------------

# 🔹 1️⃣ Create Agent

Endpoint: POST /agents/

Body (JSON): { "name": "Math Tutor", "system_prompt": "You are a helpful
math teacher." }

Expected Response: { "id": 1, "name": "Math Tutor", "system_prompt":
"...", "created_at": "..." }

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

Expected Response: { "id": 1, "agent_id": 1, "created_at": "..." }

------------------------------------------------------------------------

# 🔹 4️⃣ Get Sessions for Agent

Endpoint: GET /agents/{agent_id}/sessions/

Example: GET /agents/1/sessions/

------------------------------------------------------------------------

# 🔹 5️⃣ Send Text Message

Endpoint: POST /sessions/{session_id}/messages/

Example: POST /sessions/1/messages/

Body (JSON): { "content": "Explain Pythagoras theorem." }

Expected Flow: 1. User message stored 2. Full session history retrieved
3. AI response generated 4. AI response stored 5. AI response returned

Expected Response: { "id": 2, "session_id": 1, "role": "assistant",
"content": "...", "created_at": "..." }

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

## 🧪 Automated Testing (pytest)

````markdown
# 🧪 Automated Testing (pytest)

The project includes a full test suite located in the `tests/` directory.

---

## 📂 Covered Test Files

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

---

## ▶ Run with Coverage Report

```bash
pytest --cov=app
```

---

## ✔ What Is Tested?

* Agent creation & retrieval
* Session creation & listing
* Text message workflow
* Voice message endpoint
* Database interactions
* API response validation

---

## 🧩 Test Configuration

* Tests use isolated database configuration
* Managed through `conftest.py`
* Each test runs independently
* No impact on production database

````

---

# 📂 Project Structure Section

```markdown
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

```



---




# 🧪 Postman Complete Testing Workflow

1️⃣ Create Environment: Variable: baseUrl = http://localhost:8000

2️⃣ Create Collection: Add requests in this order:

-   Create Agent
-   Create Session
-   Send Text Message
-   Send Voice Message

3️⃣ For Voice: Body → form-data Key → audio Type → File

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

# 📂 Database

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

# 🏁 Final Project Capabilities

  Feature                Status
  ---------------------- --------
  Agent CRUD             ✅
  Session Management     ✅
  Text Messaging         ✅
  Voice Messaging        ✅
  AI Integration         ✅
  Async Architecture     ✅
  Database Persistence   ✅
  Postman Test Flow      ✅
  Docker Deployment      ✅

------------------------------------------------------------------------

# 👩‍💻 Author

Sama Yousef AI / Software Engineer Generative AI Focus
