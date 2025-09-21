# Project Scope

## Goals

### Primary Objectives
- **Multi-engine local voice assistant** with comprehensive TTS support
- **British/Irish/Australian accent focus** with preference for deeper British female voices
- **Real-time voice interaction** with thinking display and response separation
- **Voice cloning capabilities** from 6-second audio samples
- **Emotional expression support** through Bark TTS engine
- **High-performance local deployment** leveraging AMD 7700x + RTX 5060 Ti hardware

### Technical Goals
- **Multi-TTS engine integration**: Coqui XTTS v2, Bark, Piper, Whisper
- **GPU-optimized processing** with CUDA 12.9 Blackwell support
- **Web-based interface** for easy interaction and configuration
- **Voice model management** with lazy loading and memory optimization
- **Audio system reliability** with fallback mechanisms
- **Self-upgrading capabilities** with performance monitoring

### Voice Quality Targets
- **50+ Coqui XTTS speakers** with voice cloning
- **6+ British Piper voices** for real-time response
- **Bark emotional expressions** with [laughs], [sighs], [music] support
- **Vale-like voice preference** (`en_GB-southern_english_female-low`)

## Non-Goals

### Out of Scope
- **Cloud-based processing** - strictly local deployment
- **Mobile/embedded platforms** - desktop-focused implementation
- **Real-time wake word detection** - manual activation preferred
- **Home automation integration** - voice assistant core functionality only
- **Multi-user voice profiles** - single-user optimization
- **Voice activity detection** - push-to-talk interaction model

### Technical Limitations
- **Non-British accent support** - limited to British/Irish/Australian
- **Streaming TTS** - batch processing acceptable for quality
- **Real-time voice conversion** - post-processing approach
- **Custom model training** - use pre-trained models only
- **Cross-platform compatibility** - Arch Linux specific optimization

### Interface Constraints
- **Mobile UI** - desktop web interface only
- **Voice command parsing** - text-based conversation flow
- **Multi-language support** - English language focus
- **Accessibility features** - standard web interface sufficient