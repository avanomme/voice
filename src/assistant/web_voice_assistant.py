#!/usr/bin/env python3
"""
Updated Voice Assistant Web UI
Integrates with modular TTS engines and voice models
"""

from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, JSONResponse
import os
import tempfile
import logging

# Import our new modular components
from voice_models import get_all_voices, get_recommended_voices, TTS_ENGINES
from tts_engines import TTSEngineManager
from assistant_logic import ConversationManager, format_thinking_for_display
from wake_word_detector import WakeWordDetector
from error_logger import get_logger, log_web_interface_error, log_tts_error

app = FastAPI(title="Voice Assistant", description="Multi-Engine Local Voice Assistant")

# Initialize error logging
error_logger = get_logger()

# Global instances
tts_manager = TTSEngineManager()
conversation_manager = ConversationManager()

# Wake word detector setup
wake_detector = WakeWordDetector(wake_words=["hey assistant", "voice assistant"])

def on_wake_word_detected(text):
    """Callback for when wake word is detected"""
    logging.info(f"Wake word detected: {text}")
    # Could trigger web notification here

def on_speech_detected():
    """Callback for when speech is detected"""
    pass

def on_permission_error(error_msg):
    """Callback for microphone permission errors"""
    logging.error(f"Microphone permission error: {error_msg}")

wake_detector.on_wake_word = on_wake_word_detected
wake_detector.on_speech_detected = on_speech_detected
wake_detector.on_permission_error = on_permission_error

