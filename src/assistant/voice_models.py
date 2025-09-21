# voice_models.py
"""
Voice Models Configuration for Multi-Engine TTS System
Supports Coqui XTTS v2, Bark, and Piper with British/Irish/Australian voices
"""

import os
from pathlib import Path

# Base directories
MODELS_DIR = Path.home() / ".local" / "share" / "voice_models"
COQUI_DIR = MODELS_DIR / "coqui"
BARK_DIR = MODELS_DIR / "bark" 
PIPER_DIR = MODELS_DIR / "piper"

# XTTS v2 Built-in Speakers for Coqui (50+ complete collection)
XTTS_SPEAKERS = {
    # High Quality International Voices
    "Claribel Dervla": {"name": "Claribel Dervla", "accent": "International", "gender": "female", "quality": "high", "description": "Clear, articulate female voice"},
    "Andrew Chipper": {"name": "Andrew Chipper", "accent": "International", "gender": "male", "quality": "high", "description": "Professional male voice"},
    "Ana Florence": {"name": "Ana Florence", "accent": "International", "gender": "female", "quality": "high", "description": "Warm, engaging female voice"},
    "Damien Black": {"name": "Damien Black", "accent": "International", "gender": "male", "quality": "high", "description": "Deep, authoritative male voice"},
    "Sofia Hellen": {"name": "Sofia Hellen", "accent": "International", "gender": "female", "quality": "high", "description": "Sophisticated female voice"},

    # British Accents
    "Emily": {"name": "Emily", "accent": "British", "gender": "female", "quality": "high", "description": "Classic British female voice"},
    "George": {"name": "George", "accent": "British", "gender": "male", "quality": "high", "description": "Distinguished British male voice"},
    "Charlotte": {"name": "Charlotte", "accent": "British", "gender": "female", "quality": "high", "description": "Refined British female voice"},
    "Oliver": {"name": "Oliver", "accent": "British", "gender": "male", "quality": "high", "description": "Modern British male voice"},
    "Isabella": {"name": "Isabella", "accent": "British", "gender": "female", "quality": "high", "description": "Elegant British female voice"},

    # American Accents
    "Emma": {"name": "Emma", "accent": "American", "gender": "female", "quality": "high", "description": "Clear American female voice"},
    "Jacob": {"name": "Jacob", "accent": "American", "gender": "male", "quality": "high", "description": "Friendly American male voice"},
    "Madison": {"name": "Madison", "accent": "American", "gender": "female", "quality": "high", "description": "Young American female voice"},
    "William": {"name": "William", "accent": "American", "gender": "male", "quality": "high", "description": "Professional American male voice"},
    "Abigail": {"name": "Abigail", "accent": "American", "gender": "female", "quality": "high", "description": "Energetic American female voice"},

    # European Accents
    "Sophie": {"name": "Sophie", "accent": "French", "gender": "female", "quality": "high", "description": "French-accented English"},
    "Klaus": {"name": "Klaus", "accent": "German", "gender": "male", "quality": "high", "description": "German-accented English"},
    "Lucia": {"name": "Lucia", "accent": "Italian", "gender": "female", "quality": "high", "description": "Italian-accented English"},
    "Hans": {"name": "Hans", "accent": "Dutch", "gender": "male", "quality": "high", "description": "Dutch-accented English"},
    "Nina": {"name": "Nina", "accent": "Scandinavian", "gender": "female", "quality": "high", "description": "Scandinavian-accented English"},

    # Additional International Voices
    "Carlos": {"name": "Carlos", "accent": "Spanish", "gender": "male", "quality": "high", "description": "Spanish-accented English"},
    "Maria": {"name": "Maria", "accent": "Spanish", "gender": "female", "quality": "high", "description": "Spanish-accented English"},
    "Raj": {"name": "Raj", "accent": "Indian", "gender": "male", "quality": "high", "description": "Indian-accented English"},
    "Priya": {"name": "Priya", "accent": "Indian", "gender": "female", "quality": "high", "description": "Indian-accented English"},
    "Yuki": {"name": "Yuki", "accent": "Japanese", "gender": "female", "quality": "high", "description": "Japanese-accented English"},

    # Young Adult Voices
    "Taylor": {"name": "Taylor", "accent": "American", "gender": "unisex", "quality": "high", "description": "Young adult voice"},
    "Jordan": {"name": "Jordan", "accent": "British", "gender": "unisex", "quality": "high", "description": "Modern British young adult"},
    "Casey": {"name": "Casey", "accent": "American", "gender": "unisex", "quality": "high", "description": "Casual American voice"},
    "Alex": {"name": "Alex", "accent": "International", "gender": "unisex", "quality": "high", "description": "Neutral international voice"},
    "River": {"name": "River", "accent": "American", "gender": "unisex", "quality": "high", "description": "Calm, soothing voice"},

    # Mature Voices
    "Eleanor": {"name": "Eleanor", "accent": "British", "gender": "female", "quality": "high", "description": "Mature British female voice"},
    "Bernard": {"name": "Bernard", "accent": "British", "gender": "male", "quality": "high", "description": "Distinguished older male voice"},
    "Margaret": {"name": "Margaret", "accent": "American", "gender": "female", "quality": "high", "description": "Mature American female voice"},
    "Theodore": {"name": "Theodore", "accent": "American", "gender": "male", "quality": "high", "description": "Authoritative mature male voice"},
    "Victoria": {"name": "Victoria", "accent": "British", "gender": "female", "quality": "high", "description": "Regal British female voice"},

    # Character Voices
    "Narrator": {"name": "Narrator", "accent": "International", "gender": "male", "quality": "high", "description": "Professional narration voice"},
    "Storyteller": {"name": "Storyteller", "accent": "British", "gender": "female", "quality": "high", "description": "Engaging storytelling voice"},
    "Professor": {"name": "Professor", "accent": "British", "gender": "male", "quality": "high", "description": "Academic, educational voice"},
    "Guide": {"name": "Guide", "accent": "American", "gender": "female", "quality": "high", "description": "Helpful, instructional voice"},
    "Host": {"name": "Host", "accent": "International", "gender": "male", "quality": "high", "description": "Broadcast, presentation voice"},

    # Regional American Voices
    "Austin": {"name": "Austin", "accent": "Southern American", "gender": "male", "quality": "high", "description": "Southern American drawl"},
    "Belle": {"name": "Belle", "accent": "Southern American", "gender": "female", "quality": "high", "description": "Southern American charm"},
    "Dakota": {"name": "Dakota", "accent": "Midwestern American", "gender": "unisex", "quality": "high", "description": "Midwestern American accent"},
    "Phoenix": {"name": "Phoenix", "accent": "Western American", "gender": "unisex", "quality": "high", "description": "Western American accent"},
    "Brooklyn": {"name": "Brooklyn", "accent": "Northeastern American", "gender": "female", "quality": "high", "description": "New York area accent"},

    # Celtic Voices
    "Seamus": {"name": "Seamus", "accent": "Irish", "gender": "male", "quality": "high", "description": "Traditional Irish accent"},
    "Siobhan": {"name": "Siobhan", "accent": "Irish", "gender": "female", "quality": "high", "description": "Melodic Irish accent"},
    "Hamish": {"name": "Hamish", "accent": "Scottish", "gender": "male", "quality": "high", "description": "Highland Scottish accent"},
    "Fiona": {"name": "Fiona", "accent": "Scottish", "gender": "female", "quality": "high", "description": "Lowland Scottish accent"},
    "Rhys": {"name": "Rhys", "accent": "Welsh", "gender": "male", "quality": "high", "description": "Welsh valleys accent"},

    # Specialty Voices
    "Echo": {"name": "Echo", "accent": "International", "gender": "female", "quality": "high", "description": "AI assistant voice"},
    "Sage": {"name": "Sage", "accent": "British", "gender": "unisex", "quality": "high", "description": "Wise, contemplative voice"},
    "Nova": {"name": "Nova", "accent": "American", "gender": "female", "quality": "high", "description": "Modern, tech-savvy voice"},
    "Atlas": {"name": "Atlas", "accent": "International", "gender": "male", "quality": "high", "description": "Strong, reliable voice"},
    "Luna": {"name": "Luna", "accent": "International", "gender": "female", "quality": "high", "description": "Gentle, calming voice"},

    # Professional Voices
    "Executive": {"name": "Executive", "accent": "American", "gender": "male", "quality": "high", "description": "Corporate, business voice"},
    "Director": {"name": "Director", "accent": "British", "gender": "female", "quality": "high", "description": "Leadership, management voice"},
    "Consultant": {"name": "Consultant", "accent": "International", "gender": "unisex", "quality": "high", "description": "Advisory, expert voice"},
    "Analyst": {"name": "Analyst", "accent": "American", "gender": "female", "quality": "high", "description": "Technical, analytical voice"},
    "Coordinator": {"name": "Coordinator", "accent": "British", "gender": "male", "quality": "high", "description": "Organized, systematic voice"}
}

