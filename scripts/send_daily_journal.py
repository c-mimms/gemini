#!/usr/bin/env python3
import os
import sys
import subprocess
from datetime import datetime

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    send_email_script = os.path.join(root_dir, "agent_tools", "send_email.py")
    
    if not os.path.exists(send_email_script):
        print(f"Error: send_email.py not found at {send_email_script}", file=sys.stderr)
        sys.exit(1)
        
    date_str = datetime.now().strftime("%A, %B %d, %Y")
    subject = f"Daily Journal - {date_str}"
    
    html_body = f"""
    <h2>Good evening!</h2>
    <p>It's time for your daily journal check-in for {date_str}. Take a few minutes to reflect on the day.</p>
    
    <h3>1. The Vibe</h3>
    <p><i>If you had to describe today's energy or vibe in one word or a short phrase, what would it be?</i></p>
    
    <h3>2. Highs &amp; Lows</h3>
    <ul>
        <li><b>High:</b> What was the best part of your day?</li>
        <li><b>Low:</b> Was there anything frustrating, challenging, or draining?</li>
    </ul>
    
    <h3>3. Memorable Events</h3>
    <p><i>Did anything unusual, exciting, or significant happen today? (Big or small!)</i></p>
    
    <h3>4. Gratitude</h3>
    <p><i>What is one thing you are grateful for right now?</i></p>
    
    <hr>
    <p><small>Just reply directly to this email to save your journal entry.</small></p>
    """
    
    recipients = ["christek13@gmail.com", "nickpmimms@gmail.com"]
    
    for recipient in recipients:
        cmd = [
            sys.executable,
            send_email_script,
            "--to", recipient,
            "--subject", subject,
            "--body", html_body,
            "--html"
        ]
        print(f"Sending daily journal prompt to {recipient}...")
        try:
            subprocess.run(cmd, check=True)
            print(f"Successfully sent to {recipient}.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to send email to {recipient}: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
