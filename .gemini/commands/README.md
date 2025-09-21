# Claude Code Workflow Commands

This directory contains workflow automation commands for the Voice Assistant project.

## Available Commands

### `/bootstrap` or `python .claude/commands/bootstrap.py`
Sets up the complete project structure according to Claude Code standards.

**Usage:**
```bash
python .claude/commands/bootstrap.py
```

**What it does:**
- Creates standard directory structure
- Sets up Claude configuration
- Verifies project health
- Shows next steps

### `/next_task` or `python .claude/commands/next_task.py`
Implements the automated task workflow from `next_task.md`.

**Usage:**
```bash
python .claude/commands/next_task.py
```

**What it does:**
- Reads tasks from `docs/03-tasks.json`
- Finds first task with status "todo"
- Provides detailed implementation guidance
- Shows required workflow steps:
  1. Read CONTEXT.md, docs/01-scope.md, and docs/03-tasks.json
  2. Implement task (unified PATCH DIFF only)
  3. Mark task status as "done" in docs/03-tasks.json
  4. Append completion to docs/02-decisions.md
  5. Regenerate CONTEXT.md (≤200 lines)
  6. Output JSON confirmation block
  7. Create commit and git push

### `/test_voice` or `.claude/commands/test_voice.sh`
Comprehensive voice functionality testing.

**Usage:**
```bash
.claude/commands/test_voice.sh
```

**What it does:**
- Tests web server health
- Checks wake word status
- Tests voice synthesis
- Auto-starts server if needed

### `/lint_and_test` or `.claude/commands/lint_and_test.sh`
Code quality and testing automation.

**Usage:**
```bash
.claude/commands/lint_and_test.sh
```

**What it does:**
- Runs ruff linting with auto-fix
- Checks Python syntax
- Runs pytest if available
- Tests critical imports
- Verifies project structure

## Workflow Integration

These commands are designed to work with Claude Code's slash command feature:

1. **Project Setup**: Start with `/bootstrap`
2. **Task Management**: Use `/next_task` to find what to work on
3. **Development**: Code changes, then `/lint_and_test`
4. **Testing**: Use `/test_voice` to verify functionality
5. **Iteration**: Return to `/next_task` for continuous workflow

## Voice Assistant Specific Features

- **Multi-engine TTS testing**: Tests Coqui, Bark, and Piper engines
- **Wake word validation**: Verifies continuous listening functionality
- **Error log monitoring**: Checks logging system health
- **British voice priority**: Maintains focus on UK/Irish/Australian accents
- **GPU optimization**: Considers CUDA memory usage for RTX 5060 Ti

## Configuration

Commands read from:
- `.claude/settings.json` - Project configuration
- `docs/tasks.md` - Task tracking
- `logs/` - Error and activity logs
- `src/assistant/` - Core voice modules

All commands are designed to be run from the project root directory.
