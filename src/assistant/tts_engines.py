# tts_engines.py
"""
Multi-Engine TTS Implementation
Supports Coqui XTTS v2, Bark, and Piper
"""

import os
import tempfile
import subprocess
import base64
import torch
from typing import Optional
import urllib.request

from voice_models import (
    XTTS_SPEAKERS, MODELS_DIR, COQUI_DIR, BARK_DIR, PIPER_DIR,
    BARK_SPEAKERS, PIPER_MODELS
)

class TTSEngineManager:
    def __init__(self):
        self.engines = {}
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.setup_directories()
        print(f"TTS Manager initialized - Device: {self.device}")
        
    def setup_directories(self):
        """Create necessary directories"""
        for directory in [MODELS_DIR, COQUI_DIR, BARK_DIR, PIPER_DIR]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def get_engine(self, engine_name: str):
        """Get or initialize TTS engine"""
        if engine_name not in self.engines:
            if engine_name == "coqui":
                self.engines[engine_name] = CoquiEngine(self.device)
            elif engine_name == "bark":
                self.engines[engine_name] = BarkEngine(self.device)
            elif engine_name == "piper":
                self.engines[engine_name] = PiperEngine()
            else:
                raise ValueError(f"Unknown engine: {engine_name}")
        
        return self.engines[engine_name]
    
    def speak(self, text: str, engine: str = "coqui", voice_id: str = None, 
              clone_voice_path: str = None, **kwargs) -> Optional[str]:
        """
        Generate speech using specified engine
        Returns base64 encoded audio data
        """
        try:
            tts_engine = self.get_engine(engine)
            return tts_engine.synthesize(text, voice_id, clone_voice_path, **kwargs)
        except Exception as e:
            print(f"TTS Error ({engine}): {e}")
            return None

class CoquiEngine:
    def __init__(self, device: str):
        self.device = device
        self.model = None
        self.model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
        os.environ["COQUI_TOS_AGREED"] = "1"
        
    def _load_model(self):
        """Lazy load the Coqui model"""
        if self.model is None:
            try:
                from TTS.api import TTS
                print("Loading Coqui XTTS v2 model...")
                self.model = TTS(self.model_name).to(self.device)
                print("Coqui model loaded successfully")
            except ImportError:
                raise ImportError("Coqui TTS not installed. Run: pip install coqui-tts")
            except Exception as e:
                raise Exception(f"Failed to load Coqui model: {e}")
    
    def synthesize(self, text: str, voice_id: str = None, clone_voice_path: str = None, 
                   language: str = "en", **kwargs) -> str:
        """Generate speech with Coqui XTTS v2"""
        self._load_model()
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            output_path = f.name
        
        try:
            if clone_voice_path and os.path.exists(clone_voice_path):
                # Voice cloning mode
                self.model.tts_to_file(
                    text=text,
                    file_path=output_path,
                    speaker_wav=clone_voice_path,
                    language=language,
                    split_sentences=True
                )
            elif voice_id and voice_id in XTTS_SPEAKERS:
                # Use XTTS built-in speaker
                self.model.tts_to_file(
                    text=text,
                    file_path=output_path,
                    speaker=voice_id,
                    language=language
                )
            else:
                # Default synthesis if no valid voice_id or clone_voice_path is provided
                self.model.tts_to_file(
                    text=text,
                    file_path=output_path,
                    language=language
                )
            
            # Read and encode audio
            with open(output_path, 'rb') as audio_file:
                audio_data = audio_file.read()
            
            return base64.b64encode(audio_data).decode()
            
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)

class BarkEngine:
    def __init__(self, device: str):
        self.device = device
        self.model = None
        
    def _load_model(self):
        """Lazy load the Bark model"""
        if self.model is None:
            try:
                from bark import SAMPLE_RATE, generate_audio, preload_models
                print("Loading Bark model...")
                preload_models()
                self.generate_audio = generate_audio
                self.sample_rate = SAMPLE_RATE
                print("Bark model loaded successfully")
                self.model = True  # Flag that model is loaded
            except ImportError:
                raise ImportError("Bark not installed. Run: pip install git+https://github.com/suno-ai/bark.git")
    
    def synthesize(self, text: str, voice_id: str = None, clone_voice_path: str = None, **kwargs) -> str:
        """Generate speech with Bark"""
        self._load_model()
        
        # Use voice preset if specified
        if voice_id and voice_id in BARK_SPEAKERS:
            history_prompt = voice_id
        else:
            history_prompt = "v2/en_speaker_2"  # Default British female
        
        # Generate audio
        audio_array = self.generate_audio(text, history_prompt=history_prompt)
        
        # Convert to WAV and encode
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            output_path = f.name
        
        try:
            import scipy.io.wavfile as wavfile
            wavfile.write(output_path, self.sample_rate, audio_array)
            
            with open(output_path, 'rb') as audio_file:
                audio_data = audio_file.read()
            
            return base64.b64encode(audio_data).decode()
            
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)

