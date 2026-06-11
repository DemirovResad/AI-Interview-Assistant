# backend/TTS.py

import os
import wave
import tempfile
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-2.5-flash-preview-tts"
VOICE = "Aoede"


def speak(text: str) -> None:
    """Mətni səsə çevir və oxu (Gemini TTS + afplay)"""
    if not text:
        return

    print(f"🔊 Oxunur: {text[:60]}...")

    # Promptu açıq şəkildə TTS üçün formatla
    tts_prompt = f"Read the following text aloud naturally: {text}"

    response = client.models.generate_content(
        model=MODEL,
        contents=tts_prompt,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name=VOICE
                    )
                )
            )
        )
    )

    audio_data = response.candidates[0].content.parts[0].inline_data.data

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        with wave.open(tmp_path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(24000)
            wf.writeframes(audio_data)

        os.system(f"afplay {tmp_path}")
    finally:
        os.unlink(tmp_path)