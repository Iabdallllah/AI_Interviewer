# 🚀 [Tips Hindawi](https://www.tipshindawi.com/) Challenge (June–July) 2026

> 🏆 This repository is my official submission for the [ **Tips Hindawi** ](https://www.tipshindawi.com/) **Challenge (June–July) 2026**.

## 👤 Participant

| Field            | Value                                |
| ---------------- | ------------------------------------ |
| Full Name        | Abdallah Ahmed Khalifa               |
| Project Name     | Voxora                               |
| GitHub Username  | iabdallllah                          |
| Challenge Batch  | June–July 2026                       |
| Training Program | Large Language Models (LLMs) Program |
| Organization     | [**Edrak for Ai**](https://edrak4ai.com/en)                         |

---

# 📖 Project Overview

**Voxora** is an advanced real-time AI-powered interview coaching platform designed to simulate professional HR and technical interviews. The platform leverages state-of-the-art Large Language Models (LLMs), Speech-to-Text processing, and Text-to-Speech to deliver realistic mock interviews that help candidates practice, improve their communication skills, and build confidence before real interviews.

The system features a fully voice-based conversational interface where candidates interact with an AI interviewer through their microphone. The AI analyzes uploaded CVs, understands job descriptions, and conducts dynamic, adaptive interviews with personalized questions. After each session, candidates receive comprehensive performance evaluations including fluency assessment, grammar evaluation, communication analysis, technical/behavioral feedback, strengths & improvement areas, and an overall interview score out of 10.

---

# ✨ Features

* **Dynamic Language Adaptation** — Automatically detects required language from job descriptions and conducts interviews in Arabic, English, or German
* **Real-Time Voice Interaction** — Low-latency speech-to-text (Groq Whisper) and text-to-speech (gTTS) with Web Audio API for responsive audio processing
* **AI Interview Coaching** — Built with LangChain and LangGraph to maintain conversational context, analyze CVs (PDF/TXT), understand job descriptions, generate personalized questions, and adapt follow-ups based on responses
* **Comprehensive Performance Evaluation** — Post-interview reports covering fluency, grammar, communication, technical/behavioral feedback, strengths, improvement areas, and overall score
* **Modern Enterprise UI** — Glassmorphism interface with dynamic audio-reactive holographic orb, smooth conversational experience, and responsive design
* **Continuous Conversation with VAD** — Voice Activity Detection for hands-free, natural dialogue flow with interruption support
* **Chat History** — Scrollable conversation bubbles showing full interview transcript with speaker labels

---

# 🛠️ Technologies Used

## Backend
* **FastAPI** — High-performance async web framework
* **Uvicorn** — ASGI server for production deployment
* **Mangum** — AWS Lambda adapter for serverless deployment

## AI & LLM
* **Groq API** — Ultra-fast inference for Llama-3.3-70B-Versatile
* **Groq Whisper** — Speech-to-Text transcription (whisper-large-v3)
* **gTTS** — Text-to-Speech synthesis with multi-language support

## AI Orchestration
* **LangChain** — LLM application framework
* **LangGraph** — Stateful multi-agent workflow orchestration

## Speech Processing
* **Web Audio API** — Real-time audio capture, visualization, and playback
* **MediaRecorder API** — Browser-based audio recording

## Frontend
* **Vanilla HTML5/CSS3/JavaScript** — No framework dependencies
* **CSS Custom Properties** — Theming with glassmorphism effects
* **CSS Animations** — Audio-reactive orb with gradient animations

## Document Processing
* **pypdf** — PDF text extraction from uploaded CVs
* **python-multipart** — File upload handling

## Deployment
* **Vercel** — Serverless deployment (Hobby tier, free)
* **GitHub** — Version control and CI/CD integration

---

# ⚙️ Installation

## Prerequisites
* Python 3.10+
* Groq API key (free at [console.groq.com](https://console.groq.com))

## Local Setup

```bash
# Clone the repository
git clone https://github.com/iabdallllah/AI_Interviewer.git
cd AI_Interviewer

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variable
export GROQ_API_KEY=your_groq_api_key_here
# Or create .env file:
echo "GROQ_API_KEY=your_groq_api_key_here" > .env

# Run the application
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000` in your browser.

---

# 🚀 Usage

1. **Launch** the application via `uvicorn app.main:app --reload`
2. **Configure** — Click "Configure" button and enter:
   - **Job Description** (required) — Paste the target role description
   - **CV** (optional) — Upload PDF or TXT file
3. **Start Interview** — Click "Start" to begin
4. **Speak** — The AI interviewer asks the first question. Speak naturally; the system uses Voice Activity Detection (VAD) to auto-detect when you stop speaking
5. **Interact** — Answer questions; the AI adapts follow-ups based on your responses
6. **Interrupt** — Press **Space** anytime to interrupt the AI mid-speech
7. **Complete** — After 8+ questions, receive a comprehensive evaluation report

---

# 📸 Demo

> Add a screenshot or GIF of the interview interface here showing:
> - The glassmorphism UI with holographic orb
> - Chat history with speaker bubbles
> - Configuration modal

*(Demo media to be added)*

---

# 📈 Results

* Successfully deployed on Vercel Hobby tier (free, no credit card required)
* Sub-second Groq inference latency enabling real-time voice conversation
* Accurate multi-language detection (Arabic, English, German) for TTS
* End-to-end interview flow: CV parsing → JD analysis → adaptive questioning → evaluation
* Serverless architecture with automatic scaling

---

# 🔮 Future Improvements

* **Emotion & Sentiment Analysis** — Detect candidate confidence, stress, and engagement from voice tone
* **AI Voice Personalization** — Custom interviewer personas with distinct voices and styles
* **Interview History & Progress Tracking** — Dashboard showing improvement over multiple sessions
* **Multi-Session Analytics** — Comparative reports across different interview attempts
* **ATS Integration** — Export evaluation reports in ATS-compatible formats
* **Recruiter Dashboard** — Team view for hiring managers to review candidate sessions
* **Personalized Learning Recommendations** — AI-generated study plans based on weak areas
* **Interview Difficulty Levels** — Junior, Mid, Senior, and Expert modes with calibrated questions

---

# 📚 About the Challenge

This project was developed as part of the [**Tips Hindawi**](https://www.tipshindawi.com/) **Challenge (June–July) 2026**.

[Tips Hindawi](https://www.tipshindawi.com/) is the internships department of [**Edrak for Ai**](https://edrak4ai.com/en), and the challenge encourages participants to build real-world projects, apply practical skills, and showcase their work through GitHub.

For more information about the challenge, training programs, and upcoming batches, visit the official [Tips Hindawi](https://www.tipshindawi.com/) website.

---

# 📄 License

This project is shared for educational and portfolio purposes.