#!/usr/bin/env python3
"""
Bootstrap Command - Voice Assistant Project Setup
Sets up project structure according to Claude Code workflow standards
"""

import os
import json
from pathlib import Path

def create_directory_structure():
    """Create standard Claude Code directory structure"""
    directories = [
        "docs",
        "agents",
        ".claude",
        ".claude/commands",
        "logs",
        "tests",
        "scripts"
    ]

    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {dir_path}")

def setup_claude_config():
    """Ensure .claude configuration is present"""
    claude_dir = Path(".claude")

    # Settings file
    settings_file = claude_dir / "settings.json"
    if not settings_file.exists():
        settings = {
            "house_rules": [
                "Always test voice functionality after TTS changes",
                "Maintain error logging for all operations",
                "Preserve British/Irish/Australian voice priorities"
            ],
            "voice_assistant": {
                "default_voice": "en_GB-southern_english_female-low",
                "priority_engines": ["piper", "coqui", "bark"]
            }
        }
        with open(settings_file, "w") as f:
            json.dump(settings, f, indent=2)
        print(f"✅ Created: {settings_file}")

def verify_project_health():
    """Verify project is properly set up"""
    checks = [
        ("src/assistant/voice_models.py", "Voice models configuration"),
        ("src/assistant/tts_engines.py", "TTS engine management"),
        ("src/assistant/web_voice_assistant.py", "Web interface"),
        ("src/assistant/error_logger.py", "Error logging system"),
        ("src/assistant/wake_word_detector.py", "Wake word detection"),
        ("logs", "Logging directory"),
        (".claude/settings.json", "Claude configuration")
    ]

    print("\\n🔍 Project Health Check:")
    all_good = True

    for path, description in checks:
        if Path(path).exists():
            print(f"✅ {description}: {path}")
        else:
            print(f"❌ Missing {description}: {path}")
            all_good = False

    return all_good

def show_next_steps():
    """Show recommended next steps"""
    print("\\n🚀 Bootstrap Complete! Next Steps:")
    print("1. Run voice tests: .claude/commands/test_voice.sh")
    print("2. Check current task: python .claude/commands/next_task.py")
    print("3. Start web interface: python src/assistant/web_voice_assistant.py")
    print("4. Monitor logs: tail -f logs/voice_assistant.log")
    print("\\n💡 Use slash commands like /next_task for workflow automation")

def main():
    """Main bootstrap execution"""
    print("🎤 Voice Assistant Project Bootstrap")
    print("===================================")

    print("\\n📁 Setting up directory structure...")
    create_directory_structure()

    print("\\n⚙️  Configuring Claude Code settings...")
    setup_claude_config()

    print("\\n🏥 Verifying project health...")
    health_ok = verify_project_health()

    if health_ok:
        print("\\n✅ Project bootstrap successful!")
        show_next_steps()
    else:
        print("\\n⚠️  Some components missing - check setup")

if __name__ == "__main__":
    main()