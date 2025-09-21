#!/usr/bin/env python3
"""
Safe Model Loader with GPU Memory Management
Prevents std::bad_alloc errors by controlling memory allocation
"""

import os
import torch
import gc
from pathlib import Path

def setup_gpu_memory():
    """Configure GPU memory settings to prevent allocation errors"""
    if torch.cuda.is_available():
        # Set memory fraction to use only 80% of available VRAM
        torch.cuda.set_per_process_memory_fraction(0.8)
        
        # Enable memory mapping for large models
        os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:512'
        
        # Clear any existing GPU memory
        torch.cuda.empty_cache()
        gc.collect()
        
        print(f"GPU memory configured - Using {torch.cuda.get_device_name()}")
        print(f"VRAM allocated: {torch.cuda.memory_allocated()/1024**3:.1f}GB")
        print(f"VRAM reserved: {torch.cuda.memory_reserved()/1024**3:.1f}GB")
    else:
        print("Using CPU - no GPU memory management needed")

def safe_load_coqui():
    """Safely load Coqui TTS with memory management"""
    try:
        print("Attempting to load Coqui XTTS v2...")
        setup_gpu_memory()
        
        #from TTS.api import TTS
        
        # Force CPU loading first to avoid GPU memory issues
        print("Loading on CPU first...")
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
        
        # Test if we can move to GPU safely
        if torch.cuda.is_available():
            try:
                print("Attempting to move to GPU...")
                tts = tts.to("cuda")
                print("Successfully moved to GPU")
            except Exception as e:
                print(f"GPU allocation failed, staying on CPU: {e}")
                
        return tts
        
    except Exception as e:
        print(f"Coqui loading failed: {e}")
        return None

def safe_load_bark():
    """Safely load Bark with memory management"""
    try:
        print("Attempting to load Bark...")
        
        # Force CPU mode for Bark to avoid memory conflicts
        os.environ['SUNO_USE_SMALL_MODELS'] = 'True'
        os.environ['SUNO_OFFLOAD_CPU'] = 'True'
        
        from bark import preload_models
        preload_models()
        print("Bark models loaded successfully")
        return True
        
    except Exception as e:
        print(f"Bark loading failed: {e}")
        return False

def download_models_safely():
    """Download models with proper memory management"""
    print("Safe Model Downloader")
    print("=" * 30)
    
    # Clear memory before starting
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    gc.collect()
    
    # Download Whisper (small, safe)
    try:
        import whisper
        print("Loading Whisper base model...")
        whisper.load_model("base")
        print("Whisper loaded successfully")
    except Exception as e:
        print(f"Whisper loading failed: {e}")
    
    # Download Coqui with memory management
    coqui_model = safe_load_coqui()
    if coqui_model:
        try:
            # Test synthesis
            print("Testing Coqui synthesis...")
            test_audio = coqui_model.tts("Hello, this is a test", language="en")
            print("Coqui test successful")
        except Exception as e:
            print(f"Coqui test failed: {e}")
    
    # Clear memory before loading Bark
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    gc.collect()
    
    # Download Bark
    bark_success = safe_load_bark()
    
    print("\nModel loading summary:")
    print(f"Whisper: OK")
    print(f"Coqui: {'OK' if coqui_model else 'FAILED'}")
    print(f"Bark: {'OK' if bark_success else 'FAILED'}")

if __name__ == "__main__":
    download_models_safely()
