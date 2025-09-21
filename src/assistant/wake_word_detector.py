#!/usr/bin/env python3
"""
Wake Word Detection and Continuous Listening Module
Implements wake word detection with microphone permission handling
"""

import wave
import tempfile
import threading
import time
import os
import logging
from typing import Callable, Optional
import numpy as np

# Import error logging
from error_logger import log_wake_word_error, log_audio_error
from audio_manager import get_audio_manager

try:
    import webrtcvad
    VAD_AVAILABLE = True
except ImportError:
    VAD_AVAILABLE = False
    logging.warning("webrtcvad not available - wake word detection will be less efficient")

class WakeWordDetector:
    def __init__(self, wake_words=["hey assistant", "voice assistant"],
                 sample_rate=44100, chunk_duration=30):
        """
        Initialize wake word detector

        Args:
            wake_words: List of wake words to detect
            sample_rate: Audio sample rate
            chunk_duration: Audio chunk duration in milliseconds
        """
        self.wake_words = [word.lower() for word in wake_words]
        self.sample_rate = sample_rate
        self.chunk_duration = chunk_duration
        self.chunk_size = int(sample_rate * chunk_duration / 1000)

        # Voice Activity Detection
        if VAD_AVAILABLE:
            self.vad = webrtcvad.Vad(2)  # Aggressiveness level 0-3
        else:
            self.vad = None

        # Audio setup
        self.audio_manager = get_audio_manager()
        self.stream = None
        self.is_listening = False
        self.permission_granted = False

        # Whisper model check (cache the result to avoid spam)
        self.whisper_available = None
        self.whisper_warned = False

        # Callbacks
        self.on_wake_word: Optional[Callable] = None
        self.on_speech_detected: Optional[Callable] = None
        self.on_permission_error: Optional[Callable] = None

        self.logger = logging.getLogger(__name__)

    def request_microphone_permission(self) -> bool:
        """
        Request and verify microphone permissions from the OS
        Returns True if permission granted, False otherwise
        """
        try:
            # Use audio manager to test microphone access
            test_stream = self.audio_manager.create_input_stream(self.chunk_size)
            if test_stream is None:
                raise Exception("Failed to create audio input stream")

            # Try to read a small amount of data
            test_stream.start_stream()
            _ = test_stream.read(self.chunk_size, exception_on_overflow=False)
            test_stream.stop_stream()
            test_stream.close()

            self.permission_granted = True
            self.logger.info("Microphone permission granted")
            return True

        except Exception as e:
            self.permission_granted = False
            log_wake_word_error(e)
            if self.on_permission_error:
                self.on_permission_error(str(e))
            return False

    def _contains_wake_word(self, text: str) -> bool:
        """Check if text contains any wake words"""
        text_lower = text.lower()
        return any(wake_word in text_lower for wake_word in self.wake_words)

    def _is_speech(self, audio_chunk: bytes) -> bool:
        """Use VAD to detect if audio chunk contains speech"""
        if not VAD_AVAILABLE or not self.vad:
            # Fallback: simple energy-based detection
            audio_data = np.frombuffer(audio_chunk, dtype=np.int16)
            energy = np.sum(audio_data.astype(np.float32) ** 2) / len(audio_data)
            return energy > 1000000  # Threshold for speech detection

        try:
            return self.vad.is_speech(audio_chunk, self.sample_rate)
        except Exception as e:
            log_audio_error("VAD speech detection", e)
            return False

    def start_continuous_listening(self):
        """Start continuous listening for wake words"""
        if not self.permission_granted:
            if not self.request_microphone_permission():
                return False

        if self.is_listening:
            self.logger.warning("Already listening")
            return True

        try:
            # Use audio manager to create stream
            self.stream = self.audio_manager.create_input_stream(self.chunk_size)
            if self.stream is None:
                raise Exception("Failed to create audio input stream")

            self.stream.start_stream()
            self.is_listening = True
            self.listening_thread = threading.Thread(target=self._listen_loop, daemon=True)
            self.listening_thread.start()

            self.logger.info("Started continuous listening")
            return True

        except Exception:
            pass
        return False

    def stop_continuous_listening(self):
        """Stop continuous listening"""
        self.is_listening = False

        if self.stream:
            try:
                self.stream.stop_stream()
                self.stream.close()
            except Exception as e:
                log_audio_error("stopping stream", e)

        self.logger.info("Stopped continuous listening")

    def _listen_loop(self):
        """Main listening loop running in background thread"""
        audio_buffer = []
        speech_detected = False

        while self.is_listening:
            try:
                # Read audio chunk
                audio_chunk = self.stream.read(self.chunk_size, exception_on_overflow=False)

                # Check for speech activity
                if self._is_speech(audio_chunk):
                    audio_buffer.append(audio_chunk)
                    speech_detected = True

                    if self.on_speech_detected:
                        self.on_speech_detected()

                elif speech_detected and len(audio_buffer) > 0:
                    # Speech ended, process the buffer
                    self._process_speech_buffer(audio_buffer)
                    audio_buffer = []
                    speech_detected = False

                # Limit buffer size
                if len(audio_buffer) > 50:  # ~1.5 seconds
                    audio_buffer = audio_buffer[-50:]

            except Exception as e:
                log_wake_word_error(e)
                time.sleep(0.1)

    def _process_speech_buffer(self, audio_buffer):
        """Process accumulated speech audio for wake words"""
        try:
            # Save audio buffer to temp file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
                wf = wave.open(f.name, 'wb')
                wf.setnchannels(1)
                wf.setsampwidth(2)  # 16-bit
                wf.setframerate(self.sample_rate)
                wf.writeframes(b''.join(audio_buffer))
                wf.close()

                # Transcribe using Whisper (check once and cache result)
                if self.whisper_available is None:
                    try:
                        import whisper
                        self.whisper_model = whisper.load_model("base")
                        self.whisper_available = True
                        self.logger.info("Whisper model loaded for wake word detection")
                    except ImportError:
                        self.whisper_available = False
                        if not self.whisper_warned:
                            self.logger.warning("Whisper not available - wake word detection disabled")
                            self.whisper_warned = True
                    except Exception as e:
                        self.whisper_available = False
                        if not self.whisper_warned:
                            self.logger.warning("Whisper model not available for wake word transcription")
                            self.whisper_warned = True

                if self.whisper_available:
                    try:
                        result = self.whisper_model.transcribe(f.name)
                        text = result["text"].strip()

                        # Check for wake words
                        if self._contains_wake_word(text):
                            self.logger.info(f"Wake word detected: {text}")
                            if self.on_wake_word:
                                self.on_wake_word(text)
                    except Exception:
                        pass

                os.unlink(f.name)

        except Exception as e:
            log_wake_word_error(e)