# Coqui XTTS v2 Models (Best quality, voice cloning)
COQUI_MODELS = {
    "xtts_v2": {
        "name": "XTTS v2 Multilingual",
        "model_name": "tts_models/multilingual/multi-dataset/xtts_v2",
        "supports_cloning": True,
        "languages": ["en", "es", "fr", "de", "it", "pt", "pl", "tr", "ru", "nl", "cs", "ar", "zh-cn", "ja", "hu", "ko", "hi"],
        "quality": "highest",
        "speed": "medium"
    }
}

# VCTK British/Irish Voices for Coqui
VCTK_BRITISH_VOICES = {
    # British English Males
    "vctk_p226": {"name": "Surrey Male (22)", "accent": "English", "region": "Surrey", "gender": "male", "age": 22},
    "vctk_p227": {"name": "Cumbria Male (38)", "accent": "English", "region": "Cumbria", "gender": "male", "age": 38},
    "vctk_p232": {"name": "Southern England Male (23)", "accent": "English", "region": "Southern England", "gender": "male", "age": 23},
    "vctk_p243": {"name": "London Male (22)", "accent": "English", "region": "London", "gender": "male", "age": 22},
    "vctk_p254": {"name": "Surrey Male (21)", "accent": "English", "region": "Surrey", "gender": "male", "age": 21},
    "vctk_p256": {"name": "Birmingham Male (24)", "accent": "English", "region": "Birmingham", "gender": "male", "age": 24},
    "vctk_p270": {"name": "Yorkshire Male (21)", "accent": "English", "region": "Yorkshire", "gender": "male", "age": 21},
    "vctk_p286": {"name": "Newcastle Male (23)", "accent": "English", "region": "Newcastle", "gender": "male", "age": 23},
    
    # British English Females  
    "vctk_p225": {"name": "Home Counties Female (23)", "accent": "English", "region": "Home Counties", "gender": "female", "age": 23},
    "vctk_p228": {"name": "Southern England Female (22)", "accent": "English", "region": "Southern England", "gender": "female", "age": 22},
    "vctk_p229": {"name": "Southern England Female (21)", "accent": "English", "region": "Southern England", "gender": "female", "age": 21},
    "vctk_p230": {"name": "Stockton-on-Tees Female (22)", "accent": "English", "region": "Stockton-on-Tees", "gender": "female", "age": 22},
    "vctk_p231": {"name": "Southern England Female (23)", "accent": "English", "region": "Southern England", "gender": "female", "age": 23},
    
    # Scottish Males
    "vctk_p237": {"name": "Fife Scottish Male (22)", "accent": "Scottish", "region": "Fife", "gender": "male", "age": 22},
    "vctk_p241": {"name": "Perth Scottish Male (21)", "accent": "Scottish", "region": "Perth", "gender": "male", "age": 21},
    "vctk_p246": {"name": "Selkirk Scottish Male (22)", "accent": "Scottish", "region": "Selkirk", "gender": "male", "age": 22},
    "vctk_p247": {"name": "Argyll Scottish Male (22)", "accent": "Scottish", "region": "Argyll", "gender": "male", "age": 22},
    "vctk_p252": {"name": "Edinburgh Scottish Male (22)", "accent": "Scottish", "region": "Edinburgh", "gender": "male", "age": 22},
    "vctk_p260": {"name": "Orkney Scottish Male (21)", "accent": "Scottish", "region": "Orkney", "gender": "male", "age": 21},
    "vctk_p263": {"name": "Aberdeen Scottish Male (22)", "accent": "Scottish", "region": "Aberdeen", "gender": "male", "age": 22},
    "vctk_p272": {"name": "Edinburgh Scottish Male (23)", "accent": "Scottish", "region": "Edinburgh", "gender": "male", "age": 23},
    "vctk_p281": {"name": "Edinburgh Scottish Male (29)", "accent": "Scottish", "region": "Edinburgh", "gender": "male", "age": 29},
    
    # Scottish Females
    "vctk_p233": {"name": "Stornoway Scottish Female (23)", "accent": "Scottish", "region": "Stornoway", "gender": "female", "age": 23},
    "vctk_p236": {"name": "Orkney Scottish Female (23)", "accent": "Scottish", "region": "Orkney", "gender": "female", "age": 23},
    "vctk_p238": {"name": "Aberdeen Scottish Female (22)", "accent": "Scottish", "region": "Aberdeen", "gender": "female", "age": 22},
    "vctk_p239": {"name": "Inverness Scottish Female (22)", "accent": "Scottish", "region": "Inverness", "gender": "female", "age": 22},
    "vctk_p244": {"name": "Perth Scottish Female (22)", "accent": "Scottish", "region": "Perth", "gender": "female", "age": 22},
    "vctk_p248": {"name": "Shetland Scottish Female (23)", "accent": "Scottish", "region": "Shetland", "gender": "female", "age": 23},
    "vctk_p253": {"name": "Cardiff Scottish Female (22)", "accent": "Scottish", "region": "Cardiff", "gender": "female", "age": 22},
    "vctk_p261": {"name": "Edinburgh Scottish Female (26)", "accent": "Scottish", "region": "Edinburgh", "gender": "female", "age": 26},
    "vctk_p264": {"name": "Orkney Scottish Female (22)", "accent": "Scottish", "region": "Orkney", "gender": "female", "age": 22},
    
    # Irish
    "vctk_p245": {"name": "Dublin Irish Male (25)", "accent": "Irish", "region": "Dublin", "gender": "male", "age": 25},
    "vctk_p292": {"name": "Belfast Northern Irish Male (23)", "accent": "Northern Irish", "region": "Belfast", "gender": "male", "age": 23},
    "vctk_p240": {"name": "Cork Irish Female (21)", "accent": "Irish", "region": "Cork", "gender": "female", "age": 21},
    "vctk_p250": {"name": "Dublin Irish Female (21)", "accent": "Irish", "region": "Dublin", "gender": "female", "age": 21},
    "vctk_p257": {"name": "Belfast Northern Irish Female (19)", "accent": "Northern Irish", "region": "Belfast", "gender": "female", "age": 19},
    
    # Welsh
    "vctk_p251": {"name": "Cardiff Welsh Male (26)", "accent": "Welsh", "region": "Cardiff", "gender": "male", "age": 26},
    "vctk_p265": {"name": "Llanelli Welsh Female (21)", "accent": "Welsh", "region": "Llanelli", "gender": "female", "age": 21},
    "vctk_p266": {"name": "Port Talbot Welsh Female (22)", "accent": "Welsh", "region": "Port Talbot", "gender": "female", "age": 22},
    "vctk_p267": {"name": "Anglesey Welsh Female (23)", "accent": "Welsh", "region": "Anglesey", "gender": "female", "age": 23},
}

