
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY:
    try:
        import openai
        from openai import RateLimitError, OpenAIError
        openai.api_key = OPENAI_API_KEY
    except Exception as e:
        print("⚠️ OpenAI import error:", e)
        openai = None
else:
    openai = None  


async def generate_chat_response(system_prompt: str, messages: list[dict], model: str = "gpt-3.5-turbo"):

    full_messages = [{"role": "system", "content": system_prompt}] + messages

    if not openai:
        return "⚠️ AI service not configured. This is a mock response.:::::::"

    try:
        response = openai.chat.completions.create(
            model=model,
            messages=full_messages,
            temperature=0.7,
        )
        return response.choices[0].message.content

    except (RateLimitError, OpenAIError, Exception) as e:
        print("⚠️ OpenAI Error:", str(e))
        return "⚠️ AI service temporarily unavailable. This is a mock response.:::"



async def test_usage():
    messages = [{"role": "user", "content": "Hello AI, how are you?"}]
    response = await generate_chat_response("You are a helpful assistant.", messages)
    print("Response:", response)

