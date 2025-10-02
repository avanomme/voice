#!/usr/bin/env python3
"""
Check for problems in .vscode/problems.json and fix them.
"""

import json
import subprocess
from pathlib import Path

def refresh_problems():
    """Run the refresh_problems.sh script"""
    print("🔄 Refreshing problems from VS Code...")
    script_path = Path(__file__).parent.parent.parent / "refresh_problems.sh"
    if not script_path.exists():
        print("⚠️ refresh_problems.sh not found.")
        return
    
    process = subprocess.run([str(script_path)], capture_output=True, text=True)
    if process.returncode != 0:
        print(f"❌ Error running refresh_problems.sh: {process.stderr}")
    else:
        print("✅ Problems refreshed.")

def read_problems():
    """Read problems from .vscode/problems.json"""
    problems_file = Path(__file__).parent.parent.parent / ".vscode" / "problems.json"

    if not problems_file.exists():
        print("✅ No problems file found.")
        return []

    with open(problems_file) as f:
        try:
            data = json.load(f)
            return data
        except json.JSONDecodeError:
            print("❌ Error decoding problems.json")
            return []

def apply_fix(problem):
    """Applies a single safe fix."""
    if not problem.get("fix") or not problem["fix"].get("edits"):
        return

    # For simplicity, we'll only handle the first edit.
    # Ruff's safe fixes usually have one edit.
    edit = problem["fix"]["edits"][0]
    file_path = problem["filename"]
    start_line = edit["location"]["row"]
    start_col = edit["location"]["column"]
    end_line = edit["end_location"]["row"]
    end_col = edit["end_location"]["column"]
    new_text = edit["content"]

    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        # This is a simplified way to apply edits.
        # It will work for single-line edits.
        # For multi-line edits, this will need to be more sophisticated.
        if start_line == end_line:
            line_index = start_line - 1
            original_line = lines[line_index]
            lines[line_index] = original_line[:start_col-1] + new_text + original_line[end_col-1:]
        else:
            # Simple multi-line edit: replace the lines with the new text
            line_start_index = start_line - 1
            line_end_index = end_line - 1
            
            new_lines = new_text.splitlines(True)

            lines = lines[:line_start_index] + new_lines + lines[line_end_index+1:]

        with open(file_path, 'w') as f:
            f.writelines(lines)
        
        print(f"✅ Applied safe fix to {file_path}:{start_line}")

    except Exception as e:
        print(f"❌ Error applying fix to {file_path}: {e}")


def main():
    """Main execution"""
    refresh_problems()
    print("🔍 Checking for problems...")
    problems = read_problems()

    if not problems:
        print("✅ No problems found.")
        return

    print(f"🚨 Found {len(problems)} problems.")
    
    safe_fixes = []
    other_problems = []

    for problem in problems:
        fix = problem.get("fix")
        if fix and fix.get("applicability") == "safe":
            safe_fixes.append(problem)
        else:
            other_problems.append(problem)

    if safe_fixes:
        print("\n🤖 Applying safe fixes automatically...")
        for problem in safe_fixes:
            apply_fix(problem)
    
    if other_problems:
        print("\n⚠️ Unsafe or unfixable problems found:")
        for problem in other_problems:
            print(f"  - {problem.get('filename')}:{problem.get('location',{}).get('row')}: {problem.get('message')}")

    if not safe_fixes and not other_problems:
        print("✅ No actionable problems found.")


if __name__ == "__main__":
    main()
