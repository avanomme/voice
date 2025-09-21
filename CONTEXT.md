# Voice Assistant Project Context

## Overview
Multi-engine local voice assistant focused on British/Irish/Australian accents with comprehensive TTS support, voice cloning capabilities, and GPU-optimized processing. Features 50+ Coqui XTTS speakers, wake word detection, and automated British voice model downloading.

## Technical Architecture

### Core Components
- **TTS Engines**: Coqui XTTS v2, Bark, Piper, Whisper integration
- **Voice Management**: Multi-engine voice configuration with lazy loading
- **Web Interface**: Real-time interaction with thinking display
- **Wake Word Detection**: WebRTC VAD-based continuous listening
- **Model Management**: Automated downloading with centralized configuration
- **GPU Processing**: CUDA 12.9 optimized for AMD 7700x + RTX 5060 Ti

### Key Files
- `src/assistant/voice_models.py` - Complete voice configuration (50+ XTTS speakers)
- `src/assistant/wake_word_detector.py` - Wake word detection and continuous listening
- `src/assistant/web_voice_assistant.py` - Web interface with wake word integration
- `download_models.py` - Enhanced model downloader with centralized config
- `simple_voices.py` - Simplified voice mapping (Piper, Coqui, Bark)
- `voice_assistant.py` - Main assistant executable
- `safe_model_loader.py` - Memory-optimized model loading

### Dependencies
- **Runtime**: Python 3.x, CUDA 12.9, PyTorch
- **TTS**: Coqui TTS, Bark, Piper TTS
- **Audio**: sounddevice, librosa, numpy, pyaudio, webrtcvad
- **Wake Word**: WebRTC VAD, Whisper transcription
- **Web**: FastAPI, uvicorn

## Voice Configuration

### XTTS Speakers (50+ Complete Collection)
**International Voices**: Claribel Dervla, Andrew Chipper, Ana Florence, Damien Black, Sofia Hellen
**British Accents**: Emily, George, Charlotte, Oliver, Isabella, Eleanor, Bernard, Victoria
**Celtic Voices**: Seamus, Siobhan (Irish), Hamish, Fiona (Scottish), Rhys (Welsh)
**Professional**: Narrator, Storyteller, Professor, Guide, Host, Executive, Director
**Specialty**: Echo (AI assistant), Sage, Nova, Atlas, Luna

### Piper (Fast, Reliable) - Auto-Downloadable
- `en_GB_southern_english_female_low` - Vale (Deep British Female) - Default
- `en_GB_cori_medium` - Cori (Northern English)
- `en_GB_jenny_dioco_medium` - Jenny (Southern English)
- `en_GB_alba_medium` - Alba (Scottish)
- `en_GB_northern_english_male_medium` - Northern English Male

### Bark (Emotional Expressions)
- British speakers with [laughs], [sighs], [music] support
- 4 British voice variants (2 male, 2 female)

## Model Management

### Automated Downloading
- **Centralized Configuration**: download_models.py reads from voice_models.py
- **British Voice Focus**: All defined Piper British voices auto-downloaded
- **Progressive Loading**: Whisper → Piper → Coqui → Bark (by size/importance)
- **Fallback Support**: Hardcoded models if configuration fails
- **System Checks**: RAM/GPU verification before large model downloads

### Voice Model Locations
- **Base Directory**: `~/.local/share/voice_models/`
- **Piper Models**: `piper/` subdirectory with .onnx and .json files
- **Coqui Cache**: Managed by TTS library
- **Bark Cache**: Managed by Bark library

## Wake Word Detection

### Features
- **Continuous Listening**: Background VAD-based audio monitoring
- **Wake Words**: "Hey Assistant", "Voice Assistant" (configurable)
- **Permission Handling**: Explicit microphone permission requests
- **Voice Activity Detection**: WebRTC VAD for efficient processing
- **Speech Processing**: Whisper-based wake word transcription

### Integration
- Web interface wake word toggle button
- Automatic conversation initiation on detection
- Permission verification before activation
- Background thread processing with minimal CPU usage

## Project Structure

### Documentation (`docs/`)
- `01-scope.md` - Project goals and technical objectives
- `02-decisions.md` - Architecture decisions and rationale
- `03-tasks.json` - Task tracking and progress

### Source Code (`src/`)
- `assistant/voice_models.py` - Complete voice definitions and metadata
- `assistant/wake_word_detector.py` - Wake word detection system
- `assistant/web_voice_assistant.py` - Web interface with wake word support
- `assistant/` - Core assistant implementation

### Agents (`agents/`)
- Specialized agent definitions for development workflow
- `voice-engine-specialist.md` - TTS engine optimization expert

### Claude Configuration (`.claude/`)
- `commands/` - Workflow slash commands
- Agent command definitions and bootstrapping

## Hardware Targets
- **CPU**: AMD 7700x optimization
- **GPU**: RTX 5060 Ti with CUDA 12.9 Blackwell support
- **OS**: Arch Linux specific optimizations
- **Memory**: GPU memory management for model loading
- **Audio**: WebRTC VAD for efficient wake word processing

## Development Status
- ✅ Voice configuration system established (50+ XTTS speakers)
- ✅ Multi-TTS engine foundation
- ✅ Model downloading infrastructure with British voice support
- ✅ Basic testing framework
- ✅ Complete XTTS speaker definitions with metadata
- ✅ Wake word detection and continuous listening
- ✅ Microphone permission handling
- ✅ Automated British Piper voice downloading
- 🔄 Web interface integration (wake word UI added)
- 🔄 Real-time voice interaction
- 🔄 Voice cloning implementation

## Key Design Decisions
1. **Local-only processing** - No cloud dependencies
2. **British accent focus** - Vale-like voice preference
3. **Multi-engine approach** - Best of each TTS system
4. **GPU optimization** - Hardware-specific performance tuning
5. **Web-based UI** - Desktop browser interaction model
6. **Comprehensive voice coverage** - 50+ speakers with accent diversity
7. **WebRTC VAD wake word** - Efficient continuous listening without cloud services
8. **Centralized model management** - Single configuration source for all voice models

## Installation & Setup
- `install` script for system dependencies
- `requirements.txt` for Python packages (includes webrtcvad, pyaudio)
- `pyproject.toml` for project configuration
- `python download_models.py` for automated model downloading
- Microphone permissions required for wake word functionality

## Testing & Quality
- `test_basic_tts.py` - Core TTS functionality
- `test.py` - Integration testing
- Audio output validation (`output.wav`)
- Wake word detection testing through web interface
- Model download verification

## Recent Updates
- **2025-09-21**: Completed XTTS_SPEAKERS definition with 50+ speakers
- **2025-09-21**: Implemented wake word detection system
- **2025-09-21**: Enhanced model downloader with centralized configuration
- Added WebRTC VAD-based continuous listening
- Integrated microphone permission handling
- Enhanced web interface with wake word controls
- Added background speech processing with Whisper transcription
- Implemented automated British voice model downloading from centralized config