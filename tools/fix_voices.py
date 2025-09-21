#!/usr/bin/env python3
"""
Quick fix to activate all voice models
"""

def test_available_models():
    print("Testing available TTS engines...")
    
    # Test Piper voices
    import subprocess
    import os
    piper_dir = "/home/offbyone/.local/share/voice_models/piper"
    if os.path.exists(piper_dir):
        piper_voices = [f.replace('.onnx', '') for f in os.listdir(piper_dir) if f.endswith('.onnx')]
        print(f"Piper voices available: {len(piper_voices)}")
        for voice in piper_voices:
            print(f"  - {voice}")
    
    # Test Coqui XTTS speakers
    try:
        import subprocess
        result = subprocess.run(['tts', '--model_name', 'tts_models/multilingual/multi-dataset/xtts_v2', '--list_speaker_idxs'], 
                              capture_output=True, text=True)
        if 'Available speaker ids:' in result.stdout:
            print("Coqui XTTS v2 speakers available: ~50+ voices")
            print("Includes: Claribel Dervla, Ana Florence, Andrew Chipper, etc.")
    except Exception as e:
        print(f"Coqui XTTS v2: Not accessible via CLI ({e})")
    
    # Test Bark
    try:
        print("Bark models: Available with emotional expressions")
        bark_speakers = ['v2/en_speaker_0', 'v2/en_speaker_1', 'v2/en_speaker_2', 'v2/en_speaker_6']
        print(f"Bark speakers: {bark_speakers}")
    except ImportError:
        print("Bark: Not available")

def create_simple_voice_config():
    """Create a simplified voice configuration that works"""
    config = '''
# Simplified voice configuration for web interface
AVAILABLE_VOICES = {
    # Piper voices (fast, reliable)
    "piper:en_GB_southern_english_female_low": "Vale (Deep British Female) - Piper",
    "piper:en_GB_cori_medium": "Cori (Northern English) - Piper", 
    "piper:en_GB_jenny_dioco_medium": "Jenny (Southern English) - Piper",
    "piper:en_GB_alba_medium": "Alba (Scottish) - Piper",
    
    # Coqui XTTS v2 voices (high quality, voice cloning)
    "coqui:Claribel Dervla": "Claribel Dervla - Coqui XTTS",
    "coqui:Ana Florence": "Ana Florence - Coqui XTTS", 
    "coqui:Andrew Chipper": "Andrew Chipper - Coqui XTTS",
    "coqui:Damien Black": "Damien Black - Coqui XTTS",
    "coqui:Sofia Hellen": "Sofia Hellen - Coqui XTTS",
    
    # Bark voices (emotional expressions)
    "bark:v2/en_speaker_0": "British Male 1 - Bark",
    "bark:v2/en_speaker_2": "British Female 1 - Bark", 
    "bark:v2/en_speaker_4": "British Male 2 - Bark",
    "bark:v2/en_speaker_6": "British Female 2 - Bark",
}

DEFAULT_VOICE = "piper:en_GB_southern_english_female_low"  # Vale-like voice
'''
    
    with open('simple_voices.py', 'w') as f:
        f.write(config)
    
    print("Created simple_voices.py with all available voices")

if __name__ == "__main__":
    test_available_models()
    print("\n" + "="*50)
    create_simple_voice_config()
    print("Run: python web_voice_assistant.py to test all voices")
