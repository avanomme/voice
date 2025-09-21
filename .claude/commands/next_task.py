#!/usr/bin/env python3
"""
Next Task Command - Voice Assistant Workflow
Implements the automated task workflow as specified in next_task.md
"""

import json
from pathlib import Path

def load_tasks():
    """Load tasks from docs/03-tasks.json"""
    tasks_file = Path(__file__).parent.parent.parent / "docs" / "03-tasks.json"

    if not tasks_file.exists():
        return []

    with open(tasks_file) as f:
        data = json.load(f)
        return data.get("tasks", [])

def get_next_todo_task():
    """Get the first task with status 'todo'"""
    tasks = load_tasks()

    for task in tasks:
        if task.get("status") == "todo":
            return task

    return None

def main():
    """Main execution following next_task.md workflow"""
    print("🎯 Voice Assistant - Next Task Workflow")
    print("=======================================")

    # Step 1: Find first task with status "todo"
    task = get_next_todo_task()

    if task is None:
        print("✅ No tasks with status 'todo' found!")
        print("🎉 All current tasks are completed or in progress.")
        return

    print("📋 Next Task Found:")
    print(f"   • ID: {task['id']}")
    print(f"   • Title: {task['title']}")
    print(f"   • Description: {task['description']}")
    print(f"   • Priority: {task['priority']}")
    print(f"   • Category: {task['category']}")
    print(f"   • Estimated Hours: {task['estimated_hours']}")
    if task.get('dependencies'):
        print(f"   • Dependencies: {task['dependencies']}")
    print(f"   • Tags: {', '.join(task['tags'])}")
    print()

    print("📚 Required workflow steps:")
    print("1. Read CONTEXT.md, docs/01-scope.md, and docs/03-tasks.json")
    print("2. Implement the task (return unified PATCH DIFF only)")
    print("3. Mark task status as 'done' in docs/03-tasks.json")
    print("4. Append completion entry to docs/02-decisions.md")
    print("5. Regenerate CONTEXT.md (≤200 lines)")
    print("6. Run /check to inspect and fix any errors in .vscode/problems.json")
    print("7. Output JSON confirmation block")
    print("8. Create commit message and git push")
    print()

    print("🚀 Implementation guidance:")
    category = task.get('category', '').lower()

    if 'web-ui' in category:
        print("   • Focus on web_voice_assistant.py and UI components")
        print("   • Test in browser: http://localhost:8765")
        print("   • Check browser console for errors")

    elif 'voice' in category or 'models' in category:
        print("   • Review voice_models.py and tts_engines.py")
        print("   • Test voice synthesis functionality")
        print("   • Verify model loading and availability")

    elif 'system-integration' in category:
        print("   • Implement secure permission framework")
        print("   • Create YAML configuration system")
        print("   • Add logging for all system access")

    elif 'ai-learning' in category:
        print("   • Design pluggable skills framework")
        print("   • Implement local memory persistence")
        print("   • Create developer documentation")

    elif 'testing' in category:
        print("   • Create comprehensive test suite")
        print("   • Verify all engines and voices work")
        print("   • Test error handling scenarios")

    else:
        print(f"   • Review category: {category}")
        print("   • Check existing codebase for patterns")
        print("   • Follow established conventions")

    print()
    print("⚠️  Remember:")
    print("   • Return unified PATCH DIFF only for code changes")
    print("   • Limit patches to ≤3 files or ≤50 lines per change")
    print("   • Split large patches into smaller, focused changes")
    print("   • Follow existing code style and patterns")
    print("   • No comments in code unless explicitly requested")

if __name__ == "__main__":
    main()