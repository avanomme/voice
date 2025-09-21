# Voice Assistant Project - Current Status & Roadmap

## Project Overview
Multi-engine local voice assistant with British/Irish/Australian accents, thinking display, voice cloning, and emotional expressions.

## Hardware Environment
- **CPU**: AMD 7700x
- **RAM**: 92GB
- **GPU**: RTX 5060 Ti (16GB VRAM)
- **OS**: Arch Linux
- **CUDA**: 12.9 (Blackwell support)
- **Python**: 3.11 in UV virtual environment

## ✅ COMPLETED COMPONENTS

### 1. Environment Setup & Dependencies
- UV virtual environment (`voice`) with Python 3.11
- **Working PyTorch configuration**: `torch==2.9.0.dev20250901+cu129`
- **Critical patches applied**:
  - `transformers<4.50` (prevents GenerationMixin issues)
  - `torch.load` patches for Coqui TTS and Bark
- All audio system dependencies installed

### 2. TTS Engine Integration
- **Coqui XTTS v2**: Successfully loaded with 50+ built-in speakers
- **Bark**: Operational with emotional expression support
- **Whisper**: Speech recognition working
- **Piper**: Partial setup (only Alba model downloaded)

### 3. Voice Discovery
- Identified **Vale-like voice**: `en_GB-southern_english_female-low` from Piper
- Tested multiple British accents
- Confirmed preference for deeper British female voice

### 4. Working Components
- Basic web interface operational at `localhost:8765`
- Speech transcription via Whisper
- AI conversation with Ollama (qwen3:latest)
- Thinking/response separation working
- Audio playback functional (with occasional ALSA issues)

## ⚠️ CURRENT ISSUES

### 1. Limited Voice Selection
- **Only 4 voices showing** in web interface
- **Missing Piper models**: Only Alba downloaded, need 6+ British voices
- **XTTS_SPEAKERS undefined error** in voice_models.py
- Voice cloning interface present but untested

### 2. Model Integration Problems
- Coqui voices not loading in web interface
- Bark voices not appearing in dropdown
- Voice model configuration incomplete

## 🎯 IMMEDIATE TODO LIST

### Phase 1: Complete Voice Model Downloads
```bash
# Download missing Piper voices
mkdir -p ~/.local/share/voice_models/piper

# Vale-like voice (HIGH PRIORITY)
wget -O ~/.local/share/voice_models/piper/en_GB-southern_english_female-low.onnx \
  "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/southern_english_female/low/en_GB-southern_english_female-low.onnx"

wget -O ~/.local/share/voice_models/piper/en_GB-southern_english_female-low.onnx.json \
  "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/southern_english_female/low/en_GB-southern_english_female-low.onnx.json"

# Additional British voices
wget -O ~/.local/share/voice_models/piper/en_GB-cori-medium.onnx \
  "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/cori/medium/en_GB-cori-medium.onnx"

# [Continue for all British voices...]
```
1. Ensure all Piper British Voices are Functional
2. 

### Phase 2: Fix Voice Configuration
1. **Complete XTTS_SPEAKERS definition** in voice_models.py
2. **Add all 50+ Coqui speakers** from CLI output
3. **Include Bark emotional voices**
4. **Set Vale voice as default**

### Phase 3: Web Interface Updates
1. **Fix voice dropdown** to show all engines
2. **Test voice cloning** upload functionality  
3. **Verify thinking display** formatting
4. **Add engine selection** (Piper for speed, Coqui for quality)

## 📁 FILE STRUCTURE STATUS

### ✅ Working Files
- `voice_models.py` - Partial configuration (needs XTTS_SPEAKERS)
- `tts_engines.py` - Multi-engine support implemented
- `assistant_logic.py` - Conversation processing complete
- `web_voice_assistant.py` - Basic interface working
- `requirements.txt` - Blackwell-compatible dependencies
- `simple_model_downloader.py` - Model testing script

### ⚠️ Files Needing Updates
- `voice_models.py` - Add complete XTTS_SPEAKERS dictionary
- `web_voice_assistant.py` - Fix voice loading logic
- `tts_engines.py` - Update Piper model paths

## 🎭 VOICE INVENTORY TARGET

### Piper Voices (Fast, Real-time)
- `en_GB-southern_english_female-low` ⭐ (Vale-like)
- `en_GB-cori-medium` (Northern English female)
- `en_GB-jenny_dioco-medium` (Southern English female)
- `en_GB-alba-medium` ✅ (Scottish female - already have)
- `en_GB-northern_english_male-medium` (Male voice)

### Coqui XTTS v2 (High Quality + Voice Cloning)
- 50+ built-in speakers available via CLI
- Voice cloning from 6-second samples
- Multilingual support (17 languages)

### Bark (Emotional Expressions)
- `v2/en_speaker_0` (British Male 1)
- `v2/en_speaker_2` (British Female 1) 
- `v2/en_speaker_4` (British Male 2)
- `v2/en_speaker_6` (British Female 2)
- Support for [laughs], [sighs], [music] tags

## 🔧 TECHNICAL DEBT

### Memory Management
- Implement lazy loading for large models
- Add GPU memory monitoring
- Optimize model switching

### Audio System
- Resolve occasional ALSA connection issues
- Add fallback audio drivers
- Implement audio device selection

### Error Handling
- Add comprehensive TTS engine fallbacks
- Improve voice model validation
- Better error messages in web interface

## 🚀 FUTURE ENHANCEMENTS

### Self-Upgrading Capabilities
- Model performance monitoring
- Automatic voice adaptation based on usage
- Learning from user preferences

### Advanced Features
- Real-time voice conversion
- Multi-speaker conversations
- Custom wake word training
- Home automation integration

## 📋 CLAUDE CODE TASKS

### Immediate (High Priority)
1. **Fix voice_models.py XTTS_SPEAKERS definition**
2. **Download all British Piper voices** 
3. **Update web interface voice loading**
4. **Test complete voice selection dropdown**

### Secondary
1. **Implement voice cloning testing**
2. **Add Bark emotional expression examples**
3. **Create voice comparison tool**
4. **Optimize model loading performance**

### Testing Checklist
- [ ] Vale voice (`en_GB-southern_english_female-low`) working
- [ ] All 50+ Coqui speakers accessible  
- [ ] Bark emotional expressions functional
- [ ] Voice cloning with uploaded samples
- [ ] Thinking display properly formatted
- [ ] Audio playback consistent across voices
- [ ] Web interface responsive and stable

## 💾 BACKUP WORKING CONFIGURATION

### Dependencies That Work
```bash
torch==2.9.0.dev20250901+cu129
transformers<4.50
numpy>=1.26
pandas>=2.2
git+https://github.com/coqui-ai/TTS.git
bark
soundfile
```

### Critical Patches Applied
```bash
# Coqui TTS torch.load patch
sed -i 's/torch\.load(f, map_location=map_location, \*\*kwargs)/torch.load(f, map_location=map_location, weights_only=False, **kwargs)/g' /home/offbyone/uv-envs/voice/lib/python3.11/site-packages/TTS/utils/io.py

# Bark torch.load patch  
sed -i 's/torch\.load(ckpt_path, map_location=device)/torch.load(ckpt_path, map_location=device, weights_only=False)/g' /home/offbyone/uv-envs/voice/lib/python3.11/site-packages/bark/generation.py
```

---

**Current Status**: ~80% complete. Core functionality working, needs voice model integration completion.
**Next Session Priority**: Complete Piper voice downloads and fix web interface voice selection.
**Estimated Time to Full Completion**: 2-3 hours focused work.