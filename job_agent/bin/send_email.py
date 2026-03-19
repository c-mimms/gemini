#!/usr/bin/env python3
import os
import sys
import argparse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

import mimetypes
from email.mime.base import MIMEBase
from email import encoders

def main():
    parser = argparse.ArgumentParser(description="Send an email using SMTP settings from .env")
    parser.add_argument("--to", required=True, help="Recipient email address")
    parser.add_argument("--subject", required=True, help="Email subject")
    parser.add_argument("--body", help="Email body (plain text). If not provided, read from stdin or --file.")
    parser.add_argument("--file", help="Path to a file containing the email body (overrides --body and stdin)")
    parser.add_argument("--html", action="store_true", help="Send body as HTML")
    parser.add_argument("--attach", action="append", help="Path to a file to attach. Can be used multiple times.")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be sent without actually sending")
    parser.add_argument("--env-file", help="Path to .env file (default: .env in current or parent dir)")

    args = parser.parse_args()

    # Load environment variables
    env_path = args.env_file
    if not env_path:
        # Try to find .env in discord_bot root if we are in bin/
        possible_env = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
        if os.path.exists(possible_env):
            env_path = possible_env
    
    load_dotenv(env_path)

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")

    if not all([smtp_host, smtp_port, smtp_user, smtp_pass]):
        print("Error: Missing SMTP configuration in environment.", file=sys.stderr)
        print(f"Checked: SMTP_HOST={smtp_host}, SMTP_PORT={smtp_port}, SMTP_USER={smtp_user}, SMTP_PASS={'***' if smtp_pass else None}", file=sys.stderr)
        sys.exit(1)

    # Get body
    body = None
    if args.file:
        if not os.path.exists(args.file):
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        with open(args.file, "r") as f:
            body = f.read()
    elif args.body:
        body = args.body
    elif not sys.stdin.isatty():
        body = sys.stdin.read()
    
    if body is None:
        # If there's an attachment, the body can be optional
        if not args.attach:
            print("Error: No body or attachment provided (use --body, --file, pipe to stdin, or --attach).", file=sys.stderr)
            sys.exit(1)
        body = "" # Ensure body is not None

    # Construct email
    msg = MIMEMultipart()
    msg["Subject"] = args.subject
    msg["From"] = smtp_user
    msg["To"] = args.to

    # Attach the body part
    msg.attach(MIMEText(body, "html" if args.html else "plain"))

    # Attach files
    if args.attach:
        for file_path in args.attach:
            if not os.path.exists(file_path):
                print(f"Error: Attachment file not found: {file_path}", file=sys.stderr)
                continue
            
            ctype, encoding = mimetypes.guess_type(file_path)
            if ctype is None or encoding is not None:
                ctype = "application/octet-stream"
            
            maintype, subtype = ctype.split("/", 1)
            
            with open(file_path, "rb") as fp:
                part = MIMEBase(maintype, subtype)
                part.set_payload(fp.read())
            
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", "attachment", filename=os.path.basename(file_path))
            msg.attach(part)


    if args.dry_run:
        print("--- DRY RUN ---")
        print(f"To: {args.to}")
        print(f"Subject: {args.subject}")
        print(f"From: {smtp_user}")
        print(f"Format: {'HTML' if args.html else 'Plain Text'}")
        if args.attach:
            print(f"Attachments: {', '.join(args.attach)}")
        print("Body:")
        print(body)
        print("----------------")
        return

    try:
        print(f"Connecting to {smtp_host}:{smtp_port}...")
        with smtplib.SMTP(smtp_host, int(smtp_port)) as server:
            server.set_debuglevel(1 if os.getenv("DEBUG_SMTP") else 0)
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
            print(f"Successfully sent email to {args.to}")
    except Exception as e:
        print(f"Error sending email: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