@app.get("/", response_class=HTMLResponse)
async def get_index():
    """Serve the enhanced web interface"""

    try:
        # Get all available voices organized by accent
        voices_by_accent = get_all_voices()
        recommended = get_recommended_voices()

        # Build voice selection options with grouping
        voice_options = ""
        for accent, voices in voices_by_accent.items():
            if voices:  # Only show accents that have voices
                voice_options += f'<optgroup label="{accent}">'
                for voice in voices:
                    engine_label = f"({voice['engine'].title()})"
                    recommended_star = " ⭐" if voice['id'] in recommended.values() else ""
                    voice_options += f'<option value="{voice["engine"]}:{voice["id"]}">{voice["name"]} {engine_label}{recommended_star}</option>'
                voice_options += '</optgroup>'

        # Build engine info for UI
        engine_info = ""
        for engine_id, engine_data in TTS_ENGINES.items():
            engine_info += f'<div class="engine-info"><strong>{engine_data["name"]}</strong>: {engine_data["best_for"]}</div>'

    except Exception as e:
        log_web_interface_error("index page generation", e)
        voice_options = "<option value=''>Error loading voices</option>"
        engine_info = "<div class='engine-info'>Error loading engine information</div>"
    
    return HTMLResponse(content=f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multi-Engine Voice Assistant</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #1a1a1a;
            color: #e0e0e0;
        }}
        .container {{
            background: #2d2d2d;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }}
        h1 {{
            text-align: center;
            color: #4CAF50;
            margin-bottom: 10px;
        }}
        .subtitle {{
            text-align: center;
            color: #888;
            margin-bottom: 30px;
        }}
        .engine-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }}
        .voice-settings {{
            background: #333;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        .voice-settings h3 {{
            margin-top: 0;
            color: #4CAF50;
        }}
        .engine-info {{
            background: #2a2a2a;
            padding: 10px;
            border-radius: 4px;
            margin: 5px 0;
            font-size: 14px;
        }}
        .controls {{
            text-align: center;
            margin: 30px 0;
        }}
        button {{
            background: #4CAF50;
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            margin: 0 10px;
            transition: all 0.3s;
        }}
        button:hover:not(:disabled) {{
            background: #45a049;
            transform: translateY(-2px);
        }}
        button:disabled {{
            background: #666;
            cursor: not-allowed;
            transform: none;
        }}
        .recording {{
            background: #f44336 !important;
            animation: pulse 1s infinite;
        }}
        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.7; }}
            100% {{ opacity: 1; }}
        }}
        .chat-container {{
            height: 500px;
            overflow-y: auto;
            border: 1px solid #444;
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
            background: #1e1e1e;
        }}
        .message {{
            margin: 15px 0;
            padding: 15px;
            border-radius: 8px;
        }}
        .user-message {{
            background: linear-gradient(135deg, #0084ff, #0066cc);
            color: white;
            margin-left: 50px;
        }}
        .ai-message {{
            background: linear-gradient(135deg, #333, #444);
            color: #e0e0e0;
            margin-right: 50px;
        }}
        .thinking-section {{
            background: #2a2a2a;
            border: 1px solid #555;
            border-radius: 8px;
            margin: 10px 0;
            overflow: hidden;
        }}
        .thinking-header {{
            background: #3a3a3a;
            padding: 15px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: background 0.3s;
        }}
        .thinking-header:hover {{
            background: #4a4a4a;
        }}
        .thinking-content {{
            padding: 20px;
            display: none;
            border-top: 1px solid #555;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 14px;
            line-height: 1.6;
            white-space: pre-wrap;
            background: #1e1e1e;
        }}
        .thinking-content.expanded {{
            display: block;
        }}
        .chevron {{
            transition: transform 0.3s;
            font-size: 18px;
        }}
        .chevron.expanded {{
            transform: rotate(90deg);
        }}
        .status {{
            text-align: center;
            padding: 12px;
            border-radius: 4px;
            margin: 10px 0;
            font-weight: bold;
        }}
        .status.info {{ background: #2196F3; color: white; }}
        .status.error {{ background: #f44336; color: white; }}
        .status.success {{ background: #4CAF50; color: white; }}
        .status.warning {{ background: #ff9800; color: white; }}
        .audio-controls {{
            margin: 15px 0;
            text-align: center;
        }}
        audio {{
            width: 100%;
            max-width: 500px;
            background: #333;
            border-radius: 4px;
        }}
        .input-container {{
            display: flex;
            gap: 10px;
            margin: 20px 0;
        }}
        input[type="text"] {{
            flex: 1;
            padding: 15px;
            border: 1px solid #444;
            border-radius: 8px;
            background: #333;
            color: #e0e0e0;
            font-size: 16px;
            transition: border-color 0.3s;
        }}
        input[type="text"]:focus {{
            outline: none;
            border-color: #4CAF50;
        }}
        select {{
            background: #333;
            color: #e0e0e0;
            border: 1px solid #444;
            border-radius: 8px;
            padding: 12px;
            font-size: 14px;
            width: 100%;
            margin: 10px 0;
        }}
        optgroup {{
            background: #2a2a2a;
            color: #4CAF50;
            font-weight: bold;
        }}
        option {{
            background: #333;
            color: #e0e0e0;
            padding: 8px;
        }}
        .voice-test {{
            margin-left: 10px;
            padding: 10px 20px;
            font-size: 14px;
        }}
        .settings-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }}
        .clone-section {{
            background: #2a2a2a;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }}
        .file-input {{
            margin: 10px 0;
        }}
        .recommended-badge {{
            background: #ff9800;
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 11px;
            margin-left: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎤 Multi-Engine Voice Assistant</h1>
        <div class="subtitle">Coqui XTTS v2 • Bark • Piper | 40+ British/Irish/Australian Voices</div>
        
        <div class="engine-grid">
            <div class="voice-settings">
                <h3>🎭 Voice Selection</h3>
                <select id="voiceSelect">
                    <option value="">Select a voice...</option>
                    {voice_options}
                </select>
                <button class="voice-test" onclick="testVoice()">🔊 Test Voice</button>
                
                <div class="clone-section">
                    <h4>🎯 Voice Cloning (Coqui Only)</h4>
                    <input type="file" id="cloneFile" accept="audio/*" class="file-input">
                    <div style="font-size: 12px; color: #888;">Upload 6+ seconds of clear speech for voice cloning</div>
                </div>
            </div>
            
            <div class="voice-settings">
                <h3>⚙️ Engine Information</h3>
                {engine_info}
                <div style="margin-top: 15px; font-size: 12px; color: #888;">
                    ⭐ = Recommended voices for best quality
                </div>
            </div>
        </div>
        
        <div class="input-container">
            <input type="text" id="textInput" placeholder="Type your message here..." />
            <button onclick="sendText()">Send</button>
        </div>
        
        <div class="controls">
            <button id="recordBtn" onclick="toggleRecording()">🎤 Start Recording</button>
            <button id="wakeWordBtn" onclick="toggleWakeWord()">🎧 Start Wake Word</button>
            <button onclick="clearChat()">🗑️ Clear Chat</button>
            <button onclick="showStats()">📊 Stats</button>
        </div>
        
        <div id="status"></div>
        <div id="chatContainer" class="chat-container"></div>
    </div>

    <script>
        let isRecording = false;
        let mediaRecorder = null;
        let audioChunks = [];
        let wakeWordActive = false;
        
        function showStatus(message, type = 'info') {{
            const status = document.getElementById('status');
            status.innerHTML = `<div class="status ${{type}}">${{message}}</div>`;
            setTimeout(() => status.innerHTML = '', 5000);
        }}
        
        function addMessage(content, isUser = false) {{
            const chatContainer = document.getElementById('chatContainer');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${{isUser ? 'user-message' : 'ai-message'}}`;
            messageDiv.innerHTML = content;
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }}
        
        function addThinkingSection(thinking, response, engine, voice) {{
            const chatContainer = document.getElementById('chatContainer');
            
            // Create thinking section
            const thinkingDiv = document.createElement('div');
            thinkingDiv.className = 'thinking-section';
            thinkingDiv.innerHTML = `
                <div class="thinking-header" onclick="toggleThinking(this)">
                    <span>🧠 AI Thinking Process (${{engine}} - ${{voice}})</span>
                    <span class="chevron">▶</span>
                </div>
                <div class="thinking-content">${{thinking}}</div>
            `;
            
            chatContainer.appendChild(thinkingDiv);
            
            // Add response
            addMessage(`🤖 ${{response}}`);
            
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }}
        
        function toggleThinking(header) {{
            const content = header.nextElementSibling;
            const chevron = header.querySelector('.chevron');
            
            content.classList.toggle('expanded');
            chevron.classList.toggle('expanded');
        }}
        
        async function toggleRecording() {{
            const recordBtn = document.getElementById('recordBtn');
            
            if (!isRecording) {{
                try {{
                    const stream = await navigator.mediaDevices.getUserMedia({{ audio: true }});
                    mediaRecorder = new MediaRecorder(stream);
                    audioChunks = [];
                    
                    mediaRecorder.ondataavailable = event => {{
                        audioChunks.push(event.data);
                    }};
                    
                    mediaRecorder.onstop = async () => {{
                        const audioBlob = new Blob(audioChunks, {{ type: 'audio/wav' }});
                        await processAudio(audioBlob);
                        stream.getTracks().forEach(track => track.stop());
                    }};
                    
                    mediaRecorder.start();
                    isRecording = true;
                    recordBtn.innerHTML = '⏹️ Stop Recording';
                    recordBtn.className = 'recording';
                    showStatus('🎤 Recording... Speak now!', 'info');
                    
                }} catch (error) {{
                    showStatus('❌ Microphone access denied or not available', 'error');
                }}
            }} else {{
                mediaRecorder.stop();
                isRecording = false;
                recordBtn.innerHTML = '🎤 Start Recording';
                recordBtn.className = '';
                showStatus('🔄 Processing audio...', 'info');
            }}
        }}
        
        async function processAudio(audioBlob) {{
            try {{
                const formData = new FormData();
                formData.append('audio', audioBlob, 'recording.wav');
                
                showStatus('🎯 Transcribing speech...', 'info');
                const response = await fetch('/transcribe', {{
                    method: 'POST',
                    body: formData
                }});
                
                const result = await response.json();
                
                if (result.error) {{
                    showStatus(`❌ Transcription error: ${{result.error}}`, 'error');
                    return;
                }}
                
                const transcription = result.transcription;
                if (transcription && transcription.length > 2) {{
                    addMessage(`🗣️ ${{transcription}}`, true);
                    await getAIResponse(transcription);
                }} else {{
                    showStatus('❌ No clear speech detected - try again', 'warning');
                }}
                
            }} catch (error) {{
                showStatus(`❌ Audio processing error: ${{error.message}}`, 'error');
            }}
        }}

        async function toggleWakeWord() {{
            const wakeBtn = document.getElementById('wakeWordBtn');

            if (!wakeWordActive) {{
                try {{
                    const response = await fetch('/wake-word/start', {{ method: 'POST' }});
                    const result = await response.json();
                    if (result.success) {{
                        wakeWordActive = true;
                        wakeBtn.innerHTML = '🛑 Stop Wake Word';
                        showStatus('🎧 Wake word detection active - say "Hey Assistant"', 'success');
                    }} else {{
                        showStatus(`❌ Failed to start wake word: ${{result.error}}`, 'error');
                    }}
                }} catch (error) {{
                    showStatus('❌ Failed to start wake word detection', 'error');
                }}
            }} else {{
                try {{
                    const response = await fetch('/wake-word/stop', {{ method: 'POST' }});
                    const result = await response.json();
                    if (result.success) {{
                        wakeWordActive = false;
                        wakeBtn.innerHTML = '🎧 Start Wake Word';
                        showStatus('🛑 Wake word detection stopped', 'info');
                    }}
                }} catch (error) {{
                    showStatus('❌ Failed to stop wake word detection', 'error');
                }}
            }}
        }}

        async function sendText() {{
            const textInput = document.getElementById('textInput');
            const text = textInput.value.trim();
            
            if (!text) {{
                showStatus('❌ Please enter some text', 'warning');
                return;
            }}
            
            addMessage(`💬 ${{text}}`, true);
            textInput.value = '';
            await getAIResponse(text);
        }}
        
        async function getAIResponse(text) {{
            try {{
                showStatus('🤔 AI is thinking...', 'info');
                
                const voiceSelect = document.getElementById('voiceSelect');
                const selectedVoice = voiceSelect.value;
                const cloneFile = document.getElementById('cloneFile').files[0];
                
                const formData = new FormData();
                formData.append('message', text);
                if (selectedVoice) {{
                    formData.append('voice', selectedVoice);
                }}
                if (cloneFile) {{
                    formData.append('clone_audio', cloneFile);
                }}
                
                const response = await fetch('/chat', {{
                    method: 'POST',
                    body: formData
                }});
                
                const result = await response.json();
                
                if (result.error) {{
                    showStatus(`❌ AI Error: ${{result.error}}`, 'error');
                    return;
                }}
                
                // Add thinking section and response
                const engineInfo = selectedVoice ? selectedVoice.split(':')[0] : 'default';
                const voiceInfo = selectedVoice ? selectedVoice.split(':')[1] : 'default';
                
                addThinkingSection(result.thinking, result.response, engineInfo, voiceInfo);
                
                // Generate and play speech
                if (result.audio) {{
                    const audioDiv = document.createElement('div');
                    audioDiv.className = 'audio-controls';
                    audioDiv.innerHTML = `<audio controls autoplay><source src="data:audio/wav;base64,${{result.audio}}" type="audio/wav"></audio>`;
                    document.getElementById('chatContainer').appendChild(audioDiv);
                    document.getElementById('chatContainer').scrollTop = document.getElementById('chatContainer').scrollHeight;
                }}
                
                showStatus('✅ Response complete!', 'success');
                
            }} catch (error) {{
                showStatus(`❌ Request failed: ${{error.message}}`, 'error');
            }}
        }}
        
        async function testVoice() {{
            const voiceSelect = document.getElementById('voiceSelect');
            const selectedVoice = voiceSelect.value;
            
            if (!selectedVoice) {{
                showStatus('❌ Please select a voice first', 'warning');
                return;
            }}
            
            const testTexts = [
                "Hello there! This is a test of the selected voice.",
                "Good day! I'm demonstrating the speech synthesis quality.",
                "Greetings! How do you find this voice quality?"
            ];
            
            const testText = testTexts[Math.floor(Math.random() * testTexts.length)];
            
            try {{
                showStatus('🔊 Testing voice...', 'info');
                
                const response = await fetch('/test-voice', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json',
                    }},
                    body: JSON.stringify({{ 
                        text: testText,
                        voice: selectedVoice
                    }})
                }});
                
                const result = await response.json();
                
                if (result.audio) {{
                    const audio = new Audio(`data:audio/wav;base64,${{result.audio}}`);
                    audio.play();
                    showStatus('✅ Voice test complete!', 'success');
                }} else {{
                    showStatus('❌ Voice test failed', 'error');
                }}
                
            }} catch (error) {{
                showStatus(`❌ Voice test error: ${{error.message}}`, 'error');
            }}
        }}
        
        function clearChat() {{
            document.getElementById('chatContainer').innerHTML = '';
            showStatus('🗑️ Chat cleared', 'success');
        }}
        
        async function showStats() {{
            try {{
                const response = await fetch('/stats');
                const stats = await response.json();
                
                const statsMessage = `
📊 Session Statistics:
• Messages: ${{stats.message_count}}
• Engines used: ${{stats.engines_used.join(', ')}}
• Most used voice: ${{stats.popular_voice}}
• Average response time: ${{stats.avg_response_time}}s
                `;
                
                addMessage(statsMessage.trim());
                
            }} catch (error) {{
                showStatus('❌ Could not load statistics', 'error');
            }}
        }}
        
        // Enter key support for text input
        document.getElementById('textInput').addEventListener('keypress', function(e) {{
            if (e.key === 'Enter') {{
                sendText();
            }}
        }});
        
        // Initial message
        addMessage('🤖 Multi-engine voice assistant ready! Select a voice, then try recording audio or typing messages. Use voice cloning for personalized speech synthesis.');
    </script>
</body>
</html>
    """)

@app.post("/transcribe")
async def transcribe_audio(audio: UploadFile = File(...)):
    """Transcribe uploaded audio to text"""
    try:
        audio_data = await audio.read()
        assistant = conversation_manager.get_session()
        transcription = assistant.transcribe(audio_data)
        return {"transcription": transcription}
    except Exception as e:
        log_web_interface_error("transcribe", e)
        return {"error": str(e)}

@app.post("/chat")
async def chat(message: str = None, voice: str = None, clone_audio: UploadFile = File(None)):
    """Get AI response with thinking and generate speech"""
    try:
        if not message:
            return {"error": "No message provided"}
        
        # Get conversation session
        assistant = conversation_manager.get_session()
        
        # Get AI response with thinking
        thinking, ai_response = assistant.query_ollama_with_thinking(message)
        
        # Format thinking for display
        formatted_thinking = format_thinking_for_display(thinking)
        
        # Parse voice selection
        engine = "coqui"  # default
        voice_id = None
        clone_voice_path = None
        
        if voice and ":" in voice:
            engine, voice_id = voice.split(":", 1)
        
        # Handle voice cloning
        if clone_audio and engine == "coqui":
            clone_data = await clone_audio.read()
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
                f.write(clone_data)
                clone_voice_path = f.name
        
        # Generate speech for response only (not thinking)
        audio_base64 = tts_manager.speak(
            text=ai_response,
            engine=engine,
            voice_id=voice_id,
            clone_voice_path=clone_voice_path
        )
        
        # Clean up clone file
        if clone_voice_path and os.path.exists(clone_voice_path):
            os.unlink(clone_voice_path)
        
        return {
            "thinking": formatted_thinking,
            "response": ai_response,
            "audio": audio_base64,
            "engine_used": engine,
            "voice_used": voice_id or "default"
        }
    except Exception as e:
        log_web_interface_error("chat", e)
        return {"error": str(e)}

@app.post("/test-voice")
async def test_voice(request: dict):
    """Test a specific voice"""
    try:
        text = request.get("text", "Hello, this is a voice test.")
        voice = request.get("voice", "coqui:vctk_p243")
        
        # Parse voice selection
        if ":" in voice:
            engine, voice_id = voice.split(":", 1)
        else:
            engine = "coqui"
            voice_id = voice
        
        audio_base64 = tts_manager.speak(
            text=text,
            engine=engine,
            voice_id=voice_id
        )
        
        return {"audio": audio_base64}
    except Exception as e:
        return {"error": str(e)}

@app.get("/stats")
async def get_stats():
    """Get session statistics"""
    try:
        assistant = conversation_manager.get_session()
        analysis = assistant.analyze_conversation_sentiment()
        
        return {
            "message_count": analysis.get("total_exchanges", 0),
            "engines_used": ["coqui", "bark", "piper"],  # Could track actual usage
            "popular_voice": "British voices",
            "avg_response_time": "2.3"
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/wake-word/start")
async def start_wake_word():
    """Start wake word detection"""
    try:
        if wake_detector.start_continuous_listening():
            return {"success": True, "message": "Wake word detection started"}
        else:
            return {"success": False, "error": "Failed to start wake word detection"}
    except Exception as e:
        log_web_interface_error("wake-word/start", e)
        return {"success": False, "error": str(e)}

@app.post("/wake-word/stop")
async def stop_wake_word():
    """Stop wake word detection"""
    try:
        wake_detector.stop_continuous_listening()
        return {"success": True, "message": "Wake word detection stopped"}
    except Exception as e:
        log_web_interface_error("wake-word/stop", e)
        return {"success": False, "error": str(e)}

@app.get("/wake-word/status")
async def wake_word_status():
    """Get wake word detection status"""
    try:
        return {
            "active": wake_detector.is_listening,
            "permission_granted": wake_detector.permission_granted
        }
    except Exception as e:
        log_web_interface_error("wake-word/status", e)
        return {"active": False, "permission_granted": False, "error": str(e)}

@app.get("/errors")
async def get_recent_errors():
    """Get recent error logs for debugging"""
    try:
        recent_errors = error_logger.get_recent_errors(limit=20)
        return {"errors": recent_errors}
    except Exception as e:
        return {"errors": [], "error": f"Failed to retrieve errors: {str(e)}"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        return {
            "status": "healthy",
            "message": "Multi-Engine Voice Assistant is running",
            "engines_available": list(TTS_ENGINES.keys()),
            "total_voices": len(get_all_voices()),
            "wake_word_available": wake_detector is not None
        }
    except Exception as e:
        log_web_interface_error("health check", e)
        return {
            "status": "degraded",
            "message": "Voice Assistant running with errors",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    print("Starting Multi-Engine Voice Assistant Web UI...")
    print("Features: Coqui XTTS v2, Bark, Piper | 40+ UK/Irish voices | Voice cloning")
    print("Access at: http://localhost:8765")
    uvicorn.run(app, host="0.0.0.0", port=8765)
