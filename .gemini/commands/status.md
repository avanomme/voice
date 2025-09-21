# Status Command

Show current project progress and remaining tasks.

## Purpose
Provide a quick overview of project completion status and identify what work remains to be done.

## Actions
1. Read docs/03-tasks.json
2. Count tasks by status (todo, in-progress, done)
3. Calculate completion percentage
4. List remaining todo tasks with priorities
5. Identify any blocked or overdue tasks

## Usage
```
/status
```

## Output Format
```
Project Status:
- Total Tasks: X
- Completed: Y (Z%)
- In Progress: A
- Todo: B

Remaining Tasks:
1. [High] Task Title (ID: X)
2. [Medium] Task Title (ID: Y)
...
```

## Benefits
- Quick progress assessment
- Priority-based task visibility
- Completion tracking
- Workload planning
