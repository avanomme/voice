import sys
import unittest
from pathlib import Path
import logging

# Add the src/assistant directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "assistant"))

from tts_engines import TTSEngineManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TestVoiceSelection(unittest.TestCase):
    def setUp(self):
        self.tts_manager = TTSEngineManager()
        self.test_text = "Hello, this is a test of the voice selection functionality."
        logging.info("Initialized TTSEngineManager for testing.")

    def test_coqui_voices(self):
        logging.info("Testing Coqui XTTS v2 voices...")
        # Test a few representative Coqui voices
        coqui_voices_to_test = [
            "Claribel Dervla", # International
            "Emily",           # British
            "Emma"             # American
        ]
        
        for voice_id in coqui_voices_to_test:
            with self.subTest(voice=voice_id):
                logging.info(f"Synthesizing with Coqui voice: {voice_id}")
                audio_base64 = self.tts_manager.speak(self.test_text, engine="coqui", voice_id=voice_id)
                self.assertIsNotNone(audio_base64, f"Coqui synthesis failed for voice: {voice_id}")
                self.assertGreater(len(audio_base64), 100, f"Coqui audio data too short for voice: {voice_id}")
                logging.info(f"Coqui voice {voice_id} tested successfully.")

    def test_coqui_vctk_voices(self):
        logging.info("Testing Coqui VCTK British voices...")
        # Test a few representative VCTK British voices
        vctk_voices_to_test = [
            "vctk_p243", # London Male
            "vctk_p228", # Southern England Female
            "vctk_p245"  # Dublin Irish Male
        ]

        for voice_id in vctk_voices_to_test:
            with self.subTest(voice=voice_id):
                logging.info(f"Synthesizing with Coqui VCTK voice: {voice_id}")
                audio_base64 = self.tts_manager.speak(self.test_text, engine="coqui", voice_id=voice_id)
                self.assertIsNotNone(audio_base64, f"Coqui VCTK synthesis failed for voice: {voice_id}")
                self.assertGreater(len(audio_base64), 100, f"Coqui VCTK audio data too short for voice: {voice_id}")
                logging.info(f"Coqui VCTK voice {voice_id} tested successfully.")

    def test_bark_voices(self):
        logging.info("Testing Bark voices...")
        # Test a few representative Bark voices
        bark_voices_to_test = [
            "v2/en_speaker_0", # British Male 1
            "v2/en_speaker_2", # British Female 1
            "v2/en_speaker_4"  # British Male 2
        ]

        for voice_id in bark_voices_to_test:
            with self.subTest(voice=voice_id):
                logging.info(f"Synthesizing with Bark voice: {voice_id}")
                audio_base64 = self.tts_manager.speak(self.test_text, engine="bark", voice_id=voice_id)
                self.assertIsNotNone(audio_base64, f"Bark synthesis failed for voice: {voice_id}")
                self.assertGreater(len(audio_base64), 100, f"Bark audio data too short for voice: {voice_id}")
                logging.info(f"Bark voice {voice_id} tested successfully.")

    def test_piper_voices(self):
        logging.info("Testing Piper voices...")
        # Test a few representative Piper voices
        piper_voices_to_test = [
            "en_GB_cori_medium", # Northern English
            "en_GB_jenny_dioco_medium", # Southern English
            "en_GB_alba_medium" # Scottish
        ]

        for voice_id in piper_voices_to_test:
            with self.subTest(voice=voice_id):
                logging.info(f"Synthesizing with Piper voice: {voice_id}")
                audio_base64 = self.tts_manager.speak(self.test_text, engine="piper", voice_id=voice_id)
                self.assertIsNotNone(audio_base64, f"Piper synthesis failed for voice: {voice_id}")
                self.assertGreater(len(audio_base64), 100, f"Piper audio data too short for voice: {voice_id}")
                logging.info(f"Piper voice {voice_id} tested successfully.")

if __name__ == '__main__':
    # Discover and run tests
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestVoiceSelection))
    
    # Use TextTestRunner to display results
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
