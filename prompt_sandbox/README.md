# Prompt Sandbox

This directory is an isolated environment for iterating on LLM prompts and testing engine logic (Museum, Georgia Mining, Trump, etc.) without cluttering the core application repositories.

## Structure

- `scripts/`: Implementation-specific research and data acquisition tasks.
- `prompts/`: Role-specific persona and instruction templates.
- `tests/`: Automated prompt iteration tests and trace logs.

## Automated Execution

To run these prompts on a recurring schedule (e.g., to generate daily museum articles or news digests), it is recommended to use the [Background Task Scheduler](../background-task-scheduler).

### Setup (macOS)
1. **Install the scheduler:**
   ```bash
   cd ../background-task-scheduler
   pip install -e .
   ```
2. **Install the LaunchAgent service:**
   ```bash
   ./bin/install_service.sh
   ```
3. **Schedule a sandbox task:**
   ```bash
   task schedule "python3 prompt_sandbox/tests/test_prompt_iteration.py" --every "12 hours" --name "sandbox-sync"
   ```

### Setup (PC / Windows)
The scheduler is optimized for Unix environments, but you can set it up on Windows via:

#### Option A: WSL (Recommended)
Follow the macOS instructions within a **Windows Subsystem for Linux (WSL)** terminal.

#### Option B: Windows Task Scheduler (Native)
1. Open **Task Scheduler** from the Start Menu.
2. Select **Create Basic Task**.
3. Set the **Trigger** (e.g., Daily).
4. Set the **Action** to `Start a Program`.
5. For **Program/script**, point to your `python.exe` path.
6. For **Add arguments**, provide the path to the script:
   `prompt_sandbox\tests\test_prompt_iteration.py`
7. For **Start in**, provide the absolute path to your `gemini` root directory.

---
*Note: Make sure your environment variables (like AI API keys) are set in your system environment or the `.env` file within the scheduler directory.*
