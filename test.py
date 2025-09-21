import subprocess
import tempfile
import os
import urllib.request

# Extended list of British female voices, including deeper tones
voices_to_test = [
    # Existing voices you tested
    'en_GB_cori_medium',           # Northern English female
    'en_GB_jenny_dioco_medium',    # Southern English female  
    'en_GB_alba_medium',           # Scottish female
    
    # Additional British voices to download and test
    'en_GB_northern_english_female_medium',  # Northern English female (different speaker)
    'en_GB_southern_english_female_low',     # Southern English female (lower pitch)
    'en_GB_vctk_p225_low',                   # VCTK female (deeper)
    'en_GB_vctk_p231_medium',                # VCTK female (medium depth)
    'en_GB_vctk_p233_low',                   # VCTK female (Scottish, lower)
]

# Voice model URLs for additional downloads
voice_urls = {
    'en_GB_northern_english_female_medium': {
        'model': 'https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/northern_english_female/medium/en_GB-northern_english_female-medium.onnx',
        'config': 'https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/northern_english_female/medium/en_GB-northern_english_female-medium.onnx.json'
    },
    'en_GB_southern_english_female_low': {
        'model': 'https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/southern_english_female/low/en_GB-southern_english_female-low.onnx',
        'config': 'https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/southern_english_female/low/en_GB-southern_english_female-low.onnx.json'
    },
    'en_GB_vctk_p225_low': {
        'model': 'https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/vctk/p225/low/en_GB-vctk-p225-low.onnx',
        'config': 'https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/vctk/p225/low/en_GB-vctk-p225-low.onnx.json'
    }
}

test_texts = [
    'Hello there! I am your voice assistant. How can I help you today?',
    'This is a test of a deeper, more mature British female voice.',
    'I can help you with various tasks and answer your questions.'
]

def download_voice(voice_id):
    """Download voice model if it doesn't exist"""
    voices_dir = '/home/offbyone/.local/share/voice_models/piper'
    model_path = f'{voices_dir}/{voice_id}.onnx'
    config_path = f'{voices_dir}/{voice_id}.onnx.json'
    
    if os.path.exists(model_path):
        return True
        
    if voice_id in voice_urls:
        print(f'Downloading {voice_id}...')
        try:
            os.makedirs(voices_dir, exist_ok=True)
            urllib.request.urlretrieve(voice_urls[voice_id]['model'], model_path)
            urllib.request.urlretrieve(voice_urls[voice_id]['config'], config_path)
            print(f'Downloaded {voice_id}')
            return True
        except Exception as e:
            print(f'Failed to download {voice_id}: {e}')
            return False
    return True

def test_voice(voice_id, text_index=0):
    """Test a specific voice"""
    # Download if needed
    if not download_voice(voice_id):
        return False
        
    print(f'Testing {voice_id}...')
    
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
        temp_file = f.name
    
    try:
        model_path = f'/home/offbyone/.local/share/voice_models/piper/{voice_id}.onnx'
        
        if not os.path.exists(model_path):
            print(f'Model file not found: {model_path}')
            return False
            
        cmd = ['piper', '--model', model_path, '--output_file', temp_file]
        
        result = subprocess.run(cmd, input=test_texts[text_index], text=True, 
                              capture_output=True)
        
        if result.returncode == 0:
            print(f'Generated audio for {voice_id}')
            
            # Play the audio
            play_cmd = ['aplay', temp_file]
            play_result = subprocess.run(play_cmd, capture_output=True)
            
            if play_result.returncode == 0:
                print(f'Played {voice_id} successfully')
                return True
            else:
                print(f'Failed to play {voice_id}: {play_result.stderr.decode()}')
        else:
            print(f'Failed to generate {voice_id}: {result.stderr.decode()}')
            
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)
    
    return False

# Test all voices
print('Testing British female voices with deeper tones...')
print('Looking for Vale-like characteristics: clear, warm, professional, slightly deeper')
print()

successful_voices = []

for i, voice in enumerate(voices_to_test):
    success = test_voice(voice, i % len(test_texts))
    if success:
        successful_voices.append(voice)
    
    print(f'Rate this voice (1-5, 5=most Vale-like): ', end='')
    try:
        rating = input()
        if rating == '5':
            print(f'⭐ {voice} marked as Vale-like!')
    except:
        pass
    
    print('-' * 50)

print(f'\nTesting complete! Successfully tested {len(successful_voices)} voices.')
print('Voices that worked:', successful_voices)
