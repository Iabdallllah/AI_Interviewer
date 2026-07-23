# AI Voice Interviewer

An advanced real-time AI-powered interviewing platform designed to simulate professional HR and technical interviews.

The system leverages state-of-the-art Large Language Models (LLMs) and Speech-to-Text processing to conduct interactive voice interviews, dynamically adapting to the candidate's language, context, and required job description.

---

## Live Demo

[Insert Your Live Deployment Link Here]

---

## Key Features

### Dynamic Language Adaptation

Automatically detects the required language from the job description and conducts the interview accordingly.

Supported examples:
- German
- English
- Arabic

---

### Real-Time Voice Interaction

- Real-time voice-based communication.
- Utilizes Web Audio API for responsive audio processing.
- Provides synchronized Speech-to-Text and Text-to-Speech interaction with minimal latency.

---

### Context-Aware Generation

Built with LangChain and LangGraph to:

- Maintain conversation history.
- Analyze uploaded CV files (PDF/TXT).
- Generate interview questions based on:
  - Candidate experience.
  - Job description requirements.
  - Interview context.

---

### Comprehensive Evaluation

At the end of the interview, the AI provides:

- Fluency assessment.
- Grammar evaluation.
- Communication analysis.
- Professional suitability feedback.
- Overall score out of 10.

---

### Modern Enterprise UI

Features:

- Clean glassmorphism design.
- Dynamic audio-reactive holographic orb.
- Premium interactive interview experience.

---

# Tech Stack

## Backend Framework

- FastAPI

## AI / LLM Capabilities

- Groq API
- Llama-3-70b-versatile

## AI Orchestration

- LangChain
- LangGraph

## Speech Processing

### Speech-to-Text (STT)

- Groq Whisper

### Text-to-Speech (TTS)

- gTTS

## Frontend

- HTML5
- CSS3
- JavaScript
- Web Audio API
- Streamlit

---

# Project Structure

```text
hr_agent/
│
├── app/
│   ├── __init__.py
│   ├── graph.py       # LangGraph state management and LLM prompts
│   ├── main.py        # FastAPI server and core endpoints
│   └── ui.py          # UI components and configurations
│
├── .env               # Environment variables (API Keys)
├── requirements.txt   # Project dependencies
└── README.md          # Documentation
```

---

# Installation & Setup

## Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

cd hr_agent
```

---

## Create and Activate Virtual Environment

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

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

---

# Run the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The application will be available at:

```
http://127.0.0.1:8000
```

---

# Usage

1. Open the application in your browser.

2. Click on "Configure" to enter:
   - Target Job Description.
   - Candidate CV file (PDF/TXT).

3. Click "Start" to begin the interview.

4. The AI interviewer will:
   - Analyze the provided context.
   - Generate relevant interview questions.
   - Listen to candidate responses.
   - Provide real-time feedback.

5. Use the "Speak" button to record answers.

6. Receive a final AI-generated evaluation report.

---

# Future Improvements

- Real-time emotion analysis.
- Advanced voice cloning.
- Multi-candidate comparison dashboard.
- Interview analytics and reporting.
- ATS platform integration.