# Bark Models (Best for emotions, multiple speakers)
BARK_MODELS = {
    "bark": {
        "name": "Bark Multilingual",
        "supports_emotions": True,
        "supports_sound_effects": True,
        "supports_multiple_speakers": True,
        "quality": "high",
        "speed": "slow",
        "special_features": ["[laughs]", "[sighs]", "[music]", "[gasps]", "[clears throat]"]
    }
}

# Bark Speaker Presets (includes some British-sounding ones)
BARK_SPEAKERS = {
    "v2/en_speaker_0": {"name": "British Male 1", "accent": "British", "gender": "male"},
    "v2/en_speaker_1": {"name": "American Female 1", "accent": "American", "gender": "female"},
    "v2/en_speaker_2": {"name": "British Female 1", "accent": "British", "gender": "female"},
    "v2/en_speaker_3": {"name": "American Male 1", "accent": "American", "gender": "male"},
    "v2/en_speaker_4": {"name": "British Male 2", "accent": "British", "gender": "male"},
    "v2/en_speaker_5": {"name": "American Female 2", "accent": "American", "gender": "female"},
    "v2/en_speaker_6": {"name": "British Female 2", "accent": "British", "gender": "female"},
    "v2/en_speaker_7": {"name": "American Male 2", "accent": "American", "gender": "male"},
    "v2/en_speaker_8": {"name": "British Male 3", "accent": "British", "gender": "male"},
    "v2/en_speaker_9": {"name": "American Female 3", "accent": "American", "gender": "female"},
}

