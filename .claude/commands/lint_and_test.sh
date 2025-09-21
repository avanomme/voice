#!/bin/bash
# Lint and test the voice assistant codebase

echo "🔍 Voice Assistant - Lint and Test"
echo "=================================="

cd "$(dirname "$0")/../.."

# Check if we're in the right directory
if [ ! -f "src/assistant/web_voice_assistant.py" ]; then
    echo "❌ Not in voice assistant project directory"
    exit 1
fi

echo "📁 Current directory: $(pwd)"

# Run ruff linting if available
if command -v ruff &> /dev/null; then
    echo "🔧 Running ruff linter..."
    ruff check src/ --fix || echo "⚠️  Linting issues found"
else
    echo "⚠️  ruff not found - skipping linting"
fi

# Run basic Python syntax check
echo "🐍 Checking Python syntax..."
python -m py_compile src/assistant/*.py && echo "✅ Python syntax OK" || echo "❌ Syntax errors found"

# Check if pytest is available and run tests
if command -v pytest &> /dev/null && [ -d "tests" ]; then
    echo "🧪 Running tests..."
    python -m pytest tests/ -v || echo "⚠️  Some tests failed"
else
    echo "⚠️  pytest not found or no tests directory - skipping tests"
fi

# Test imports and basic functionality
echo "📦 Testing critical imports..."
python -c "
try:
    from src.assistant import voice_models, tts_engines, error_logger
    print('✅ Core modules import successfully')
except Exception as e:
    print(f'❌ Import error: {e}')
"

# Check log directory
if [ -d "logs" ]; then
    echo "✅ Logs directory exists"
    ls -la logs/ | head -5
else
    echo "❌ Logs directory missing"
fi

echo "🏁 Lint and test completed!"