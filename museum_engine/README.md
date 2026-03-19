# Mimms Museum Engine (Standalone Replacement)

This is a standalone, end-to-end replacement for the original museum pipeline. It generates a new museum article per run, stores selected format inside run metadata, stores research facts and sources as graph nodes, and can publish the site using the same static build script.

## What This Replaces
It mirrors the behavior of `/Users/chris/code/gemini/discord_bot/scripts/museum_task.md` but writes to a **new, self-contained** directory:
- Articles go to `/Users/chris/code/gemini/museum_engine/articles/`
- Research and state live under `/Users/chris/code/gemini/museum_engine/state/`

The original pipeline is untouched.

## Quick Start
```
python3 /Users/chris/code/gemini/museum_engine/cli/run_museum.py --offline
```

This runs in offline mode and uses a stub model. It will create one HTML file in `museum_engine/articles/`.

## Real Web Research + LLM Output
To run with web research and a real model:

1. Install dependencies (optional, required for OpenAI):
```
pip install openai
```

2. Set environment variables:
```
export MUSEUM_ENGINE_MODEL=openai
export OPENAI_API_KEY=your_key_here
```

3. Run:
```
python3 /Users/chris/code/gemini/museum_engine/cli/run_museum.py
```

This will attempt to search the web and download a small set of Wikimedia Commons images when available.

## Publish
```
python3 /Users/chris/code/gemini/museum_engine/cli/run_museum.py --publish
```

## Config and Prompts
- Config: `/Users/chris/code/gemini/museum_engine/configs/museum_engine.json`
- Prompt: `/Users/chris/code/gemini/museum_engine/prompts/museum_task.md`

## Tests
```
python3 -m unittest /Users/chris/code/gemini/museum_engine/tests/test_museum_pipeline.py
```
