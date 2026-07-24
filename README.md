# Voxora

### *Your Personal AI Interview Coach.*

An advanced real-time AI-powered interview coaching platform designed to simulate professional HR and technical interviews.

Voxora leverages state-of-the-art Large Language Models (LLMs) and Speech-to-Text processing to deliver realistic mock interviews, helping candidates practice, improve their communication skills, and build confidence before real interviews.

---

## Live Demo

[Insert Your Live Deployment Link Here]

---

# Key Features

## Dynamic Language Adaptation

Automatically detects the required language from the job description and conducts the interview accordingly.

Supported languages include:

- German
- English
- Arabic

---

## Real-Time Voice Interaction

- Real-time voice-based conversations.
- Responsive audio processing powered by the Web Audio API.
- Low-latency Speech-to-Text and Text-to-Speech communication.

---

## AI Interview Coaching

Built with LangChain and LangGraph to:

- Maintain conversational context.
- Analyze uploaded CVs (PDF/TXT).
- Understand the target job description.
- Generate personalized HR and technical interview questions.
- Adapt follow-up questions based on candidate responses.
- Simulate realistic interview scenarios.

---

## Comprehensive Performance Evaluation

After every interview session, Voxora provides:

- Fluency assessment.
- Grammar evaluation.
- Communication analysis.
- Technical and behavioral feedback.
- Strengths & improvement areas.
- Overall interview score (out of 10).

---

## Modern Enterprise UI

Features include:

- Glassmorphism interface.
- Dynamic audio-reactive holographic orb.
- Smooth conversational experience.
- Responsive modern design.

---

# Tech Stack

## Backend

- FastAPI

## AI & LLM

- Groq API
- Llama-3-70B-Versatile

## AI Orchestration

- LangChain
- LangGraph

## Speech Processing

### Speech-to-Text

- Groq Whisper

### Text-to-Speech

- gTTS

## Frontend

- HTML5
- CSS3
- JavaScript
- Streamlit
- Web Audio API

---

# Project Structure

```text
hr_agent/
│
├── app/
│   ├── __init__.py
│   ├── graph.py       # LangGraph workflow and interview logic
│   ├── main.py        # FastAPI server and REST endpoints
│   └── ui.py          # Streamlit UI
│
├── .env
├── requirements.txt
└── README.md
```

---

# Installation

## Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

cd hr_agent
```

---

## Create a Virtual Environment

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
```

---

# Run the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

---

# Usage

1. Launch the application.
2. Upload your CV (PDF/TXT).
3. Paste the target Job Description.
4. Start your mock interview.
5. Answer questions using your microphone.
6. Receive instant AI-powered feedback and a detailed evaluation report.

---

# Future Roadmap

- Emotion and sentiment analysis.
- AI voice personalization.
- Interview history and progress tracking.
- Multi-session analytics dashboard.
- ATS integration.
- Recruiter dashboard.
- Personalized learning recommendations.
- Interview difficulty levels.

---

## Why Voxora?

Voxora is more than an AI interviewer—it's your personal interview coach. By combining conversational AI, voice interaction, and intelligent feedback, it helps candidates practice realistically, identify weaknesses, and walk into interviews with confidence.
