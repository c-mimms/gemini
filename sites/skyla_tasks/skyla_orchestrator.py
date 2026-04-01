#!/usr/bin/env python3
import os
import sys
import json
import subprocess
from datetime import datetime, timezone

STATE_FILE = "state.json"
SESSION_UUID = "skyla-main-session"

def get_last_run():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            data = json.load(f)
            return data.get("last_run")
    return None

def set_last_run():
    now = datetime.now(timezone.utc).isoformat()
    with open(STATE_FILE, "w") as f:
        json.dump({"last_run": now}, f)

def main():
    last_run = get_last_run()
    
    # 1. First run / Intro Loop
    if not last_run:
        print("First run detected. Triggering intro sequence...")
        intro_prompt = (
            "This is your very first execution! You are being introduced to Skyla. "
            "Please run the build script to create your inaugural site layout. "
            "Then, send a fun, silly, and grand introductory HTML email to Skyla "
            "explaining what you can do for her!"
        )
        agent_dir = os.path.dirname(os.path.abspath(__file__))
        policy_file = os.path.join(agent_dir, "agent_prompt.md")
        
        gemini_cmd = [
            "gemini",
            "--prompt", intro_prompt,
            "--resume", SESSION_UUID,
            "--policy", policy_file
        ]
        res = subprocess.run(gemini_cmd, cwd=agent_dir)
        if res.returncode != 0:
            print("Failed to run intro sequence.", file=sys.stderr)
            sys.exit(res.returncode)
            
        print("Intro sequence complete.")
        set_last_run()
        sys.exit(0)

    # 2. Daily Loop
    agent_dir = os.path.dirname(os.path.abspath(__file__))
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
        set_last_run()
        sys.exit(0)

    print(f"Found {len(emails)} new email(s). Invoking agent...")
    
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

    policy_file = os.path.join(agent_dir, "agent_prompt.md")
    
    gemini_cmd = [
        "gemini", 
        "--prompt", prompt, 
        "--resume", SESSION_UUID,
        "--policy", policy_file
    ]
    
    print("Running gemini agent...")
    gemini_res = subprocess.run(gemini_cmd, cwd=agent_dir)
    
    if gemini_res.returncode != 0:
        print("Agent execution failed.", file=sys.stderr)
        # Even on failure, advance the last run time so we don't loop forever failing,
        # but in a resilient system we might log and retry.
        sys.exit(1)
        
    print("Agent execution completed.")
    set_last_run()

if __name__ == "__main__":
    main()
