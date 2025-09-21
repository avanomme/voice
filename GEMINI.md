# Project Overview

This project is a multi-engine, local-first voice assistant with a web-based interface. It focuses on providing a wide range of voice options, particularly with British, Irish, and Australian accents. The assistant leverages several open-source text-to-speech (TTS) and speech-to-text (STT) engines, and is optimized for GPU acceleration.

## Main Technologies

*   **Backend:** Python, FastAPI, Uvicorn
*   **Frontend:** HTML, CSS, JavaScript
*   **Machine Learning:** PyTorch, Transformers
*   **TTS Engines:** Coqui XTTS v2, Bark, Piper
*   **STT Engine:** OpenAI Whisper
*   **Wake Word:** WebRTC VAD

## Architecture

The application is structured as a web server that provides a user interface for interacting with the voice assistant. The core logic is modular, with separate components for managing TTS engines, handling conversations, and detecting wake words.

*   `src/assistant/web_voice_assistant.py`: The main FastAPI application that serves the web UI and exposes API endpoints.
*   `src/assistant/tts_engines.py`: Manages the different TTS engines (Coqui, Bark, Piper).
*   `src/assistant/assistant_logic.py`: Handles the conversation flow and interacts with the language model.
*   `src/assistant/wake_word_detector.py`: Implements the wake word detection functionality.
*   `download_models.py`: A script for downloading all the necessary models for the TTS and STT engines.

# Building and Running

1.  **Install Dependencies:**

    The project uses a `requirements.txt` file to manage Python dependencies. To install them, run:

    ```bash
    pip install -r requirements.txt
    ```

2.  **Download Models:**

    Before running the application, you need to download the models for the different TTS and STT engines. The `download_models.py` script automates this process.

    ```bash
    python download_models.py
    ```

3.  **Run the Application:**

    The web application can be started by running the `web_voice_assistant.py` script.

    ```bash
    python src/assistant/web_voice_assistant.py
    ```

    The application will be available at `http://localhost:8765`.

# Development Conventions

*   **Code Style:** The code seems to follow the PEP 8 style guide, with a maximum line length of 88 characters.
*   **Testing:** The project has a `tests` directory, but it is not fully implemented. The `test_basic_tts.py` file provides a basic test for the TTS functionality.
*   **Modularity:** The code is organized into modules with specific responsibilities, which makes it easier to maintain and extend.
*   **Error Handling:** The application uses a custom logger to log errors to a file.
