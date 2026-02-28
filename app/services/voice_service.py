


import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY:
    try:
        from openai import OpenAI, RateLimitError, OpenAIError
        client = OpenAI(api_key=OPENAI_API_KEY)
    except Exception as e:
        print("⚠️ OpenAI import error:", e)
        client = None
else:
    client = None  

async def speech_to_text(file):

    if not client:
        return " Mock transcription: AI service unavailable."

    try:
        transcript = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=file
        )
        return transcript.text

    except (RateLimitError, OpenAIError, Exception) as e:
        print("⚠️ speech_to_text error:", e)
        return "⚠️ Mock transcription: AI service unavailable."

async def text_to_speech(text: str) -> bytes:

    if not client:
        return b" MOCK_AUDIO_BYTES"

    try:
        speech = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=text
        )
        return speech.content

    except (RateLimitError, OpenAIError, Exception) as e:
        print("⚠️ text_to_speech error:", e)
        return b" MOCK_AUDIO_BYTES"