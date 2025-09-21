Read CONTEXT.md, docs/01-scope.md, and docs/03-tasks.json.

- Find the first task with "status":"todo".
- Implement it (return unified PATCH DIFF only, respecting House Rules).
- After implementing, mark that task's status as "done" in docs/03-tasks.json.
- Append one line to docs/02-decisions.md with the format:
  YYYY-MM-DD – Completed <task title> (<short rationale>).
- Regenerate CONTEXT.md (≤200 lines).
- Finally, output a JSON block confirming which task was completed.
- create commit message for git
- git push origin main
- After implementing the task, run /check to refresh .vscode/problems.json.
  For any Ruff diagnostics with `"fix": {"applicability":"safe"}`, apply the edit automatically.
  For others, show them in a list.

Output in order:
1) Unified PATCH DIFF.
2) Updated docs/03-tasks.json.
3) Updated docs/02-decisions.md.
4) Replacement CONTEXT.md.
5) run /check
6) JSON block { "task_completed": {...} }.
7) Create commit and push to git