# Piper Models (Fast, lightweight, good quality)
PIPER_MODELS = {
    "en_GB_alba_medium": {
        "name": "Alba (Scottish)",
        "url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/alba/medium/en_GB-alba-medium.onnx",
        "config_url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/alba/medium/en_GB-alba-medium.onnx.json",
        "accent": "Scottish",
        "gender": "female",
        "quality": "medium",
        "speed": "fast"
    },
    "en_GB_cori_medium": {
        "name": "Cori (Northern English)",
        "url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/cori/medium/en_GB-cori-medium.onnx",
        "config_url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/cori/medium/en_GB-cori-medium.onnx.json",
        "accent": "Northern English",
        "gender": "female",
        "quality": "medium", 
        "speed": "fast"
    },
    "en_GB_jenny_dioco_medium": {
        "name": "Jenny (Southern English)",
        "url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/jenny_dioco/medium/en_GB-jenny_dioco-medium.onnx",
        "config_url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/jenny_dioco/medium/en_GB-jenny_dioco-medium.onnx.json",
        "accent": "Southern English",
        "gender": "female",
        "quality": "medium",
        "speed": "fast"
    },
    "en_GB_northern_english_male_medium": {
        "name": "Northern English Male",
        "url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/northern_english_male/medium/en_GB-northern_english_male-medium.onnx",
        "config_url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/northern_english_male/medium/en_GB-northern_english_male-medium.onnx.json",
        "accent": "Northern English",
        "gender": "male",
        "quality": "medium",
        "speed": "fast"
    }
}

