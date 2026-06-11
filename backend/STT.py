# backend/STT.py

import os
import tempfile
import sounddevice as sd
import soundfile as sf
import numpy as np
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SAMPLE_RATE = 16000
CHANNELS = 1
LANGUAGE = "az"


def record_until_silence(
    silence_threshold: float = 0.02,
    silence_duration: float = 2.0,
    max_duration: float = 120.0
) -> np.ndarray:

    print("🎙️ Danışın  (susanda avtomatik dayanır)")

    chunk_size = int(SAMPLE_RATE * 0.5)
    recorded_chunks = []
    silent_chunks = 0
    max_silent_chunks = int(silence_duration / 0.5)
    max_chunks = int(max_duration / 0.5)

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="float32"
    ) as stream:
        for _ in range(max_chunks):
            chunk, _ = stream.read(chunk_size)
            recorded_chunks.append(chunk.copy())

            volume = np.abs(chunk).mean()

            if volume < silence_threshold:
                silent_chunks += 1
                if silent_chunks >= max_silent_chunks:
                    print("✅ Cavab alındı")
                    break
            else:
                silent_chunks = 0

    return np.concatenate(recorded_chunks, axis=0)

# Groq Whisper
def transcribe(audio: np.ndarray) -> str:
  
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        sf.write(tmp.name, audio, SAMPLE_RATE)
        tmp_path = tmp.name

    try:
        with open(tmp_path, "rb") as audio_file:
            result = client.audio.transcriptions.create(
                model="whisper-large-v3-turbo",
                file=audio_file,
                response_format="text",
                language=LANGUAGE
            )
        text = result.strip()
        print(f"📝 Transkript: {text}")
        return text
    finally:
        os.unlink(tmp_path)

# RECORDING
def listen() -> str:
   
    audio = record_until_silence()

    if audio is None or len(audio) == 0:
        return ""

    return transcribe(audio)