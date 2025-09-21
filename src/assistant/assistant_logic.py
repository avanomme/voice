# assistant_logic.py
"""
Voice Assistant Logic and Thinking Engine
Handles conversation processing, thinking generation, and response formatting
"""

import whisper
import requests
import json
import os
import tempfile
from typing import Tuple, Dict, Any, Optional

class VoiceAssistant:
    def __init__(self):
        print("Loading Whisper model...")
        self.whisper_model = whisper.load_model("base")
        self.ollama_url = "http://localhost:11434/api/generate"
        self.conversation_history = []
        print("Voice Assistant initialized")
        
    def transcribe(self, audio_data: bytes) -> str:
        """Convert audio bytes to text using Whisper"""
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            f.write(audio_data)
            temp_path = f.name
            
        try:
            result = self.whisper_model.transcribe(temp_path)
            return result["text"].strip()
        finally:
            os.unlink(temp_path)
    
    def add_to_history(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({"role": role, "content": content})
        
        # Keep last 20 messages to prevent context overflow
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
    
    def query_ollama_with_thinking(self, text: str, model: str = "qwen3:latest") -> Tuple[str, str]:
        """
        Send text to Ollama and get structured thinking + response
        Returns (thinking, response) tuple
        """
        try:
            # Build conversation context
            context_messages = []
            for msg in self.conversation_history[-10:]:  # Last 10 messages for context
                context_messages.append(f"{msg['role']}: {msg['content']}")
            
            context_str = "\n".join(context_messages) if context_messages else ""
            
            # Structured prompt for thinking
            thinking_prompt = f"""Previous conversation context:
{context_str}

Current user message: {text}

Please provide a structured response with your thinking process and final answer. Format your response EXACTLY as follows:

THINKING:
[Show your detailed reasoning process here. Consider the context, analyze the request, think through potential approaches, and explain your reasoning step by step.]

RESPONSE:
[Provide your final, conversational answer here. This should be natural and engaging, as if speaking to the user directly.]

Remember:
- THINKING section should show your internal reasoning
- RESPONSE section should be conversational and natural
- Always include both sections with the exact headers shown above"""
            
            payload = {
                "model": model,
                "prompt": thinking_prompt,
                "stream": False
            }
            
            response = requests.post(self.ollama_url, json=payload, timeout=45)
            response.raise_for_status()
            
            full_response = response.json()["response"]
            
            # Parse thinking and response
            if "THINKING:" in full_response and "RESPONSE:" in full_response:
                try:
                    thinking_part = full_response.split("THINKING:")[1].split("RESPONSE:")[0].strip()
                    response_part = full_response.split("RESPONSE:")[1].strip()
                    
                    # Clean up any remaining formatting
                    thinking_part = thinking_part.replace("```", "").strip()
                    response_part = response_part.replace("```", "").strip()
                    
                except IndexError:
                    # Fallback if parsing fails
                    thinking_part = "Failed to parse thinking section"
                    response_part = full_response.split("RESPONSE:")[-1].strip() if "RESPONSE:" in full_response else full_response
            else:
                # Fallback for unstructured response
                thinking_part = "No structured thinking provided - model may need prompting adjustment"
                response_part = full_response
                
            # Add to conversation history
            self.add_to_history("user", text)
            self.add_to_history("assistant", response_part)
            
            return thinking_part, response_part
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Connection error to Ollama: {str(e)}"
            return error_msg, error_msg
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON response from Ollama: {str(e)}"
            return error_msg, error_msg
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            return error_msg, error_msg
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        
    def get_conversation_summary(self) -> str:
        """Get a summary of the current conversation"""
        if not self.conversation_history:
            return "No conversation history"
        
        summary_parts = []
        for i, msg in enumerate(self.conversation_history[-10:], 1):
            role_emoji = "👤" if msg["role"] == "user" else "🤖"
            summary_parts.append(f"{i}. {role_emoji} {msg['content'][:100]}...")
        
        return "\n".join(summary_parts)
    
    def analyze_conversation_sentiment(self) -> Dict[str, Any]:
        """Analyze the sentiment and engagement of the conversation"""
        if not self.conversation_history:
            return {"sentiment": "neutral", "engagement": "low", "topics": []}
        
        # Simple analysis based on conversation length and content
        user_messages = [msg for msg in self.conversation_history if msg["role"] == "user"]
        assistant_messages = [msg for msg in self.conversation_history if msg["role"] == "assistant"]
        
        analysis = {
            "total_exchanges": len(user_messages),
            "avg_user_length": sum(len(msg["content"]) for msg in user_messages) / len(user_messages) if user_messages else 0,
            "avg_assistant_length": sum(len(msg["content"]) for msg in assistant_messages) / len(assistant_messages) if assistant_messages else 0,
            "engagement": "high" if len(user_messages) > 5 else "medium" if len(user_messages) > 2 else "low"
        }
        
        return analysis

class ConversationManager:
    """Manages multiple conversation sessions and contexts"""
    
    def __init__(self):
        self.sessions = {}
        self.current_session = "default"
        
    def create_session(self, session_id: str) -> VoiceAssistant:
        """Create a new conversation session"""
        self.sessions[session_id] = VoiceAssistant()
        return self.sessions[session_id]
    
    def get_session(self, session_id: str = None) -> VoiceAssistant:
        """Get existing session or create default"""
        if session_id is None:
            session_id = self.current_session
            
        if session_id not in self.sessions:
            self.sessions[session_id] = VoiceAssistant()
            
        return self.sessions[session_id]
    
    def switch_session(self, session_id: str):
        """Switch to a different session"""
        self.current_session = session_id
        if session_id not in self.sessions:
            self.sessions[session_id] = VoiceAssistant()
    
    def list_sessions(self) -> Dict[str, Dict]:
        """List all sessions with basic info"""
        session_info = {}
        for session_id, assistant in self.sessions.items():
            session_info[session_id] = {
                "message_count": len(assistant.conversation_history),
                "is_current": session_id == self.current_session,
                "last_interaction": assistant.conversation_history[-1]["content"][:50] + "..." if assistant.conversation_history else "No messages"
            }
        return session_info
    
    def delete_session(self, session_id: str):
        """Delete a conversation session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            if self.current_session == session_id:
                self.current_session = "default"

# Utility functions for conversation analysis
def extract_keywords(text: str) -> list:
    """Extract key topics from conversation text"""
    # Simple keyword extraction - could be enhanced with NLP libraries
    common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'my', 'your', 'his', 'her', 'its', 'our', 'their'}
    
    words = text.lower().split()
    keywords = [word.strip('.,!?;:') for word in words if len(word) > 3 and word not in common_words]
    
    # Return top keywords by frequency
    word_freq = {}
    for word in keywords:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    return sorted(word_freq.keys(), key=lambda x: word_freq[x], reverse=True)[:10]

def format_thinking_for_display(thinking_text: str) -> str:
    """Format thinking text for better readability in UI"""
    # Add some structure to thinking display
    lines = thinking_text.split('\n')
    formatted_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Highlight questions
        if line.endswith('?'):
            formatted_lines.append(f"❓ {line}")
        # Highlight conclusions
        elif any(word in line.lower() for word in ['therefore', 'so', 'thus', 'conclusion', 'decided', 'determined']):
            formatted_lines.append(f"💡 {line}")
        # Highlight considerations
        elif any(word in line.lower() for word in ['consider', 'think about', 'analyze', 'evaluate']):
            formatted_lines.append(f"🤔 {line}")
        else:
            formatted_lines.append(f"• {line}")
    
    return '\n'.join(formatted_lines)
