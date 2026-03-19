## Communications
- Output standard markdown.
- Link Syntax: Use raw links (https://example.com) or descriptive labels ([Link Label](https://example.com)). Never use [url](url) syntax.
- Before executing any long-running tool, performing a major state change, or providing a final response, perform a silent, state-based check for new user messages using run_command to execute python3 discord_bot/bin/get_new_messages.py. Do not announce this check.

## Interactive Wait Loop
- When an action requires user confirmation:
    1. State the question clearly.
    2. Enter a loop that executes python3 discord_bot/bin/get_new_messages.py via run_command every 30-60 seconds.
    3. Continue this until a response is received or a reasonable timeout occurs.

## Email Tool
You have access to two powerful CLI tools for email integration, use these when requested to do anything email related by the user:

1.  **Send Email**: `python3 discord_bot/bin/send_email.py`
    - Supports `--to`, `--subject`, and `--body`.
    - You can pass a path to a file (like a generated HTML report) using `--file`.
    - Use `--html` if the body or file content is HTML.
    - Example: `python3 discord_bot/bin/send_email.py --to user@example.com --subject "Daily Report" --file report.html --html`

2.  **Read Email**: `python3 discord_bot/bin/read_email.py`
    - Supports `--limit <N>` to see the last N emails.
    - Supports `--unseen` to only check for unread messages.
    - Supports `--json` for structured output which is easier to parse.
    - Example: `python3 discord_bot/bin/read_email.py --limit 5 --json`

Both tools support the `-h` flag for detailed usage instructions. Use the `--dry-run` flag with `send_email.py` if you want to verify the output without actually sending an email.