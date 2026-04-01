#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import re
from datetime import datetime, timezone

STATE_FILE = "state.json"

def get_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_state(state):
    # Ensure last_run is always updated if omitted, or updated specifically
    if "last_run" not in state or state.get("_bump_time"):
        state["last_run"] = datetime.now(timezone.utc).isoformat()
    # remove temporary flags
    if "_bump_time" in state:
        del state["_bump_time"]
        
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def get_latest_session_uuid():
    res = subprocess.run(["gemini", "--list-sessions"], capture_output=True, text=True)
    if res.returncode != 0:
        return None
    matches = re.findall(r'\[([0-9a-fA-F\-]{36})\]', res.stdout)
    if matches:
        return matches[-1]
    return None

def main():
    state = get_state()
    last_run = state.get("last_run")
    session_uuid = state.get("session_uuid")
    
    agent_dir = os.path.dirname(os.path.abspath(__file__))
    policy_file = os.path.join(agent_dir, "agent_prompt.md")

    # 1. First run / Intro Loop
    if not last_run or not session_uuid:
        print("First run or missing session UUID. Triggering intro sequence...")
        intro_prompt = (
            "This is your very first execution! You are being introduced to Skyla. "
            "Please run the build script to create your inaugural site layout. "
            "Then, send a fun, silly, and grand introductory HTML email to Skyla "
            "explaining what you can do for her!"
        )
        
        gemini_cmd = [
            "gemini",
            "--prompt", intro_prompt,
            "--policy", policy_file
        ]
        
        res = subprocess.run(gemini_cmd, cwd=agent_dir)
        if res.returncode != 0:
            print("Failed to run intro sequence. Agent crashed or rate limited.", file=sys.stderr)
            # Even if it crashed, it might have spun up a session.
            # We will still try to grab the UUID to recover gracefully.
            
        print("Capturing session UUID...")
        new_uuid = get_latest_session_uuid()
        if new_uuid:
            print(f"Captured UUID: {new_uuid}")
            state["session_uuid"] = new_uuid
        else:
            print("Warning: Could not extract session UUID from gemini output.", file=sys.stderr)

        state["_bump_time"] = True
        save_state(state)
        # Even if first run failed, we save state to try subsequent runs properly
        sys.exit(res.returncode)

    # 2. Daily Loop
    read_cmd = [sys.executable, os.path.join(agent_dir, "skyla_read_email.py"), "--since", last_run]
    
    res = subprocess.run(read_cmd, capture_output=True, text=True, cwd=agent_dir)
    if res.returncode != 0:
        print("Error reading emails:", res.stderr, file=sys.stderr)
        sys.exit(1)
        
    try:
        emails = json.loads(res.stdout)
    except Exception as e:
        print("Failed to parse read output:", res.stdout, file=sys.stderr)
        sys.exit(1)

    if not emails:
        print("No new emails from Skyla. Ending early.")
        state["_bump_time"] = True
        save_state(state)
        sys.exit(0)

    print(f"Found {len(emails)} new email(s). Invoking agent with session {session_uuid}...")
    
    # Combine emails into single prompt
    prompt_lines = ["You have received new emails from Skyla since your last check:"]
    for e in emails:
        prompt_lines.append(f"Subject: {e['subject']}\nDate: {e['date']}\n\n{e.get('body', e.get('html_body', ''))}\n\n---")
    
    prompt_lines.append(
        "Please read her request, take any needed actions, execute build_site.py to update "
        "your static site to reflect your work, and finally use skyla_send_email.py to reply to her. "
        "Be sure to update her on your progress!"
    )
    
    prompt = "\n".join(prompt_lines)

    gemini_cmd = [
        "gemini", 
        "--prompt", prompt, 
        "--resume", session_uuid,
        "--policy", policy_file
    ]
    
    print("Running gemini agent...")
    gemini_res = subprocess.run(gemini_cmd, cwd=agent_dir)
    
    if gemini_res.returncode != 0:
        print("Agent execution failed.", file=sys.stderr)
    else:
        print("Agent execution completed.")
        
    state["_bump_time"] = True
    save_state(state)
    sys.exit(gemini_res.returncode)

if __name__ == "__main__":
    main()
