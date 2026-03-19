# Background Task Scheduler: Improvement Ideas

Date: 2026-03-10

## Nice-to-Have

- Show relative last/next run times in `task list` (e.g., "in 4 hours", "3m ago").

## Completed

- Add daemon startup reconciliation that marks `running` executions as `failed` or `abandoned` with a clear reason when the daemon restarts.
- Implement the `queue` and `replace` overlap policies (currently only `skip` is effectively enforced).
- Add a per-task working directory (`--cwd`) and propagate it to subprocesses.
- Set a default `WorkingDirectory` for the daemon service to avoid scanning `/`.
- Add kill-tree behavior for timeouts to terminate subprocess children.
- Allow per-task concurrency limits to override the global daemon limit.

## High Impact

- Implement misfire handling for cron/natural schedules (e.g., run-once if missed vs skip) with a configurable policy.
- Add a retention policy for old execution rows and logs, plus a `task prune` command.
- Make database writes more resilient on `database is locked` by using retries with backoff.

## Medium Impact

- Add an execution heartbeat and detect stuck executions to prevent silent hangs.
- Track per-execution duration and expose a `task stats` CLI for recent durations and failure rates.
- Support explicit timezones per task instead of assuming local time.
- Add jitter to retry backoff to avoid thundering herd effects.
- Support running commands without a shell for safer argument handling.
- Capture and store environment diffs so runs are reproducible.
- Add a per-task `max_concurrent` enforcement in the scheduler loop.
- Expose `task tail <id>` that follows the current execution logs even if the task restarts.
- Add `task explain <id>` to summarize recent failures and retries.
- Add colored output and structured JSON output for automation.
- Provide a `task health` command for DB connectivity, daemon status, and queue depth.
- Support explicit disabling of workspace discovery or directory scanning for Gemini tasks that do not need it.
- Allow explicit `--include-directories` or a per-task workspace root for Gemini tasks.
- Capture the exact Gemini CLI version used per execution.
- Add a safe mode that disables tool usage for tasks that should only generate text.
- Add an allowlist for executors per task to prevent accidental executor changes.
- Add a configurable redaction pipeline for logs.

## Lower Impact

- For `replace`, stop the prior execution and record the reason as `replaced_by`.
- Optionally encrypt stored stdout/stderr at rest for sensitive tasks.
- Add launchd/systemd templates that set explicit working directory and environment.
- Provide a `taskd doctor` command to validate PATH, credentials, and permissions.
