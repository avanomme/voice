# Technical Decisions Log

## 2025-09-21
**Initialized Claude Code workflow.**
- Bootstrapped project structure with docs/, agents/, .claude/ directories
- Established modular architecture with voice_models.py, tts_engines.py separation
- Configured multi-engine TTS support (Coqui XTTS v2, Bark, Piper)
- Set up task tracking system with JSON-based workflow

2025-09-21 – Completed Complete XTTS_SPEAKERS definition in voice_models.py (expanded from 3 to 50+ speakers with comprehensive accent coverage and metadata)
2025-09-21 – Completed Wake word & Continuous Chat Initialisation (implemented WebRTC VAD-based wake word detection with microphone permission handling and continuous listening mode)
2025-09-21 – Completed Download missing British Piper voice models (enhanced download_models.py with centralized voice_models.py configuration and added missing British voices)