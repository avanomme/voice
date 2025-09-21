#!/usr/bin/env python3
"""
Simple Model Downloader - Just downloads voice models
Assumes dependencies are already installed
"""

def download_whisper_model():
    """Download Whisper model"""
    print("Downloading Whisper model...")
    try:
        import whisper
        model = whisper.load_model("base")
        print("✅ Whisper model ready")
        return True
    except Exception as e:
        print(f"❌ Whisper failed: {e}")
        return False

def download_coqui_model():
    """Download Coqui XTTS v2 model"""
    print("Downloading Coqui XTTS v2 model (this may take a few minutes)...")
    try:
        from TTS.api import TTS
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cuda")
        
        # Test synthesis
        print("Testing Coqui synthesis...")
        wav = tts.tts("Hello, this is a test.", language="en")
        print("✅ Coqui XTTS v2 ready")
        return True
    except Exception as e:
        print(f"❌ Coqui failed: {e}")
        return False

def download_bark_model():
    """Download Bark models"""
    print("Downloading Bark models (this may take several minutes)...")
    try:
        from bark import preload_models, generate_audio
        preload_models()
        
        # Test synthesis
        print("Testing Bark synthesis...")
        audio = generate_audio("Hello from Bark", history_prompt="v2/en_speaker_2")
        print("✅ Bark models ready")
        return True
    except Exception as e:
        print(f"❌ Bark failed: {e}")
        return False

def main():
    """Download all voice models"""
    print("Voice Model Downloader")
    print("=" * 30)
    
    results = {}
    
    # Download in order
    results['whisper'] = download_whisper_model()
    results['coqui'] = download_coqui_model()
    results['bark'] = download_bark_model()
    
    print("\n" + "=" * 30)
    print("Download Summary:")
    for model, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {model.title()}")
    
    successful = sum(results.values())
    total = len(results)
    
    if successful == total:
        print(f"\n🎉 All {total} models downloaded successfully!")
        print("Ready to run: python web_voice_assistant.py")
    else:
        print(f"\n⚠️ {successful}/{total} models downloaded")
        if successful > 0:
            print("You can still run the voice assistant with available models")

if __name__ == "__main__":
    main()
