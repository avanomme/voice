#!/usr/bin/env python3
"""
Audio Manager for Voice Assistant
Handles audio input/output with fallback mechanisms for different systems
"""

import pyaudio
import os
import logging
import subprocess
import shutil
from pathlib import Path
from typing import Optional, List
from error_logger import log_audio_error

class AudioManager:
    def __init__(self):
        """Initialize audio manager with best available audio system"""
        self.logger = logging.getLogger(__name__)
        self.audio = None
        self.preferred_device = None
        self.sample_rate = 16000
        self.channels = 1
        self.format = pyaudio.paInt16

        # Suppress ALSA/JACK error messages
        self._suppress_audio_errors()

        # Find best audio device
        self._find_best_audio_device()

    def _suppress_audio_errors(self):
        """Suppress ALSA and JACK error messages"""
        # Redirect ALSA errors to null
        os.environ['ALSA_LOG_LEVEL'] = '0'

        # Set environment variables to avoid JACK/PulseAudio conflicts
        os.environ['PULSE_RUNTIME_PATH'] = '/tmp/pulse-runtime'

        # Disable problematic audio outputs
        devnull = open(os.devnull, 'w')
        os.dup2(devnull.fileno(), 2)  # Redirect stderr temporarily

    def _find_best_audio_device(self):
        """Find the best available audio input device"""
        try:
            self.audio = pyaudio.PyAudio()

            # Get default input device
            default_input = self.audio.get_default_input_device_info()
            self.preferred_device = default_input['index']

            self.logger.info(f"Using audio device: {default_input['name']}")

        except Exception as e:
            log_audio_error("device detection", e)
            self.preferred_device = None

    def create_input_stream(self, chunk_size: int = 1024):
        """Create an audio input stream with error handling"""
        try:
            if not self.audio:
                self.audio = pyaudio.PyAudio()

            stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                input_device_index=self.preferred_device,
                frames_per_buffer=chunk_size,
                start=False  # Don't start immediately
            )

            return stream

        except Exception as e:
            log_audio_error("input stream creation", e)
            return None

    def test_audio_playback(self, text: str = "Audio test") -> bool:
        """Test audio playback using available system"""
        try:
            # Try different TTS methods in order of preference
            tts_methods = [
                self._try_piper_tts,
                self._try_espeak_tts,
                self._try_festival_tts
            ]

            for method in tts_methods:
                if method(text):
                    return True

            self.logger.warning("No working TTS method found")
            return False

        except Exception as e:
            log_audio_error("audio playback test", e)
            return False

    def _try_piper_tts(self, text: str) -> bool:
        """Try Piper TTS if available"""
        try:
            if shutil.which('piper'):
                # Use a simple Piper model if available
                cmd = ['piper', '--model', 'en_US-lessac-medium', '--output_file', '/tmp/test_audio.wav']
                process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                process.communicate(input=text.encode())

                # Play the audio
                if Path('/tmp/test_audio.wav').exists():
                    subprocess.run(['aplay', '/tmp/test_audio.wav'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    os.unlink('/tmp/test_audio.wav')
                    return True
        except:
            pass
        return False

    def _try_espeak_tts(self, text: str) -> bool:
        """Try espeak TTS if available"""
        try:
            if shutil.which('espeak'):
                subprocess.run(['espeak', text], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return True
        except:
            pass
        return False

    def _try_festival_tts(self, text: str) -> bool:
        """Try Festival TTS if available"""
        try:
            if shutil.which('festival'):
                cmd = ['festival', '--tts']
                process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                process.communicate(input=text.encode())
                return True
        except:
            pass
        return False

    def get_available_devices(self) -> List[dict]:
        """Get list of available audio devices"""
        devices = []
        try:
            if not self.audio:
                self.audio = pyaudio.PyAudio()

            for i in range(self.audio.get_device_count()):
                try:
                    device_info = self.audio.get_device_info_by_index(i)
                    if device_info['maxInputChannels'] > 0:  # Input device
                        devices.append({
                            'index': i,
                            'name': device_info['name'],
                            'channels': device_info['maxInputChannels'],
                            'sample_rate': device_info['defaultSampleRate']
                        })
                except:
                    continue

        except Exception as e:
            log_audio_error("device enumeration", e)

        return devices

    def cleanup(self):
        """Clean up audio resources"""
        try:
            if self.audio:
                self.audio.terminate()
                self.audio = None
        except Exception as e:
            log_audio_error("cleanup", e)

    def __del__(self):
        """Destructor to ensure cleanup"""
        self.cleanup()

# Global audio manager instance
_audio_manager: Optional[AudioManager] = None

def get_audio_manager() -> AudioManager:
    """Get or create the global audio manager instance"""
    global _audio_manager
    if _audio_manager is None:
        _audio_manager = AudioManager()
    return _audio_manager