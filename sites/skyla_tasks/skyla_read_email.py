#!/usr/bin/env python3
import os
import sys
import argparse
import imaplib
import email
from email.header import decode_header
from email.utils import parsedate_to_datetime
from datetime import datetime
import json
from dotenv import load_dotenv

def decode_mime_words(s):
    if not s:
        return ""
    parts = decode_header(s)
    decoded_parts = []
    for content, charset in parts:
        if isinstance(content, bytes):
            decoded_parts.append(content.decode(charset or "utf-8", errors="replace"))
        else:
            if isinstance(content, str):
                decoded_parts.append(content)
    return "".join(decoded_parts)

def main():
    parser = argparse.ArgumentParser(description="Fetch recent emails from Skyla")
    parser.add_argument("--since", help="Fetch emails sent after this ISO format timestamp (e.g., 2026-03-31T20:00:00)")
    parser.add_argument("--limit", type=int, default=10, help="Max emails to return")
    args = parser.parse_args()

    # Determine filter time
    since_dt = None
    if args.since:
        try:
            since_dt = datetime.fromisoformat(args.since.replace("Z", "+00:00"))
            if since_dt.tzinfo is None:
                # Assume local if UTC offset not provided, or fallback to UTC
                from datetime import timezone
                since_dt = since_dt.replace(tzinfo=timezone.utc)
        except ValueError:
            print(f"Error parsing --since date: {args.since}", file=sys.stderr)
            sys.exit(1)

    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../agent_tools/.env"))
    
    imap_host = os.getenv("IMAP_HOST")
    imap_port = os.getenv("IMAP_PORT")
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")

    if not all([imap_host, imap_port, smtp_user, smtp_pass]):
        print("Error: Missing IMAP/SMTP config. Check agent_tools/.env", file=sys.stderr)
        sys.exit(1)

    try:
        mail = imaplib.IMAP4_SSL(imap_host, int(imap_port))
        mail.login(smtp_user, smtp_pass)
        mail.select("inbox")

        # Create search query: from Skyla
        search_crit = '(FROM "skylaackley@gmail.com")'
        if since_dt:
            # IMAP SINCE is date-only (e.g., 31-Mar-2026)
            imap_date = since_dt.strftime("%d-%b-%Y")
            search_crit = f'(FROM "skylaackley@gmail.com" SINCE "{imap_date}")'

        status, messages = mail.search(None, search_crit)
        if status != "OK":
            mail.logout()
            print("[]")
            return

        email_ids = messages[0].split()
        if not email_ids:
            mail.logout()
            print("[]")
            return
            
        latest_ids = email_ids[-args.limit:]
        latest_ids.reverse()

        results = []
        for e_id in latest_ids:
            res, msg_data = mail.fetch(e_id, "(RFC822)")
            if res != "OK": continue

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    # Parse Date and filter precisely
                    msg_date_str = msg.get("Date")
                    if msg_date_str and since_dt:
                        msg_dt = parsedate_to_datetime(msg_date_str)
                        if msg_dt.tzinfo is None:
                            from datetime import timezone
                            msg_dt = msg_dt.replace(tzinfo=timezone.utc)
                        if msg_dt <= since_dt:
                            continue # Skip emails exactly on or before the since_dt threshold
                    
                    subject = decode_mime_words(msg["Subject"])
                    from_ = decode_mime_words(msg["From"])

                    body = ""
                    html_body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            ctype = part.get_content_type()
                            cdisp = str(part.get("Content-Disposition"))
                            if "attachment" in cdisp: continue
                            
                            try:
                                pbody = part.get_payload(decode=True).decode(errors="replace")
                            except Exception:
                                continue
                            
                            if ctype == "text/plain":
                                body += pbody
                            elif ctype == "text/html":
                                html_body += pbody
                    else:
                        body = msg.get_payload(decode=True).decode(errors="replace")

                    results.append({
                        "id": e_id.decode(),
                        "from": from_,
                        "subject": subject,
                        "date": msg_date_str,
                        "body": body.strip(),
                        "html_body": html_body.strip()
                    })

        mail.logout()
        # Return exact chronological order inside the list
        results.reverse()
        print(json.dumps(results, indent=2))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