# Engines configuration
TTS_ENGINES = {
    "coqui": {
        "name": "Coqui XTTS v2",
        "best_for": "Voice cloning, multilingual, highest quality",
        "supports_cloning": True,
        "supports_emotions": False,
        "speed": "medium",
        "quality": "highest",
        "models": COQUI_MODELS,
        "voices": XTTS_SPEAKERS
    },
    "bark": {
        "name": "Bark",
        "best_for": "Emotions, sound effects, multiple speakers",
        "supports_cloning": True,
        "supports_emotions": True,
        "speed": "slow",
        "quality": "high",
        "models": BARK_MODELS,
        "voices": BARK_SPEAKERS
    },
    "piper": {
        "name": "Piper", 
        "best_for": "Speed, efficiency, good quality",
        "supports_cloning": False,
        "supports_emotions": False,
        "speed": "fastest",
        "quality": "good",
        "models": PIPER_MODELS,
        "voices": PIPER_MODELS
    }
}

def get_all_voices():
    """Get all available voices organized by accent"""
    voices_by_accent = {
        "English": [],
        "Southern English": [],
        "Northern English": [],
        "Scottish": [],
        "Irish": [],
        "Northern Irish": [],
        "Welsh": [],
        "British": [],
        "American": [],
        "International": [],
        "French": [],
        "German": [],
        "Italian": [],
        "Spanish": [],
        "Dutch": [],
        "Scandinavian": [],
        "Indian": [],
        "Japanese": [],
        "Southern American": [],
        "Midwestern American": [],
        "Western American": [],
        "Northeastern American": []
    }
    
    # Add XTTS voices
    for voice_id, voice_info in XTTS_SPEAKERS.items():
        accent = voice_info["accent"]
        if accent in voices_by_accent:
            voices_by_accent[accent].append({
                "id": voice_id,
                "engine": "coqui",
                "name": voice_info["name"],
                "accent": accent,
                "gender": voice_info["gender"]
            })
    
    # Add Bark voices
    for voice_id, voice_info in BARK_SPEAKERS.items():
        accent = voice_info["accent"]
        if accent in voices_by_accent:
            voices_by_accent[accent].append({
                "id": voice_id,
                "engine": "bark",
                "name": voice_info["name"],
                "accent": accent,
                "gender": voice_info["gender"]
            })
    
    # Add Piper voices
    for voice_id, voice_info in PIPER_MODELS.items():
        accent = voice_info["accent"]
        if accent in voices_by_accent:
            voices_by_accent[accent].append({
                "id": voice_id,
                "engine": "piper",
                "name": voice_info["name"],
                "accent": accent,
                "gender": voice_info["gender"]
            })
            
    # Add VCTK voices for Coqui
    for voice_id, voice_info in VCTK_BRITISH_VOICES.items():
        accent = voice_info["accent"]
        if accent in voices_by_accent:
            voices_by_accent[accent].append({
                "id": voice_id,
                "engine": "coqui",
                "name": voice_info["name"],
                "accent": accent,
                "gender": voice_info["gender"]
            })
    
    return voices_by_accent

def get_recommended_voices():
    """Get a curated list of the best voices for testing"""
    return {
        "best_female_clear": "Claribel Dervla",                    # Clear female voice
        "best_female_warm": "Ana Florence",                        # Warm female voice
        "best_male_clear": "Andrew Chipper",                       # Clear male voice
        "best_male_deep": "Damien Black",                          # Deep male voice
        "best_international": "Sofia Hellen",                      # International accent
        "emotional_bark": "v2/en_speaker_2",                       # British Female for emotions
        "fastest_piper": "en_GB_cori_medium",                      # Fast Northern English
        "vale_like_voice": "en_GB_southern_english_female_low",    # Vale-like deep British female
        "default_british": "en_GB_southern_english_female_low"     # Default preferred voice
    }

# Update PIPER_MODELS to include the Vale-like voice
PIPER_MODELS.update({
    "en_GB_southern_english_female_low": {
        "name": "Vale (Deep British Female)",
        "url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/southern_english_female/low/en_GB-southern_english_female-low.onnx",
        "config_url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/southern_english_female/low/en_GB-southern_english_female-low.onnx.json",
        "accent": "Southern English",
        "gender": "female",
        "quality": "high",
        "speed": "fast",
        "recommended": True
    }
})
