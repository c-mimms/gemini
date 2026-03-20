---
name: agent_tools
description: Core tools available for agents to use (e.g., sending and reading emails).
---
# Agent Tools Skill

This folder contains tools that can be used by any agent.
Currently, it provides email capabilities:
- `read_email.py`: Read emails from an IMAP server (supports JSON output and saving attachments).
- `send_email.py`: Send emails using an SMTP server (supports attachments and HTML).

These tools require an `.env` file in the `agent_tools` directory containing your IMAP/SMTP credentials. See `.env.example` for required variables.

Example usage:
```bash
python3 agent_tools/read_email.py --limit 5 --json
python3 agent_tools/send_email.py --to user@example.com --subject "Hello" --body "World"
```
