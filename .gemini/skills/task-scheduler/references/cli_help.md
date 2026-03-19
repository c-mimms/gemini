# Task CLI Help

## task --help
```
usage: task [-h] {schedule,list,status,log,cancel,retry,monitor} ...

Background task scheduler CLI

positional arguments:
  {schedule,list,status,log,cancel,retry,monitor}
    schedule            Schedule a new task
    list                List all scheduled tasks
    status              Show detailed info for a task
    log                 View execution logs for a task
    cancel              Cancel a scheduled task
    retry               Manually retry a failed task
    monitor             Auto-refreshing task dashboard

options:
  -h, --help            show this help message and exit
```

## task schedule --help
```
usage: task schedule [-h] [--executor {shell,gemini}] [--command COMMAND]
                     [--context-file CONTEXT_FILE] [--name NAME] [--at AT] [--every EVERY]
                     [--cron CRON] [--max-retries MAX_RETRIES] [--timeout TIMEOUT]
                     [--overlap-policy {skip,queue,replace}] [--gemini-fallback]
                     [COMMAND]

positional arguments:
  COMMAND               Shell command to run (shorthand)

options:
  -h, --help            show this help message and exit
  --executor {shell,gemini}
  --command COMMAND     Explicit command (alternative to positional)
  --context-file CONTEXT_FILE
                        Path to context YAML/JSON for gemini executor
  --name NAME           Human-friendly task name
  --at AT               One-time schedule, e.g. "tomorrow at 9am"
  --every EVERY         Recurring interval, e.g. "day", "30 minutes"
  --cron CRON           Cron expression, e.g. "0 9 * * 1-5"
  --max-retries MAX_RETRIES
  --timeout TIMEOUT     Timeout in seconds
  --overlap-policy {skip,queue,replace}
  --gemini-fallback     On final failure, run a Gemini analysis task
```
