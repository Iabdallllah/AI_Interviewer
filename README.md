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

**Voxora** is an advanced real-time AI-powered interview coaching platform designed to simulate professional HR and technical interviews. Built with state-of-the-art Large Language Models (LLMs) and Speech-to-Text processing, Voxora delivers realistic mock interviews that help candidates practice, improve their communication skills, and build confidence before real interviews.

The platform combines conversational AI, voice interaction, and intelligent feedback to create a personal interview coach that adapts to each candidate's CV and target job description.

---

# ✨ Features

### 🎯 Dynamic Language Adaptation
Automatically detects the required language from the job description and conducts the interview accordingly.
- **Supported Languages:** Arabic, English, German

### 🎙️ Real-Time Voice Interaction
- Real-time voice-based conversations
- Responsive audio processing powered by Web Audio API
- Low-latency Speech-to-Text and Text-to-Speech communication

### 🤖 AI Interview Coaching
Built with **LangChain** and **LangGraph** to:
- Maintain conversational context throughout the interview
- Analyze uploaded CVs (PDF/TXT)
- Understand the target job description
- Generate personalized HR and technical interview questions
- Adapt follow-up questions based on candidate responses
- Simulate realistic interview scenarios

### 📊 Comprehensive Performance Evaluation
After every interview session, Voxora provides:
- Fluency assessment
- Grammar evaluation
- Communication analysis
- Technical and behavioral feedback
- Strengths & improvement areas
- Overall interview score (out of 10)

### 🎨 Modern Enterprise UI
- Glassmorphism interface design
- Dynamic audio-reactive holographic orb
- Smooth conversational experience
- Responsive modern design
- Continuous conversation mode (no push-to-talk needed)

---

# 🛠️ Technologies Used

| Category | Technologies |
|----------|--------------|
| **Backend** | FastAPI, Uvicorn |
| **AI & LLM** | Groq API, Llama-3.3-70B-Versatile |
| **AI Orchestration** | LangChain, LangGraph |
| **Speech Processing** | Groq Whisper (STT), gTTS (TTS) |
| **Frontend** | HTML5, CSS3, JavaScript, Web Audio API |
| **Deployment** | Vercel (Serverless) |
| **Language** | Python 3.11+ |

---

# ⚙️ Installation

## Prerequisites
- Python 3.11+
- Groq API Key (get one at [console.groq.com](https://console.groq.com))

## Local Setup

```bash
# Clone the repository
git clone https://github.com/iabdallllah/AI_Interviewer.git
cd AI_Interviewer

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variable
export GROQ_API_KEY=your_groq_api_key_here

# Run the application
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000` in your browser.

---

# 🚀 Usage

1. **Launch the application** - Run the server and open the web interface
2. **Configure Interview** - Click "Configure" and enter:
   - Job Description (paste the target role description)
   - Candidate CV (optional - upload PDF or TXT)
3. **Start Interview** - Press "Start" to begin the mock interview
4. **Answer Questions** - Speak naturally; Voxora listens continuously and auto-detects when you finish
5. **Receive Feedback** - Get instant AI-powered evaluation and detailed report

### Keyboard Shortcuts
- `Space` - Interrupt AI while it's speaking
- `Escape` - End interview / Close settings

---

# 📸 Demo

### Live Demo
🔗 [https://voxorai.vercel.app](https://voxorai.vercel.app) *(Replace with your actual Vercel deployment URL)*

### Screenshots
*Add screenshots here showing:*
- Interview setup modal
- Main interview interface with holographic orb
- Chat history with message bubbles
- Evaluation results

---

# 📈 Results

- ✅ **Real-time voice conversation** with sub-second latency
- ✅ **Multi-language support** (Arabic, English, German) with automatic detection
- ✅ **CV-aware interviewing** - questions tailored to candidate's experience
- ✅ **Context-aware follow-ups** using LangGraph state management
- ✅ **Instant evaluation** with detailed scoring across multiple dimensions
- ✅ **Serverless deployment** on Vercel (free tier, no credit card required)
- ✅ **Continuous conversation** - no push-to-talk buttons needed

---

# 🔮 Future Improvements

* **Emotion & Sentiment Analysis** - Detect candidate confidence, stress, enthusiasm
* **AI Voice Personalization** - Multiple voice options, speed/pitch control
* **Interview History & Progress Tracking** - Dashboard with session history and improvement trends
* **Multi-Session Analytics** - Long-term skill development insights
* **ATS Integration** - Export evaluation reports in ATS-compatible formats
* **Recruiter Dashboard** - Team collaboration features for hiring managers
* **Personalized Learning Recommendations** - AI-suggested resources based on weaknesses
* **Interview Difficulty Levels** - Junior, Mid, Senior, Principal tracks
* **Offline Mode** - Local model support via Ollama/LM Studio

---

# 📚 About the Challenge

This project was developed as part of the [**Tips Hindawi**](https://www.tipshindawi.com/) **Challenge (June–July) 2026**.

[Tips Hindawi](https://www.tipshindawi.com/) is the internships department of [**Edrak for Ai**](https://edrak4ai.com/en), and the challenge encourages participants to build real-world projects, apply practical skills, and showcase their work through GitHub.

For more information about the challenge, training programs, and upcoming batches, visit the official [Tips Hindawi](https://www.tipshindawi.com/) website.

---

# 📄 License

This project is shared for educational and portfolio purposes.

---

# 🔗 Connect

<div align="center">
  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/abdallllah)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/iabdallllah)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:abdallah.khalifa@proton.me)

</div>

---

<div align="center">
  <sub>Built with ❤️ by <strong>Abdallah Ahmed Khalifa</strong> for the <a href="https://www.tipshindawi.com/">Tips Hindawi Challenge 2026</a></sub>
</div>