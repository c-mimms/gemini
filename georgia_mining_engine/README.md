# Georgia Mining Research Engine (Standalone Replacement)

This is a standalone, research‑focused replacement for the original Georgia mining pipeline. It prioritizes data profiling and explicit dataset‑backed findings.

## What This Replaces
It mirrors the behavior of `/Users/chris/code/gemini/discord_bot/scripts/georgia_mining_task.md` but writes to a **new, self‑contained** directory:
- Articles: `/Users/chris/code/gemini/georgia_mining_engine/articles/`
- Data: `/Users/chris/code/gemini/georgia_mining_engine/data/`
- State: `/Users/chris/code/gemini/georgia_mining_engine/state/`

The original pipeline is untouched.

## Quick Start (Offline)
```
python3 /Users/chris/code/gemini/georgia_mining_engine/cli/run_georgia_mining.py --offline
```

## Real Model Output
```
export MUSEUM_ENGINE_MODEL=openai
export OPENAI_API_KEY=your_key_here
python3 /Users/chris/code/gemini/georgia_mining_engine/cli/run_georgia_mining.py
```

## Publish
```
python3 /Users/chris/code/gemini/georgia_mining_engine/cli/run_georgia_mining.py --publish
```

## Config and Prompt
- Config: `/Users/chris/code/gemini/georgia_mining_engine/configs/georgia_mining_engine.json`
- Prompt: `/Users/chris/code/gemini/georgia_mining_engine/prompts/georgia_mining_task.md`

## Tests
```
python3 -m unittest /Users/chris/code/gemini/georgia_mining_engine/tests/test_georgia_mining_pipeline.py
```
