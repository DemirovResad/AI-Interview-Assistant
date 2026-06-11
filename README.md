# 🤖 AI Interview Assistant

An intelligent voice-based technical interview assistant powered by **Groq Whisper** (STT), **Gemini 3.1 Flash Lite** (LLM), and **Gemini TTS** (TTS). Conducts fully automated technical interviews in **Azerbaijani** 🇦🇿.

---

## 📁 Project Structure

```
AI Interview Assistant/
├── backend/
│   ├── STT.py            # Speech-to-Text (Groq Whisper)
│   ├── LLM.py            # Language Model (Gemini 3.1 Flash Lite)
│   ├── TTS.py            # Text-to-Speech (Gemini TTS)
│   ├── prompts.py        # All interview prompts
│   ├── interview.py      # Main interview pipeline
│   └── app.py            # CLI test runner
├── frontend/
│   └── streamlit_app.py  # Web UI (Streamlit)
├── .env                  # API keys (not committed)
├── .gitignore
└── README.md
```

---

## 🚀 Features

- 📄 **Vacancy Analyzer** — Extracts skills, seniority, and interview focus from job descriptions
- 🧠 **Question Generator** — Creates 15 tailored questions (Easy / Medium / Hard)
- 🎤 **Voice Input** — Candidate answers via microphone in Azerbaijani
- ⚖️ **Answer Evaluator** — Scores answers on technical accuracy, depth, and communication
- 🔄 **Adaptive Questions** — Adjusts difficulty based on previous answer scores
- 📊 **Final Report** — Overall score, hiring recommendation, strengths & weaknesses
- 🌐 **Streamlit UI** — Web interface with charts and downloadable JSON report

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
<<<<<<< HEAD
| STT | Groq Whisper `whisper-large-v3-turbo` |
| LLM | Gemini `gemini-3.1-flash-lite` |
| TTS | Gemini `gemini-2.5-flash-preview-tts` |
=======
| STT | Groq Whisper (`whisper-large-v3-turbo`) |
| LLM | Gemini LLM (`gemini-3.1-flash-lite`) |
| TTS | Gemini TTS (`gemini-2.5-flash-preview-tts`) / |
>>>>>>> cb0f1031307a587056ff85591d053c6005dd6541
| UI | Streamlit + Plotly |
| Audio | sounddevice, soundfile |
| Language | Azerbaijani 🇦🇿 |

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/DemirovResad/AI-Interview-Assistant.git
cd AI-Interview-Assistant
```

### 2. Install dependencies

```bash
pip install groq google-genai sounddevice soundfile numpy \
            python-dotenv streamlit plotly gtts
```

### 3. Create `.env` file

```
GROQ_API_KEY=your_groq_api_key
GEMINI_API_KEY=your_gemini_api_key
```

> 🔑 **Groq API key:** [console.groq.com](https://console.groq.com)
> 🔑 **Gemini API key:** [aistudio.google.com](https://aistudio.google.com)

### 4. Create `.gitignore`

```
.env
__pycache__/
*.pyc
.DS_Store
*.wav
*.mp3
```

---

## ▶️ Usage

### Web UI (Streamlit)

```bash
cd frontend
/usr/local/bin/python3.12 -m streamlit run streamlit_app.py
```

Open [http://localhost:8501](http://localhost:8501)

### CLI (Terminal)

```bash
cd backend
python app.py
```

---

## 🔄 Pipeline

```
1. Vacancy Upload        →  Paste job description
         ↓
2. Vacancy Analyzer      →  Extract skills & seniority       (LLM → JSON)
         ↓
3. Question Generator    →  15 questions by difficulty        (LLM → JSON)
         ↓
4. Candidate Answer      →  Voice input via microphone        (STT → Text)
         ↓
5. Answer Evaluator      →  Score 0–10 with feedback          (LLM → JSON)
         ↓
6. Adaptive Generator    →  Adjust next question difficulty   (LLM → JSON)
         ↓
7. Final Report          →  Overall score & recommendation    (LLM → JSON)
```

---

## 📊 Scoring Guide

| Score | Meaning |
|-------|---------|
| 0–2 | Incorrect answer |
| 3–4 | Very weak understanding |
| 5–6 | Basic understanding |
| 7–8 | Good understanding |
| 9–10 | Excellent with practical knowledge |

---

## 🏷️ Hiring Recommendations

| Overall Score | Recommendation |
|---------------|----------------|
| 90–100 | ✅ Strong Hire |
| 75–89 | ✅ Hire |
| 60–74 | ⚠️ Consider |
| 40–59 | ⚠️ Weak Consider |
| 0–39 | ❌ Reject |

---

## ⚠️ API Rate Limits (Free Tier)

| Service | Limit |
|---------|-------|
| Groq LLM | 1,000 req/day, 6,000 TPM |
| Groq Whisper (STT) | 1,000 req/day |
| Gemini LLM | 1,500 req/day |
| Gemini TTS | 10 req/day |

> 💡 **Tip:** Use **gTTS** instead of Gemini TTS to avoid the 10 req/day limit.

---

## 🔒 Security

- Never commit your `.env` file
- `.env` is already in `.gitignore`
- Rotate API keys if accidentally exposed

---

## 📝 License

MIT License — free to use and modify.
