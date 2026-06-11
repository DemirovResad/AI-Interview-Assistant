# 🤖 AI Interview Assistant

An intelligent voice-based technical interview assistant powered by **Groq Whisper** (STT), **Groq LLaMA** (LLM), and **Gemini TTS** (TTS).

---

## 📁 Project Structure

AI Interview Assistant/
├── backend/
│   ├── STT.py            # Speech-to-Text (Groq Whisper)
│   ├── LLM.py            # Language Model (Groq LLaMA 3.3 70B)
│   ├── TTS.py            # Text-to-Speech (Gemini TTS / gTTS)
│   ├── prompts.py        # All interview prompts
│   ├── interview.py      # Main interview pipeline
│   └── app.py            # CLI test runner
├── frontend/
│   └── streamlit_app.py  # Web UI
├── .env                  # API keys (not committed)
├── .gitignore
└── README.md

---

## 🚀 Features

- 📄 **Vacancy Analyzer** — Extracts skills, seniority, and interview focus from job descriptions
- 🧠 **Question Generator** — Creates 15 tailored interview questions (Easy / Medium / Hard)
- 🎤 **Voice Input** — Candidate answers via microphone (Azerbaijani language support)
- ⚖️ **Answer Evaluator** — Scores answers on technical accuracy, depth, and communication
- 🔄 **Adaptive Questions** — Adjusts difficulty based on previous answer scores
- 📊 **Final Report** — Overall score, hiring recommendation, strengths & weaknesses
- 🌐 **Streamlit UI** — Full web interface with charts and downloadable JSON report

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| STT | Groq Whisper (`whisper-large-v3-turbo`) |
| LLM | Gemini LLM (`gemini-3.1-flash-lite`) |
| TTS | Gemini TTS (`gemini-2.5-flash-preview-tts`) / gTTS |
| UI | Streamlit + Plotly |
| Audio | sounddevice, soundfile |
| Language | Azerbaijani 🇦🇿 |

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-interview-assistant.git
cd ai-interview-assistant
```

### 2. Install dependencies

```bash
pip install groq google-genai sounddevice soundfile numpy \
            python-dotenv streamlit plotly gtts
```

### 3. Create `.env` file

GROQ_API_KEY=your_groq_api_key
GEMINI_API_KEY=your_gemini_api_key

> 🔑 **Groq API key:** [console.groq.com](https://console.groq.com)  
> 🔑 **Gemini API key:** [aistudio.google.com](https://aistudio.google.com)

### 4. Create `.gitignore`

---

## ▶️ Usage

### Web UI (Streamlit)

```bash
cd frontend
/usr/local/bin/python3.12 -m streamlit run streamlit_app.py
```

Then open [http://localhost:8501](http://localhost:8501)

### CLI (Terminal)

```bash
cd backend
python app.py
```

---

## 🔄 Pipeline

Vacancy Upload        →  Paste job description
↓
Vacancy Analyzer      →  Extract skills & seniority       (LLM → JSON)
↓
Question Generator    →  15 questions by difficulty        (LLM → JSON)
↓
Candidate Answer      →  Voice input via microphone        (STT → Text)
↓
Answer Evaluator      →  Score 0–10 with feedback          (LLM → JSON)
↓
Adaptive Generator    →  Adjust next question difficulty   (LLM → JSON)
↓
Final Report          →  Overall score & recommendation    (LLM → JSON)

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

> 💡 **Tip:** Use **Groq** for LLM + STT and **gTTS** for TTS to stay within free limits.

---

## 🔒 Security

- Never commit your `.env` file
- `.env` is already in `.gitignore`
- Rotate API keys if accidentally exposed

---

## 📝 License

MIT License — free to use and modify.# AI-Interview-Assistant
# AI-Interview-Assistant
# AI-Interview-Assistant
# AI-Interview-Assistant
