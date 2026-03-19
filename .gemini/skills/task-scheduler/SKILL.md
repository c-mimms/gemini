---
name: task-scheduler
description: Schedule one-time and recurring shell or Gemini tasks using the 'task' CLI tool. Use when the user asks for a command to be run later, on a schedule, or as a background job.
---

# Task Scheduler

This skill provides the ability to schedule tasks for later or recurring execution using the `task` CLI tool. It supports both simple shell commands and complex Gemini agentic tasks.

## Quick Start

- **One-time task**: `task schedule "echo hello" --at "tomorrow at 9am"`
- **Recurring task**: `task schedule "python3 script.py" --every "day" --name "daily-job"`
- **Gemini agentic task**: `task schedule --executor gemini --context-file task.yaml --every "week"`

## Task Scheduling

### 1. One-time Tasks
Use the `--at` flag with natural language descriptors (e.g., "in 5 minutes", "tomorrow at 3pm", "next friday").

```bash
task schedule "command" --at "time"
```

### 2. Recurring Tasks
Use the `--every` flag for intervals or `--cron` for standard cron expressions.

- **Intervals**: "10 minutes", "hour", "day", "week", "month"
- **Cron**: "0 9 * * 1-5" (every weekday at 9am)

```bash
task schedule "command" --every "interval"
task schedule "command" --cron "expression"
```

### 3. Gemini Executor
For tasks that require AI reasoning, use the `gemini` executor. This requires a `--context-file` (YAML/JSON) that contains the prompt or context for the agent.

```bash
task schedule --executor gemini --context-file /path/to/context.yaml --every "day"
```

## Task Management

- **List Tasks**: `task list` (shows ID, name, schedule, last run, status)
- **Task Status**: `task status <id>` (detailed info, including next run time)
- **View Logs**: `task log <id>` (stdout/stderr from last execution)
- **Cancel Task**: `task cancel <id>`
- **Retry Task**: `task retry <id>` (manually trigger a failed task)

## Examples

### Email Reminder
```bash
task schedule "mail -s 'Reminder' user@example.com < /path/to/msg.txt" --at "next week"
```

### Morning Email Summary (Gemini Agent)
```bash
# Create summary_task.yaml with the prompt
# task schedule --executor gemini --context-file summary_task.yaml --every "day"
```

### Weekly Job
```bash
task schedule "run-aggregation-job" --every "week"
```

## Advanced Features

- **Gemini Fallback**: Use `--gemini-fallback` to automatically trigger a Gemini analysis task if a shell command fails all retries.
- **Max Retries**: Use `--max-retries N` to specify the number of times to retry a failed task (with exponential backoff).
- **Timeout**: Use `--timeout N` to set an execution timeout in seconds.
- **Overlap Policy**: Use `--overlap-policy {skip,queue,replace}` to handle cases where a new instance of a task starts before the previous one finished.

## Resources
- [CLI Help](references/cli_help.md): Full CLI help documentation.
