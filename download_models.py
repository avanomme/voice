#!/usr/bin/env python3
"""
Model Pre-downloader for Voice Assistant
Downloads all TTS models before running the web interface
"""

import os
import sys
import urllib.request
from pathlib import Path
import subprocess

def print_status(message, color="\033[92m"):
    """Print colored status message"""
    print(f"{color}[INFO]\033[0m {message}")

def print_error(message):
    """Print error message"""
    print(f"\033[91m[ERROR]\033[0m {message}")

def download_piper_models():
    """Download Piper voice models"""
    print_status("Downloading Piper voice models...")
    
    piper_dir = Path.home() / ".local" / "share" / "voice_models" / "piper"
    piper_dir.mkdir(parents=True, exist_ok=True)
    
    piper_models = {
        "en_GB_alba_medium": {
            "url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/alba/medium/en_GB-alba-medium.onnx",
            "config_url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/alba/medium/en_GB-alba-medium.onnx.json",
        },
        "en_GB_cori_medium": {
            "url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/cori/medium/en_GB-cori-medium.onnx",
            "config_url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/cori/medium/en_GB-cori-medium.onnx.json",
        },
        "en_GB_jenny_dioco_medium": {
            "url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/jenny_dioco/medium/en_GB-jenny_dioco-medium.onnx",
            "config_url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/jenny_dioco/medium/en_GB-jenny_dioco-medium.onnx.json",
        }
    }
    
    for model_id, model_info in piper_models.items():
        model_path = piper_dir / f"{model_id}.onnx"
        config_path = piper_dir / f"{model_id}.onnx.json"
        
        if not model_path.exists():
            print_status(f"Downloading {model_id}...")
            try:
                urllib.request.urlretrieve(model_info["url"], model_path)
                urllib.request.urlretrieve(model_info["config_url"], config_path)
                print_status(f"Downloaded {model_id}")
            except Exception as e:
                print_error(f"Failed to download {model_id}: {e}")
        else:
            print_status(f"{model_id} already exists")

def download_coqui_models():
    """Pre-download Coqui models"""
    print_status("Pre-downloading Coqui XTTS v2 model...")
    
    try:
        # Import TTS and trigger model download
        #from TTS.api import TTS
        
        print_status("Loading XTTS v2 (this will download ~1GB on first run)...")
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=True)
        print_status("Coqui XTTS v2 model ready")
        
        # Test a quick synthesis to ensure it works
        print_status("Testing Coqui model...")
        test_wav = tts.tts("Hello, this is a test", language="en")
        print_status("Coqui model test successful")
        
    except ImportError:
        print_error("Coqui TTS not installed. Run: uv pip install coqui-tts")
    except Exception as e:
        print_error(f"Failed to download Coqui model: {e}")

def download_bark_models():
    """Pre-download Bark models"""
    print_status("Pre-downloading Bark models...")
    
    try:
        from bark import preload_models
        print_status("Loading Bark models (this may take several minutes on first run)...")
        preload_models()
        print_status("Bark models ready")
        
    except ImportError:
        print_error("Bark not installed. Run: uv pip install git+https://github.com/suno-ai/bark.git")
    except Exception as e:
        print_error(f"Failed to download Bark models: {e}")

def download_whisper_models():
    """Pre-download Whisper models"""
    print_status("Pre-downloading Whisper models...")
    
    try:
        import whisper
        print_status("Loading Whisper base model...")
        model = whisper.load_model("base", download_root=Path.home() / ".cache" / "whisper")
        print_status("Whisper model ready")
        
    except ImportError:
        print_error("Whisper not installed. Run: uv pip install openai-whisper")
    except Exception as e:
        print_error(f"Failed to download Whisper model: {e}")

def check_system_requirements():
    """Check system requirements and available memory"""
    print_status("Checking system requirements...")
    
    try:
        import psutil
        
        # Check available RAM
        memory = psutil.virtual_memory()
        available_gb = memory.available / (1024**3)
        
        print_status(f"Available RAM: {available_gb:.1f} GB")
        
        if available_gb < 4:
            print_error("Warning: Less than 4GB RAM available. TTS models may fail to load.")
            return False
        
        # Check GPU
        try:
            import torch
            if torch.cuda.is_available():
                gpu_name = torch.cuda.get_device_name()
                vram = torch.cuda.get_device_properties(0).total_memory / (1024**3)
                print_status(f"GPU detected: {gpu_name} ({vram:.1f}GB VRAM)")
            else:
                print_status("No GPU detected - using CPU (slower but functional)")
        except ImportError:
            print_status("PyTorch not installed yet")
        
        return True
        
    except ImportError:
        print_status("psutil not available - skipping memory check")
        return True

def main():
    """Main model download process"""
    print_status("Voice Assistant Model Downloader")
    print_status("=" * 50)
    
    # Check system requirements first
    if not check_system_requirements():
        print_error("System requirements not met. Consider closing other applications.")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Create model directories
    models_base = Path.home() / ".local" / "share" / "voice_models"
    for subdir in ["coqui", "bark", "piper"]:
        (models_base / subdir).mkdir(parents=True, exist_ok=True)
    
    # Download models in order of importance
    download_whisper_models()  # Fastest, always needed
    download_piper_models()    # Fast, British voices
    
    # Ask before downloading large models
    print_status("\nReady to download large TTS models (may take 10+ minutes)")
    print_status("Coqui XTTS v2: ~1GB, Bark: ~2GB")
    
    response = input("Download large models now? (Y/n): ")
    if response.lower() != 'n':
        download_coqui_models()
        download_bark_models()
    else:
        print_status("Skipping large models - they will download when first used")
    
    print_status("Model download process complete!")
    print_status("You can now run: python web_voice_assistant.py")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_error("\nDownload interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)
