from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
from app.graph import interview_app
from groq import Groq
from gtts import gTTS
import os
import json
import io
import base64

app = FastAPI(title="Voxora")

groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def extract_text_from_file(file: UploadFile) -> str:
    if not file or not file.filename:
        return ""
    try:
        content = file.file.read()
        if file.filename.endswith('.pdf'):
            try:
                import pypdf
                reader = pypdf.PdfReader(io.BytesIO(content))
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
                return text.strip()
            except:
                return content.decode('utf-8', errors='ignore')
        else:
            return content.decode('utf-8', errors='ignore')
    except:
        return ""

def text_to_speech_base64(text: str) -> str:
    text_lower = text.lower()
    if any('\u0600' <= c <= '\u06FF' for c in text):
        lang = 'ar'
    elif any(c in text_lower for c in ['ä', 'ö', 'ü', 'ß']) or any(word in text_lower.split() for word in ['und', 'der', 'die', 'das', 'ich', 'ist', 'ein', 'eine', 'zu', 'sie', 'wir', 'guten']):
        lang = 'de'
    else:
        lang = 'en'
        
    tts = gTTS(text=text, lang=lang, slow=False)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return base64.b64encode(fp.read()).decode('utf-8')

@app.get("/", response_class=HTMLResponse)
async def get_live_ui():
    templates_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
    html_path = os.path.join(templates_dir, "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Voxorai</h1><p>Template not found</p>"

@app.post("/api/start-interview")
async def start_interview(
    job_description: Optional[str] = Form(...),
    cv_file: Optional[UploadFile] = File(None)
):
    try:
        file_text = extract_text_from_file(cv_file)
        final_cv = file_text if file_text else "Candidate has not provided a specific CV."
        
        current_state = {
            "job_description": job_description,
            "candidate_cv": final_cv,
            "messages": []
        }
        result = interview_app.invoke(current_state)
        ai_response = result["messages"][-1]["content"]
        audio_b64 = text_to_speech_base64(ai_response)
        return {
            "ai_message": ai_response,
            "updated_messages": result["messages"],
            "audio_base64": audio_b64
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/voice-chat")
async def voice_chat_endpoint(
    job_description: Optional[str] = Form(...),
    cv_file: Optional[UploadFile] = File(None),
    messages: str = Form("[]"),
    audio_file: UploadFile = File(...)
):
    try:
        file_text = extract_text_from_file(cv_file)
        final_cv = file_text if file_text else "Candidate has not provided a specific CV."

        ext = os.path.splitext(audio_file.filename or "audio.wav")[1] or ".wav"
        audio_bytes = await audio_file.read()
        temp_filename = f"/tmp/temp_audio{ext}"
        
        with open(temp_filename, "wb") as f:
            f.write(audio_bytes)
            
        with open(temp_filename, "rb") as file:
            transcription = groq_client.audio.transcriptions.create(
                file=(temp_filename, file.read()),
                model="whisper-large-v3",
                response_format="text"
            )
        
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
            
        user_text = transcription.strip()
        
        parsed_messages = json.loads(messages)
        if user_text:
            parsed_messages.append({"role": "user", "content": user_text})
            
        current_state = {
            "job_description": job_description,
            "candidate_cv": final_cv,
            "messages": parsed_messages
        }
        
        result = interview_app.invoke(current_state)
        ai_response = result["messages"][-1]["content"]
        
        audio_b64 = text_to_speech_base64(ai_response)
        
        return {
            "user_transcription": user_text,
            "ai_message": ai_response,
            "updated_messages": result["messages"],
            "audio_base64": audio_b64
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
