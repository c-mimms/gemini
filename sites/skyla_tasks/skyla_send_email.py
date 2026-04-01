#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser(description="Send beautifully formatted HTML email to Skyla")
    parser.add_argument("--subject", required=True, help="Email subject")
    parser.add_argument("--body", help="HTML content to send")
    parser.add_argument("--file", help="File containing HTML content")
    args = parser.parse_args()

    agent_tools_send = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../agent_tools/send_email.py")
    
    cmd = [
        sys.executable,
        agent_tools_send,
        "--to", "skylaackley@gmail.com",
        "--subject", args.subject,
        "--html"
    ]
    
    if args.file:
        cmd.extend(["--file", args.file])
    elif args.body:
        cmd.extend(["--body", args.body])
    elif not sys.stdin.isatty():
        body = sys.stdin.read()
        cmd.extend(["--body", body])
    else:
        print("Error: No body provided. Provide --body, --file, or pipe via stdin.", file=sys.stderr)
        sys.exit(1)

    print(f"Sending HTML email to Skyla...", flush=True)
    res = subprocess.run(cmd)
    if res.returncode != 0:
        print("Failed to send email to Skyla.", file=sys.stderr)
    sys.exit(res.returncode)

if __name__ == "__main__":
    main()
