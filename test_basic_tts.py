import whisper
import subprocess
import tempfile

# Test Whisper (working)
print("Testing Whisper...")
model = whisper.load_model("base")
print("Whisper OK")

# Test Piper (should work)
print("Testing Piper...")
try:
    result = subprocess.run(['piper', '--help'], capture_output=True)
    print("Piper OK" if result.returncode == 0 else "Piper failed")
except:
    print("Piper not found")

# Test basic TTS
print("Testing system TTS...")
try:
    import pyttsx3
    engine = pyttsx3.init()
    print("System TTS OK")
except:
    print("System TTS failed")

print("Basic components ready - skipping Coqui for now")
