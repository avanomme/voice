# xtts_say.py
import sys
from torch.serialization import add_safe_globals
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import XttsAudioConfig
from TTS.api import TTS

# Allowlist the classes used inside the checkpoint
add_safe_globals([XttsConfig, XttsAudioConfig])

# Create the TTS model on GPU
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
tts.to("cuda")  # explicitly move to GPU

# Get text from command-line arguments
text = " ".join(sys.argv[1:]) or "Hi from XTTS v2 on CUDA 12.9!"
tts.tts_to_file(text=text, file_path="output.wav")

print("✅ Done. Saved to output.wav")
