# backend/LLM.py

import os
import time
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-3.1-flash-lite"


def ask(prompt: str, system: str = None, retries: int = 3) -> str:
    """Gemini-yə sual göndər, cavab al"""
    full_prompt = f"{system}\n\n{prompt}" if system else prompt

    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=full_prompt
            )
            return response.text.strip()
        except Exception as e:
            print(f"⚠️ Cəhd {attempt + 1}/{retries}: {e}")
            if attempt < retries - 1:
                time.sleep(3)

    return ""


def ask_with_history(messages: list[dict], system: str = None, retries: int = 3) -> str:
    """Söhbət tarixçəsi ilə Gemini-yə göndər"""
    history = []
    for msg in messages:
        role = "user" if msg["role"] == "user" else "model"
        history.append({
            "role": role,
            "parts": [{"text": msg["content"]}]
        })

    config = {"system_instruction": system} if system else None

    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=history,
                config=config
            )
            return response.text.strip()
        except Exception as e:
            print(f"⚠️ Cəhd {attempt + 1}/{retries}: {e}")
            if attempt < retries - 1:
                time.sleep(3)

    return ""