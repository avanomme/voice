#!/usr/bin/env python3
"""
Next Task Command - Voice Assistant Workflow
Auto-selects and executes the next priority task
"""

import json
import os
from pathlib import Path

def load_tasks():
    """Load tasks from docs/tasks.md"""
    tasks_file = Path(__file__).parent.parent.parent / "docs" / "tasks.md"

    if not tasks_file.exists():
        return []

    tasks = []
    current_task = None

    with open(tasks_file) as f:
        for line in f:
            line = line.strip()
            if line.startswith("## Task"):
                # Extract task number and title
                if ":" in line:
                    task_part = line.split(":", 1)[1].strip()
                    current_task = {"title": task_part, "description": "", "status": "pending"}
                    tasks.append(current_task)
            elif line.startswith("**Status:**") and current_task:
                status = line.replace("**Status:**", "").strip()
                current_task["status"] = status.lower()
            elif line and current_task and not line.startswith("#"):
                current_task["description"] += line + " "

    return tasks

def get_next_task():
    """Get the next pending task"""
    tasks = load_tasks()

    for i, task in enumerate(tasks):
        if task["status"] in ["pending", "in progress"]:
            return i, task

    return None, None

def main():
    """Main execution"""
    print("🎯 Voice Assistant - Next Task Selector")
    print("=====================================")

    task_num, task = get_next_task()

    if task is None:
        print("✅ All tasks completed!")
        return

    print(f"📋 Next Task: #{task_num}")
    print(f"📝 Title: {task['title']}")
    print(f"📖 Description: {task['description'].strip()}")
    print(f"🏷️  Status: {task['status']}")
    print()

    print("🚀 Suggested actions:")

    # Task-specific suggestions
    title_lower = task['title'].lower()

    if "wake word" in title_lower:
        print("   • Test wake word detection: .claude/commands/test_voice.sh")
        print("   • Check wake word logs: tail -f logs/voice_assistant.log")
        print("   • Test microphone permissions")

    elif "tts" in title_lower or "voice" in title_lower:
        print("   • Test voice synthesis: python src/assistant/test_tts.py")
        print("   • Download models: python download_models.py")
        print("   • Check GPU utilization: nvidia-smi")

    elif "web" in title_lower or "interface" in title_lower:
        print("   • Start web interface: python src/assistant/web_voice_assistant.py")
        print("   • Test endpoints: curl http://localhost:8765/health")
        print("   • Check browser console for errors")

    elif "error" in title_lower or "logging" in title_lower:
        print("   • Check error logs: tail -f logs/errors.log")
        print("   • Test error handling scenarios")
        print("   • Verify log file permissions")

    else:
        print("   • Review task requirements carefully")
        print("   • Check related documentation in docs/")
        print("   • Test relevant functionality")

    print()
    print("💡 Pro tip: Run 'python .claude/commands/next_task.py' anytime to see current priority")

if __name__ == "__main__":
    main()