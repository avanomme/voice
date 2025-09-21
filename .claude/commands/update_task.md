# Update Task Command

Manually mark a task as done in the task tracking system.

## Purpose
Provide manual control over task status when work is completed outside the normal workflow or when tasks need to be marked as done without implementation.

## Actions
1. Read current docs/03-tasks.json
2. Find task by ID or title
3. Update status to "done"
4. Add completion timestamp
5. Log decision in docs/02-decisions.md

## Usage
```
/update_task <task_id>
```

## Example
```
/update_task 5
```

## Parameters
- `task_id`: Numeric ID of the task to mark as done

## Outputs
- Updated docs/03-tasks.json with status change
- New entry in docs/02-decisions.md
- Confirmation of task update
