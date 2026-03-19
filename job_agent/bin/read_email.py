#!/usr/bin/env python3
import os
import sys
import argparse
import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv
import json

def decode_mime_words(s):
    if not s:
        return ""
    parts = decode_header(s)
    decoded_parts = []
    for content, charset in parts:
        if isinstance(content, bytes):
            decoded_parts.append(content.decode(charset or "utf-8", errors="replace"))
        else:
            decoded_parts.append(content)
    return "".join(decoded_parts)

def main():
    parser = argparse.ArgumentParser(description="Read emails using IMAP settings from .env")
    parser.add_argument("--limit", type=int, default=5, help="Number of emails to fetch (default: 5)")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    parser.add_argument("--id", type=str, help="Fetch a specific email by its ID")
    parser.add_argument("--save-attachments", type=str, help="Save attachments from a specific email to the given directory")
    parser.add_argument("--env-file", help="Path to .env file")

    args = parser.parse_args()

    if args.save_attachments and not args.id:
        print("Error: --save-attachments requires --id to be specified.", file=sys.stderr)
        sys.exit(1)

    # Load environment variables
    env_path = args.env_file
    if not env_path:
        possible_env = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
        if os.path.exists(possible_env):
            env_path = possible_env
    
    load_dotenv(env_path)

    imap_host = os.getenv("IMAP_HOST")
    imap_port = os.getenv("IMAP_PORT")
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")

    if not all([imap_host, imap_port, smtp_user, smtp_pass]):
        print("Error: Missing IMAP/SMTP configuration in environment.", file=sys.stderr)
        sys.exit(1)

    try:
        # Connect to IMAP
        mail = imaplib.IMAP4_SSL(imap_host, int(imap_port))
        mail.login(smtp_user, smtp_pass)
        mail.select("inbox")

        # If ID is provided, handle that specific email
        if args.id:
            e_id = args.id.encode()
            res, msg_data = mail.fetch(e_id, "(RFC822)")
            if res != "OK":
                print(f"Error fetching email with ID {args.id}: {res}", file=sys.stderr)
                sys.exit(1)
            
            msg = email.message_from_bytes(msg_data[0][1])

            if args.save_attachments:
                if not os.path.isdir(args.save_attachments):
                    os.makedirs(args.save_attachments)

                saved_files = []
                for part in msg.walk():
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        continue
                    
                    filename = part.get_filename()
                    if filename:
                        filename = decode_mime_words(filename)
                        filepath = os.path.join(args.save_attachments, filename)
                        with open(filepath, 'wb') as f:
                            f.write(part.get_payload(decode=True))
                        saved_files.append(os.path.abspath(filepath))
                
                # Print the paths of saved files, one per line
                for f_path in saved_files:
                    print(f_path)
                
                mail.logout()
                return # Exit after saving attachments

            # If not saving attachments, just show the email content (similar to original logic)
            subject = decode_mime_words(msg["Subject"])
            from_ = decode_mime_words(msg["From"])
            date = msg["Date"]
            
            body = ""
            html_body = ""

            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    try:
                        part_body = part.get_payload(decode=True).decode(errors="replace")
                    except Exception:
                        continue
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        body += part_body
                    elif content_type == "text/html" and "attachment" not in content_disposition:
                        html_body += part_body
            else:
                body = msg.get_payload(decode=True).decode(errors="replace")

            email_data = {
                "id": args.id,
                "from": from_,
                "subject": subject,
                "date": date,
                "body": body.strip(),
                "html_body": html_body.strip()
            }
            if args.json:
                print(json.dumps(email_data, indent=2))
            else:
                print(f"ID: {email_data['id']}")
                print(f"From: {email_data['from']}")
                print(f"Subject: {email_data['subject']}")
                print(f"Date: {email_data['date']}")
                print("-" * 20)
                print(email_data["body"])
            
            mail.logout()
            return

        # Original logic to list multiple emails
        search_crit = "ALL"
        status, messages = mail.search(None, search_crit)
        
        if status != "OK":
            print(f"Error searching emails: {status}", file=sys.stderr)
            sys.exit(1)

        email_ids = messages[0].split()
        latest_email_ids = email_ids[-args.limit:]
        latest_email_ids.reverse() # Most recent first

        emails = []

        for e_id in latest_email_ids:
            res, msg_data = mail.fetch(e_id, "(RFC822)")
            if res != "OK":
                continue
            
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = decode_mime_words(msg["Subject"])
                    from_ = decode_mime_words(msg["From"])
                    date = msg["Date"]
                    
                    body = ""
                    html_body = ""

                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))

                            try:
                                part_body = part.get_payload(decode=True).decode(errors="replace")
                            except Exception:
                                continue

                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                body += part_body
                            elif content_type == "text/html" and "attachment" not in content_disposition:
                                html_body += part_body
                    else:
                        body = msg.get_payload(decode=True).decode(errors="replace")

                    emails.append({
                        "id": e_id.decode(),
                        "from": from_,
                        "subject": subject,
                        "date": date,
                        "body": body.strip(),
                        "html_body": html_body.strip()
                    })

        if args.json:
            print(json.dumps(emails, indent=2))
        else:
            if not emails:
                print("No emails found.")
            for e in emails:
                print(f"ID: {e['id']}")
                print(f"From: {e['from']}")
                print(f"Subject: {e['subject']}")
                print(f"Date: {e['date']}")
                print("-" * 20)
                print(e["body"][:500] + ("..." if len(e["body"]) > 500 else ""))
                print("=" * 40)

        mail.logout()

    except Exception as e:
        print(f"Error reading emails: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