class PiperEngine:
    def __init__(self):
        self.models_downloaded = set()
        
    def _download_model(self, voice_id: str):
        """Download Piper model if not exists"""
        if voice_id not in PIPER_MODELS:
            raise ValueError(f"Unknown Piper voice: {voice_id}")
        
        if voice_id in self.models_downloaded:
            return
            
        voice_info = PIPER_MODELS[voice_id]
        model_path = PIPER_DIR / f"{voice_id}.onnx"
        config_path = PIPER_DIR / f"{voice_id}.onnx.json"
        
        if not model_path.exists():
            print(f"Downloading Piper voice: {voice_info['name']}")
            urllib.request.urlretrieve(voice_info["url"], model_path)
            urllib.request.urlretrieve(voice_info["config_url"], config_path)
            print(f"Downloaded {voice_info['name']}")
        
        self.models_downloaded.add(voice_id)
    
    def synthesize(self, text: str, voice_id: str = None, clone_voice_path: str = None, **kwargs) -> str:
        """Generate speech with Piper"""
        if not voice_id:
            voice_id = "en_GB_cori_medium"  # Default British voice
        
        self._download_model(voice_id)
        
        model_path = PIPER_DIR / f"{voice_id}.onnx"
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            output_path = f.name
        
        try:
            # Use piper command line
            cmd = ["piper", "--model", str(model_path), "--output_file", output_path]
            process = subprocess.Popen(
                cmd, 
                stdin=subprocess.PIPE, 
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate(input=text)
            
            if process.returncode != 0:
                raise Exception(f"Piper failed: {stderr}")
            
            with open(output_path, 'rb') as audio_file:
                audio_data = audio_file.read()
            
            return base64.b64encode(audio_data).decode()
            
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)

# Installation helpers
def install_dependencies():
    """Install required TTS libraries"""
    import subprocess
    import sys
    
    print("Installing TTS dependencies...")
    
    # Coqui TTS
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "coqui-tts", "torch", "torchaudio"
        ])
        print("✓ Coqui TTS installed")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install Coqui TTS: {e}")
    
    # Bark
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "git+https://github.com/suno-ai/bark.git",
            "scipy"
        ])
        print("✓ Bark installed")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install Bark: {e}")
    
    # Piper (already installed via pacman)
    print("✓ Piper should be installed via system package manager")
    
    print("Dependencies installation complete!")

def test_engines():
    """Test all TTS engines"""
    manager = TTSEngineManager()
    test_text = "Hello, this is a test of the text to speech system with a British accent."
    
    print("Testing TTS engines...")
    
    # Test Coqui
    try:
        print("Testing Coqui XTTS v2...")
        audio = manager.speak(test_text, engine="coqui", voice_id="vctk_p243")
        if audio:
            print("✓ Coqui working")
        else:
            print("✗ Coqui failed")
    except Exception as e:
        print(f"✗ Coqui error: {e}")
    
    # Test Bark
    try:
        print("Testing Bark...")
        audio = manager.speak(test_text, engine="bark", voice_id="v2/en_speaker_2")
        if audio:
            print("✓ Bark working")
        else:
            print("✗ Bark failed")
    except Exception as e:
        print(f"✗ Bark error: {e}")
    
    # Test Piper
    try:
        print("Testing Piper...")
        audio = manager.speak(test_text, engine="piper", voice_id="en_GB_cori_medium")
        if audio:
            print("✓ Piper working")
        else:
            print("✗ Piper failed")
    except Exception as e:
        print(f"✗ Piper error: {e}")
    
    print("Engine testing complete")
