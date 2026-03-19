#!/usr/bin/env python3
import asyncio
import os
import sys
import time
import json
from datetime import datetime

# Adjust Python path so we can import src.app.runner easily
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app.runner import run_next_turn

async def main():
    if len(sys.argv) < 2:
        print("Usage: python test_prompt_iteration.py <input_file_path>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"Error: file not found: {input_file}")
        sys.exit(1)

    with open(input_file, "r") as f:
        content = f.read().strip()

    # Setup directories
    basename = os.path.splitext(os.path.basename(input_file))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bot_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_dir = os.path.join(bot_dir, "tests", "prompt_tests", "out", f"{basename}_{timestamp}")
    os.makedirs(out_dir, exist_ok=True)

    print(f"[*] Starting prompt iteration test for: {basename}")
    print(f"[*] Output directory: {out_dir}")

    # Set up environ for runner
    os.environ["DEBUG_PROMPT_DUMP"] = "1"
    os.environ["DEBUG_PROMPT_DUMP_DIR"] = out_dir
    os.environ["GEMINI_RUNNER_DEBUG"] = "1"

    latest_message = {
        "id": f"test_{timestamp}",
        "content": content,
        "timestamp": time.time(),
        "source": "user"
    }

    transcript_path = os.path.join(out_dir, "transcript.txt")
    events_path = os.path.join(out_dir, "events.jsonl")

    print("[*] Running conversation turn...")
    with open(transcript_path, "w") as t_file, open(events_path, "w") as e_file:
        t_file.write(f"User: {content}\n\n")
        
        async for event in run_next_turn(latest_message, context_id="test_context", project_root=bot_dir):
            event_dict = {
                "type": event.type,
                "content": event.content,
                "metadata": event.metadata
            }
            e_file.write(json.dumps(event_dict) + "\n")
            
            if event.type == "text":
                sys.stdout.write(event.content)
                sys.stdout.flush()
                t_file.write(event.content)
            elif event.type == "status":
                pass
            elif event.type == "error":
                print(f"\n[ERROR]: {event.content}")
                t_file.write(f"\n[ERROR]: {event.content}\n")
            elif event.type == "tool_use":
                print(f"\n[BOT TOOL]: {event.content}")
                t_file.write(f"\n[BOT TOOL]: {event.content}\n")

    print(f"\n\n[*] Test run complete. Outputs saved in {out_dir}")
    print(f"[*] Prompt text used is at {os.path.join(out_dir, 'prompt_dump.txt')}")

if __name__ == "__main__":
    asyncio.run(main())
