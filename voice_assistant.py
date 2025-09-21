#!/usr/bin/env python3
import whisper
import subprocess
import tempfile
import requests
import json
import pyaudio
import wave
import threading
import time
import os

class VoiceAssistant:
    def __init__(self):
        self.whisper_model = whisper.load_model("base")
        self.ollama_url = "http://localhost:11434/api/generate"
        self.piper_model = os.path.expanduser("~/.local/share/piper/voices/en_US-lessac-medium.onnx")
        self.listening = False
        
    def record_audio(self, duration=5):
        """Record audio from microphone"""
        chunk = 1024
        format = pyaudio.paInt16
        channels = 1
        rate = 16000
        
        p = pyaudio.PyAudio()
        stream = p.open(format=format, channels=channels, rate=rate, 
                       input=True, frames_per_buffer=chunk)
        
        print("Recording...")
        frames = []
        for _ in range(0, int(rate / chunk * duration)):
            data = stream.read(chunk)
            frames.append(data)
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            wf = wave.open(f.name, 'wb')
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(format))
            wf.setframerate(rate)
            wf.writeframes(b''.join(frames))
            wf.close()
            return f.name
    
    def transcribe(self, audio_file):
        """Convert speech to text"""
        result = self.whisper_model.transcribe(audio_file)
        return result["text"].strip()
    
    def query_ollama(self, text):
        """Send text to Ollama and get response"""
        payload = {
            "model": "qwen3:latest",
            "prompt": text,
            "stream": False
        }
        response = requests.post(self.ollama_url, json=payload)
        return response.json()["response"]
    
    def speak(self, text):
        """Convert text to speech using Piper"""
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            cmd = ["piper", "--model", self.piper_model, "--output_file", f.name]
            process = subprocess.Popen(cmd, stdin=subprocess.PIPE, text=True)
            process.communicate(input=text)
            
            # Play the audio
            subprocess.run(["aplay", f.name])
            os.unlink(f.name)
    
    def conversation_loop(self):
        """Main conversation loop"""
        print("Voice Assistant Ready! Press Enter to start recording, 'q' to quit")
        
        while True:
            user_input = input("\nPress Enter to record (q to quit): ").strip()
            if user_input.lower() == 'q':
                break
                
            # Record audio
            audio_file = self.record_audio(duration=5)
            
            try:
                # Transcribe
                user_text = self.transcribe(audio_file)
                print(f"You said: {user_text}")
                
                if user_text:
                    # Get AI response
                    ai_response = self.query_ollama(user_text)
                    print(f"AI: {ai_response}")
                    
                    # Speak response
                    self.speak(ai_response)
                    
            except Exception as e:
                print(f"Error: {e}")
            finally:
                os.unlink(audio_file)

if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.conversation_loop()
