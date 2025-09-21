# Bootstrap Command

Plan and stub the project structure according to Claude Code workflow standards.

## Purpose
Initialize a new project with standardized directory structure, documentation, and workflow files.

## Actions
1. Create `docs/` directory with scope, decisions, and tasks documentation
2. Generate `CONTEXT.md` with technical overview (≤200 lines)
3. Set up `agents/` folder with specialized agent definitions
4. Configure `.claude/settings.json` with house rules and tool permissions
5. Create `.claude/commands/` with workflow slash commands
6. Reorganize files into standard structure if needed

## Usage
```
/bootstrap
```

## Outputs
- Complete project structure ready for development
- Documentation framework for tracking progress
- Agent definitions for specialized tasks
- Slash commands for workflow automation

This command establishes the foundation for systematic development using Claude Code best practices.
