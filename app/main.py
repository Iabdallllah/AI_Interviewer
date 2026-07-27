import os
import json
import io
import base64
import traceback
from dotenv import load_dotenv

load_dotenv(override=True)

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from app.graph import interview_app
from groq import Groq
from gtts import gTTS

app = FastAPI(title="Voxora")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    clean_text = text.replace("[INTERVIEW_CONCLUDED]", "").strip()
    text_lower = clean_text.lower()
    
    if any('\u0600' <= c <= '\u06FF' for c in clean_text):
        lang = 'ar'
    elif any(c in text_lower for c in ['ä', 'ö', 'ü', 'ß']) or any(word in text_lower.split() for word in ['und', 'der', 'die', 'das', 'ich', 'ist', 'ein', 'eine', 'zu', 'sie', 'wir', 'guten', 'hallo', 'wie']):
        lang = 'de'
    else:
        lang = 'en'
        
    tts = gTTS(text=clean_text, lang=lang, slow=False)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return base64.b64encode(fp.read()).decode('utf-8')

@app.get("/", response_class=HTMLResponse)
async def get_live_ui():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Voxora</title>
        <style>
            :root {
                --bg-main: #000000; --surface: #0a0a0a; --surface-elevated: #141414;
                --border-subtle: #262626; --text-primary: #ffffff; --text-secondary: #a3a3a3;
                --accent-blue: #3b82f6; --accent-purple: #8b5cf6; --accent-emerald: #10b981; --accent-rose: #ef4444;
            }

            body {
                background-color: var(--bg-main); color: var(--text-primary);
                font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, sans-serif;
                margin: 0; padding: 0; display: flex; flex-direction: column; min-height: 100vh; overflow-x: hidden;
            }

            .header {
                width: 100%; display: flex; justify-content: space-between; align-items: center;
                padding: 20px 30px; box-sizing: border-box; background: linear-gradient(to bottom, rgba(0,0,0,0.9), transparent);
                position: fixed; top: 0; left: 0; z-index: 50;
            }
            
            .brand-container { display: flex; flex-direction: column; gap: 2px; }
            .logo { font-size: 20px; font-weight: 700; letter-spacing: 1px; color: var(--text-primary); }
            .slogan { font-size: 11px; font-weight: 500; color: var(--text-secondary); letter-spacing: 0.5px; }
            
            .setup-btn {
                background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.15);
                color: var(--text-primary); padding: 8px 18px; border-radius: 20px; font-size: 13px; font-weight: 500; cursor: pointer; transition: all 0.2s ease;
            }
            .setup-btn:hover { background: rgba(255, 255, 255, 0.2); transform: translateY(-1px); }

            .main-container {
                flex: 1; width: 100%; max-width: 600px; margin: 0 auto; padding: 100px 20px 100px 20px;
                display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 24px; box-sizing: border-box;
            }

            .setup-modal {
                position: fixed; inset: 0; background: rgba(0, 0, 0, 0.85); backdrop-filter: blur(8px);
                display: flex; align-items: center; justify-content: center; z-index: 100; opacity: 0; pointer-events: none; transition: opacity 0.3s ease;
            }
            .setup-modal.active { opacity: 1; pointer-events: auto; }
            .setup-content {
                background: var(--surface-elevated); border: 1px solid var(--border-subtle); border-radius: 24px;
                padding: 32px; width: 90%; max-width: 480px; max-height: 90vh; overflow-y: auto; 
                transform: translateY(15px) scale(0.98); opacity: 0; transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1); box-shadow: 0 25px 50px -12px rgba(0,0,0,1);
            }
            .setup-modal.active .setup-content { transform: translateY(0) scale(1); opacity: 1; }
            
            .setup-content h2 { margin: 0 0 24px 0; font-size: 20px; font-weight: 500; }
            .input-group { margin-bottom: 20px; }
            .input-group label { display: block; font-size: 13px; color: var(--text-secondary); margin-bottom: 8px; font-weight: 500; }
            
            .row-group { display: flex; gap: 15px; }
            .row-group .input-group { flex: 1; }

            textarea, select {
                width: 100%; background: var(--surface); border: 1px solid var(--border-subtle); color: var(--text-primary);
                border-radius: 12px; padding: 14px; font-size: 14px; box-sizing: border-box; font-family: inherit; transition: all 0.2s ease; outline: none;
            }
            textarea { resize: none; height: 80px; }
            
            select {
                appearance: none; -webkit-appearance: none; -moz-appearance: none;
                background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23a3a3a3' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
                background-repeat: no-repeat; background-position: right 14px center; background-size: 16px;
                padding-right: 40px; cursor: pointer;
            }
            select:hover { border-color: #404040; background-color: #111; }
            textarea:focus, select:focus { border-color: var(--accent-purple); box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.15); }
            select option { background-color: var(--surface-elevated); color: var(--text-primary); padding: 12px; }

            .file-upload-wrapper { position: relative; width: 100%; }
            .file-upload-wrapper input[type="file"] { position: absolute; left: 0; top: 0; opacity: 0; width: 100%; height: 100%; cursor: pointer; }
            .file-upload-btn {
                background: var(--surface); border: 1px dashed var(--border-subtle); color: var(--text-secondary);
                padding: 16px; border-radius: 12px; font-size: 14px; text-align: center; transition: all 0.2s ease;
            }
            .file-upload-wrapper:hover .file-upload-btn { border-color: var(--accent-blue); color: var(--text-primary); background: #111;}
            
            .close-modal {
                width: 100%; border: none; padding: 14px; border-radius: 12px; font-weight: 600; cursor: pointer; font-size: 15px; transition: background 0.2s;
                background: var(--text-primary); color: var(--bg-main); margin-top: 10px;
            }
            .close-modal:hover { background: #e5e5e5; }

            .orb-wrapper { height: 220px; display: flex; align-items: center; justify-content: center; position: relative; cursor: pointer; }
            .orb {
                width: 130px; height: 130px; border-radius: 50%; background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
                position: relative; z-index: 10; transition: transform 0.05s ease-out;
            }
            .orb::before, .orb::after { content: ''; position: absolute; inset: -5px; border-radius: 50%; background: inherit; filter: blur(25px); z-index: -1; opacity: 0.6; transition: all 0.3s ease; }
            .orb::after { filter: blur(45px); opacity: 0.4; inset: -20px; }
            .orb.speaking { background: linear-gradient(135deg, var(--accent-purple), var(--accent-rose), var(--accent-blue)); animation: rotateGradient 4s linear infinite; }
            .orb.speaking::before { filter: blur(35px); opacity: 0.8; }
            .orb.listening { background: linear-gradient(135deg, var(--accent-emerald), var(--accent-blue)); animation: rotateGradient 3s linear infinite; }
            .orb.listening::before { filter: blur(30px); opacity: 0.7; }

            @keyframes rotateGradient { 0% { filter: hue-rotate(0deg); } 100% { filter: hue-rotate(360deg); } }

            .status-text { font-size: 14px; font-weight: 500; color: var(--accent-blue); letter-spacing: 0.5px; height: 20px; transition: color 0.3s ease; text-align: center; }
            
            .transcript-box { 
                width: 100%; font-size: 17px; line-height: 1.7; color: var(--text-primary); text-align: center; 
                min-height: 60px; padding: 0 10px; text-shadow: 0 0 10px rgba(255,255,255,0.1); 
                transition: height 0.3s ease; display: block;
            }
            .stream-word { 
                opacity: 0.3; display: inline; transition: opacity 0.15s ease-in-out; 
            }
            .stream-word.visible { opacity: 1; text-shadow: 0 0 8px rgba(255,255,255,0.4); }

            .control-panel { display: flex; gap: 16px; margin-top: 20px; transition: transform 0.3s ease; }
            .btn { padding: 14px 32px; border-radius: 30px; font-size: 15px; font-weight: 600; cursor: pointer; border: none; transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1); }
            .btn:active:not(:disabled) { transform: scale(0.96); }
            .btn-start { background: var(--text-primary); color: var(--bg-main); }
            .btn-start:hover:not(:disabled) { background: #e5e5e5; }
            .btn-start.active { background: var(--accent-rose); color: white; }

            .credits-footer { position: fixed; bottom: 20px; left: 0; width: 100%; display: flex; flex-direction: column; align-items: center; gap: 10px; z-index: 40; opacity: 0.4; transition: opacity 0.3s ease; pointer-events: auto; }
            .credits-footer:hover { opacity: 1; }
            .credits-text { font-size: 12px; color: var(--text-secondary); letter-spacing: 0.5px; }
            .credits-text strong { color: var(--text-primary); font-weight: 600; }
            .social-links { display: flex; gap: 14px; }
            .social-links a { color: var(--text-secondary); text-decoration: none; transition: color 0.2s ease, transform 0.2s ease; display: flex; align-items: center; justify-content: center; }
            .social-links a:hover { color: var(--text-primary); transform: translateY(-2px); }
            .social-links svg { width: 18px; height: 18px; fill: currentColor; }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="brand-container">
                <div class="logo">Voxora</div>
                <div class="slogan">Your Personal AI Interview Coach</div>
            </div>
            <button class="setup-btn" onclick="toggleSettings(true)">Configure</button>
        </div>

        <div class="setup-modal" id="setupModal">
            <div class="setup-content">
                <h2>Interview Setup</h2>
                
                <div class="input-group">
                    <label>Interviewer Persona</label>
                    <select id="personaInput">
                        <option value="general_hr">General HR (Soft Skills & Culture Fit)</option>
                        <option value="technical_concepts">Technical Lead (Concepts & System Design)</option>
                        <option value="linguistic_assessment">Linguistic Assessment (Language Fluency)</option>
                        <option value="stress_test">Stress Test (Pressure & Crisis Management)</option>
                        <option value="executive_stakeholder">Executive Board (Business & ROI Focus)</option>
                    </select>
                </div>

                <div class="row-group">
                    <div class="input-group">
                        <label>Length</label>
                        <select id="lengthInput">
                            <option value="short">Short (~4 Qs)</option>
                            <option value="medium" selected>Medium (~7 Qs)</option>
                            <option value="long">Long (~10 Qs)</option>
                        </select>
                    </div>
                    <div class="input-group">
                        <label>Difficulty</label>
                        <select id="difficultyInput">
                            <option value="easy">Easy</option>
                            <option value="medium" selected>Medium</option>
                            <option value="hard">Hard</option>
                            <option value="expert">Expert</option>
                        </select>
                    </div>
                </div>

                <div class="input-group">
                    <label>Job Description</label>
                    <textarea id="jdInput" placeholder="ex. Customer Service Agent - AI Engineer..."></textarea>
                </div>
                
                <div class="input-group">
                    <label>Candidate CV (Optional PDF/TXT)</label>
                    <div class="file-upload-wrapper">
                        <div class="file-upload-btn" id="fileLabel">Tap to upload CV</div>
                        <input type="file" id="cvFile" accept=".pdf,.txt" onchange="updateFileName(this)">
                    </div>
                </div>
                <button class="close-modal" onclick="toggleSettings(false)">Done</button>
            </div>
        </div>

        <div class="main-container">
            <div class="orb-wrapper" onclick="interruptAI()"><div class="orb" id="orb"></div></div>
            <div class="status-text" id="status">Ready for interview</div>
            <div class="transcript-box" id="transcript"></div>
            <div class="control-panel">
                <button class="btn btn-start" id="startBtn" onclick="toggleInterview()">Start Interview</button>
            </div>
        </div>

        <div class="credits-footer">
            <div class="credits-text">Crafted by <strong>Abdallah Khalifa</strong></div>
            <div class="social-links">
                <a href="https://www.linkedin.com/in/abdallllah" target="_blank"><svg viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg></a>
                <a href="mailto:abdallah.khalifa@proton.me"><svg viewBox="0 0 24 24"><path d="M0 3v18h24v-18h-24zm6.623 7.929l-4.623 5.712v-9.458l4.623 3.746zm-4.141-5.929h19.035l-9.517 7.713-9.518-7.713zm5.694 7.188l3.824 3.099 3.83-3.104 5.612 6.817h-18.866l5.6-6.812zm9.201-1.451l4.623-3.747v9.463l-4.623-5.716z"/></svg></a>
            </div>
        </div>

        <script>
            let mediaRecorder, audioChunks = [], messages = [], audioContext, analyser, dataArray, globalAnimId;
            let silenceTimer = null;
            let isUserSpeaking = false;
            let isInterviewActive = false;
            let currentAudio = null;
            let micOpenedTime = 0; 
            let shouldEndInterviewAfterAudio = false;
            let consecutiveSpeechFrames = 0; 

            function initAudioContext() {
                if (!audioContext) audioContext = new (window.AudioContext || window.webkitAudioContext)();
                if (audioContext.state === 'suspended') audioContext.resume();
            }

            function playBeep(type) {
                if (!audioContext) return;
                const osc = audioContext.createOscillator();
                const gainNode = audioContext.createGain();
                osc.connect(gainNode); gainNode.connect(audioContext.destination);
                if (type === 'start') {
                    osc.type = 'sine'; osc.frequency.setValueAtTime(600, audioContext.currentTime); osc.frequency.exponentialRampToValueAtTime(800, audioContext.currentTime + 0.1); gainNode.gain.setValueAtTime(0.1, audioContext.currentTime); gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1); osc.start(); osc.stop(audioContext.currentTime + 0.1);
                } else if (type === 'stop') {
                    osc.type = 'sine'; osc.frequency.setValueAtTime(400, audioContext.currentTime); osc.frequency.exponentialRampToValueAtTime(200, audioContext.currentTime + 0.15); gainNode.gain.setValueAtTime(0.1, audioContext.currentTime); gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.15); osc.start(); osc.stop(audioContext.currentTime + 0.15);
                }
            }

            function toggleSettings(show) { 
                const modal = document.getElementById("setupModal");
                if (show) {
                    modal.classList.add("active");
                    if (currentAudio) currentAudio.pause();
                } else {
                    modal.classList.remove("active");
                }
            }
            
            function updateFileName(input) {
                const label = document.getElementById("fileLabel");
                if (input.files?.length > 0) { label.innerText = input.files[0].name; label.style.color = "var(--accent-emerald)"; label.style.borderColor = "var(--accent-emerald)"; }
            }

            function interruptAI() {
                if (isInterviewActive && currentAudio && !currentAudio.paused) {
                    currentAudio.pause(); currentAudio.currentTime = 0; currentAudio = null;
                    if (globalAnimId) cancelAnimationFrame(globalAnimId); 
                    const orb = document.getElementById("orb"); orb.style.transform = 'scale(1)'; orb.className = "orb";
                    document.getElementById("status").style.color = "var(--accent-emerald)";
                    document.getElementById("status").innerText = "Interrupted. Listening...";
                    startContinuousListening();
                }
            }
            
            async function toggleInterview() {
                const startBtn = document.getElementById("startBtn");

                if (isInterviewActive) {
                    isInterviewActive = false;
                    if (silenceTimer) { clearTimeout(silenceTimer); silenceTimer = null; }
                    if (globalAnimId) cancelAnimationFrame(globalAnimId);
                    if (mediaRecorder && mediaRecorder.state === "recording") mediaRecorder.stop();
                    if (currentAudio) { currentAudio.pause(); currentAudio.currentTime = 0; currentAudio = null; }

                    startBtn.innerText = "Start Interview"; startBtn.classList.remove("active");
                    document.getElementById("status").style.color = "var(--text-secondary)";
                    document.getElementById("status").innerText = "Interview Ended manually.";
                    document.getElementById("orb").className = "orb"; document.getElementById("orb").style.transform = "scale(1)";
                    return;
                }

                initAudioContext();
                const jd = document.getElementById("jdInput").value.trim();
                if (!jd) { toggleSettings(true); return; }

                isInterviewActive = true; 
                messages = [];
                shouldEndInterviewAfterAudio = false;
                
                startBtn.innerText = "End Interview"; startBtn.classList.add("active");
                document.getElementById("status").style.color = "var(--text-primary)"; document.getElementById("status").innerText = "Connecting...";
                document.getElementById("transcript").innerHTML = "";

                const fileInput = document.getElementById("cvFile");
                const persona = document.getElementById("personaInput").value;
                const difficulty = document.getElementById("difficultyInput").value;
                const length = document.getElementById("lengthInput").value;

                const formData = new FormData();
                formData.append("job_description", jd);
                formData.append("persona", persona);
                formData.append("difficulty", difficulty);
                formData.append("length", length);
                if (fileInput.files.length > 0) formData.append("cv_file", fileInput.files[0]);

                try {
                    const response = await fetch('/api/start-interview', { method: 'POST', body: formData });
                    const data = await response.json();
                    messages = data.updated_messages;
                    playAudioResponse(data.audio_base64, data.ai_message);
                } catch (err) { 
                    document.getElementById("status").style.color = "var(--accent-rose)"; document.getElementById("status").innerText = "Connection failed"; 
                }
            }

            function startContinuousListening() {
                if (!isInterviewActive) return;
                
                if (silenceTimer) { clearTimeout(silenceTimer); silenceTimer = null; }
                if (globalAnimId) cancelAnimationFrame(globalAnimId);

                navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
                    mediaRecorder = new MediaRecorder(stream); audioChunks = [];
                    const source = audioContext.createMediaStreamSource(stream);
                    analyser = audioContext.createAnalyser(); analyser.fftSize = 256; source.connect(analyser);
                    dataArray = new Uint8Array(analyser.frequencyBinCount);
                    
                    const orb = document.getElementById("orb"); orb.className = "orb listening"; 
                    document.getElementById("status").style.color = "var(--accent-emerald)"; 
                    document.getElementById("status").innerText = "Listening... (Tap Orb to Interrupt AI)";
                    
                    playBeep('start'); 
                    isUserSpeaking = false; 
                    consecutiveSpeechFrames = 0;
                    micOpenedTime = Date.now(); 

                    mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
                    mediaRecorder.onstop = () => {
                        if (globalAnimId) cancelAnimationFrame(globalAnimId); 
                        orb.style.transform = 'scale(1)'; 
                        stream.getTracks().forEach(t => t.stop());
                        if (isInterviewActive && audioChunks.length > 0) sendAudioToServer(new Blob(audioChunks, { type: 'audio/wav' }));
                    };
                    mediaRecorder.start(); reactToAudioAndVAD();
                }).catch(err => alert("Microphone access is required for the interview."));
            }

            function reactToAudioAndVAD() {
                if (!analyser || !isInterviewActive) return;
                
                if (Date.now() - micOpenedTime < 1000) {
                    globalAnimId = requestAnimationFrame(reactToAudioAndVAD);
                    return;
                }

                analyser.getByteFrequencyData(dataArray);
                let maxVal = Math.max(...dataArray); let sum = dataArray.reduce((a, b) => a + b, 0); let avg = sum / dataArray.length;
                let scale = 1 + (Math.max(avg, maxVal * 0.5) / 255) * 0.45;
                document.getElementById("orb").style.transform = `scale(${Math.min(scale, 1.5)})`;

                if (mediaRecorder && mediaRecorder.state === "recording") {
                    const SILENCE_THRESHOLD = 25; 
                    const SILENCE_DELAY = 2500;   

                    if (avg > SILENCE_THRESHOLD) {
                        consecutiveSpeechFrames++;
                        if (consecutiveSpeechFrames > 3) {
                            isUserSpeaking = true;
                            if (silenceTimer) { clearTimeout(silenceTimer); silenceTimer = null; }
                        }
                    } else {
                        consecutiveSpeechFrames = 0;
                        if (isUserSpeaking && !silenceTimer) {
                            silenceTimer = setTimeout(() => { 
                                isUserSpeaking = false; 
                                playBeep('stop'); 
                                mediaRecorder.stop(); 
                            }, SILENCE_DELAY);
                        }
                    }
                }
                globalAnimId = requestAnimationFrame(reactToAudioAndVAD);
            }

            async function sendAudioToServer(blob) {
                document.getElementById("status").style.color = "var(--text-secondary)"; document.getElementById("status").innerText = "Processing...";
                document.getElementById("orb").className = "orb"; 
                
                const jd = document.getElementById("jdInput").value;
                const fileInput = document.getElementById("cvFile");
                const persona = document.getElementById("personaInput").value;
                const difficulty = document.getElementById("difficultyInput").value;
                const length = document.getElementById("lengthInput").value;

                const formData = new FormData();
                formData.append("audio_file", blob, "voice.wav");
                formData.append("job_description", jd);
                formData.append("persona", persona); 
                formData.append("difficulty", difficulty);
                formData.append("length", length);
                if (fileInput.files.length > 0) formData.append("cv_file", fileInput.files[0]);
                formData.append("messages", JSON.stringify(messages));

                try {
                    const response = await fetch('/api/voice-chat', { method: 'POST', body: formData });
                    const data = await response.json();
                    
                    if (data.silence_detected) {
                        document.getElementById("status").style.color = "var(--accent-emerald)"; document.getElementById("status").innerText = "Listening... (Didn't catch that)";
                        startContinuousListening(); return;
                    }

                    messages = data.updated_messages;
                    
                    if (data.ai_message.includes("[INTERVIEW_CONCLUDED]")) {
                        shouldEndInterviewAfterAudio = true;
                    }
                    
                    playAudioResponse(data.audio_base64, data.ai_message);
                } catch (err) { 
                    document.getElementById("status").style.color = "var(--accent-rose)"; document.getElementById("status").innerText = "Error sending message"; 
                }
            }

            function playAudioResponse(base64Str, textMessage) {
                if (!isInterviewActive) return;
                
                if (silenceTimer) { clearTimeout(silenceTimer); silenceTimer = null; }
                if (globalAnimId) cancelAnimationFrame(globalAnimId);

                textMessage = textMessage.replace("[INTERVIEW_CONCLUDED]", "").replace(/\\n/g, " ").replace(/\\s+/g, " ").trim();

                const orb = document.getElementById("orb"); const transcriptBox = document.getElementById("transcript");
                orb.className = "orb speaking"; document.getElementById("status").style.color = "var(--accent-blue)"; document.getElementById("status").innerText = "Interviewer speaking... (Tap to interrupt)";

                transcriptBox.innerHTML = "";
                
                const words = textMessage.split(" ");
                const spanElements = words.map(w => {
                    const span = document.createElement("span"); 
                    span.className = "stream-word"; 
                    span.innerText = w; 
                    transcriptBox.appendChild(span); 
                    transcriptBox.appendChild(document.createTextNode(" "));
                    return span;
                });

                try {
                    const audio = new Audio(URL.createObjectURL(new Blob([Uint8Array.from(atob(base64Str), c => c.charCodeAt(0))], { type: 'audio/mp3' })));
                    currentAudio = audio; 
                    const source = audioContext.createMediaElementSource(audio);
                    analyser = audioContext.createAnalyser(); analyser.fftSize = 128; source.connect(analyser); analyser.connect(audioContext.destination);
                    dataArray = new Uint8Array(analyser.frequencyBinCount);
                    
                    audio.addEventListener('timeupdate', () => {
                        if (audio.duration) {
                            const progress = Math.min(1, (audio.currentTime + 0.75) / audio.duration);
                            spanElements.slice(0, Math.floor(progress * words.length)).forEach(s => s.classList.add("visible"));
                        }
                    });

                    function visualizeSpeaker() {
                        if (!analyser || orb.className !== "orb speaking") return;
                        analyser.getByteFrequencyData(dataArray); let sum = dataArray.reduce((a, b) => a + b, 0); let scale = 1 + ((sum / dataArray.length) / 255) * 0.35;
                        orb.style.transform = `scale(${Math.min(scale, 1.5)})`; globalAnimId = requestAnimationFrame(visualizeSpeaker);
                    }

                    audio.play().then(() => visualizeSpeaker()).catch(() => spanElements.forEach(s => s.classList.add("visible")));
                    
                    audio.onended = () => {
                        if (currentAudio === audio) {
                            currentAudio = null; 
                            if (globalAnimId) cancelAnimationFrame(globalAnimId); 
                            orb.style.transform = 'scale(1)'; orb.className = "orb"; spanElements.forEach(s => s.classList.add("visible"));
                            
                            if (shouldEndInterviewAfterAudio) {
                                isInterviewActive = false;
                                const startBtn = document.getElementById("startBtn");
                                startBtn.innerText = "Start Interview"; startBtn.classList.remove("active");
                                document.getElementById("status").style.color = "var(--accent-emerald)";
                                document.getElementById("status").innerText = "Interview Successfully Concluded.";
                            } else if (isInterviewActive) {
                                startContinuousListening(); 
                            }
                        }
                    };
                } catch (e) { 
                    orb.className = "orb"; spanElements.forEach(s => s.classList.add("visible")); 
                    if (shouldEndInterviewAfterAudio) {
                        isInterviewActive = false;
                        const startBtn = document.getElementById("startBtn");
                        startBtn.innerText = "Start Interview"; startBtn.classList.remove("active");
                        document.getElementById("status").style.color = "var(--accent-emerald)";
                        document.getElementById("status").innerText = "Interview Successfully Concluded.";
                    }
                }
            }
        </script>
    </body>
    </html>
    """

@app.post("/api/start-interview")
async def start_interview(
    job_description: Optional[str] = Form(...), 
    cv_file: Optional[UploadFile] = File(None),
    persona: str = Form("general_hr"),
    difficulty: str = Form("medium"),
    length: str = Form("medium")
):
    try:
        file_text = extract_text_from_file(cv_file)
        final_cv = file_text if file_text else "Candidate has not provided a specific CV."
        current_state = {
            "job_description": job_description, 
            "candidate_cv": final_cv, 
            "messages": [], 
            "persona": persona,
            "difficulty": difficulty,
            "length": length
        }
        result = interview_app.invoke(current_state)
        ai_response = result["messages"][-1]["content"]
        return {"ai_message": ai_response, "updated_messages": result["messages"], "audio_base64": text_to_speech_base64(ai_response)}
    
    except Exception as e:
        traceback.print_exc()  
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/voice-chat")
async def voice_chat_endpoint(
    job_description: Optional[str] = Form(...), 
    cv_file: Optional[UploadFile] = File(None), 
    messages: str = Form("[]"), 
    audio_file: UploadFile = File(...),
    persona: str = Form("general_hr"),
    difficulty: str = Form("medium"),
    length: str = Form("medium")
):
    try:
        file_text = extract_text_from_file(cv_file)
        final_cv = file_text if file_text else "Candidate has not provided a specific CV."
        
        audio_bytes = await audio_file.read()
        temp_filename = "/tmp/temp_audio.wav"
        
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
        
        hallucinations = [
            "", "thank you.", "thank you", "thanks.", "you", "amara.org", "subtitles",
            "uh", "um", "uhh", "umm", "err", "ah", "eh"
        ]
        
        if not user_text or user_text.lower() in hallucinations:
            return {"silence_detected": True}
        
        parsed_messages = json.loads(messages)
        parsed_messages.append({"role": "user", "content": user_text})
        
        current_state = {
            "job_description": job_description, 
            "candidate_cv": final_cv, 
            "messages": parsed_messages, 
            "persona": persona,
            "difficulty": difficulty,
            "length": length
        }
        result = interview_app.invoke(current_state)
        ai_response = result["messages"][-1]["content"]
        
        return {"user_transcription": user_text, "ai_message": ai_response, "updated_messages": result["messages"], "audio_base64": text_to_speech_base64(ai_response)}
    
    except Exception as e:
        traceback.print_exc()  
        raise HTTPException(status_code=500, detail=str(e))
from mangum import Mangum
handler = Mangum(app)
