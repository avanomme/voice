#!/bin/bash
# Test voice functionality across all engines

echo "🎙️ Testing Voice Assistant Functionality"
echo "========================================"

# Check if web server is running
if curl -s http://localhost:8765/health > /dev/null; then
    echo "✅ Web server is running"

    # Test health endpoint
    echo "📊 Health check:"
    curl -s http://localhost:8765/health | jq .

    # Test wake word status
    echo "🎧 Wake word status:"
    curl -s http://localhost:8765/wake-word/status | jq .

    # Test simple voice generation
    echo "🔊 Testing voice synthesis:"
    curl -s -X POST http://localhost:8765/test-voice \
         -H "Content-Type: application/json" \
         -d '{"text": "Voice test successful", "voice": "coqui:vctk_p243"}' | jq .

else
    echo "❌ Web server not running - starting it..."
    cd "$(dirname "$0")/../.." && python src/assistant/web_voice_assistant.py &
    sleep 5
    echo "🔄 Retrying tests..."
    $0  # Retry this script
fi