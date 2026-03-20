import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import io
import json

# Add the parent directory to sys.path to import from bin/
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from read_email import main

class TestReadEmail(unittest.TestCase):
    @patch("read_email.imaplib.IMAP4_SSL")
    @patch.dict(os.environ, {
        "IMAP_HOST": "imap.test.com",
        "IMAP_PORT": "993",
        "SMTP_USER": "test@test.com",
        "SMTP_PASS": "password"
    })
    def test_read_email_json(self, mock_imap):
        # Setup mock IMAP
        mock_mail = mock_imap.return_value
        mock_mail.search.return_value = ("OK", [b"1 2"])
        
        # Mock fetch response for email ID 2
        # RFC822 format simplified
        email_content = b"""From: sender@test.com
Subject: Test Subject
Date: Mon, 1 Jan 2026 10:00:00 +0000
Content-Type: text/plain; charset="utf-8"

Test Body Content
"""
        mock_mail.fetch.return_value = ("OK", [(None, email_content)])

        test_args = [
            "read_email.py",
            "--limit", "1",
            "--json"
        ]
        
        with patch.object(sys, "argv", test_args):
            with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
                main()
        
        # Verify IMAP called
        mock_imap.assert_called_with("imap.test.com", 993)
        mock_mail.login.assert_called_with("test@test.com", "password")
        
        # Verify JSON output
        output = json.loads(mock_stdout.getvalue())
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0]["subject"], "Test Subject")
        self.assertEqual(output[0]["body"], "Test Body Content")

    @patch("read_email.imaplib.IMAP4_SSL")
    @patch.dict(os.environ, {
        "IMAP_HOST": "imap.test.com",
        "IMAP_PORT": "993",
        "SMTP_USER": "test@test.com",
        "SMTP_PASS": "password"
    })
    def test_read_email_plain(self, mock_imap):
        # Setup mock IMAP
        mock_mail = mock_imap.return_value
        mock_mail.search.return_value = ("OK", [b"1"])
        
        email_content = b"""From: sender@test.com
Subject: Test Subject
Date: Mon, 1 Jan 2026 10:00:00 +0000

Test Body Content
"""
        mock_mail.fetch.return_value = ("OK", [(None, email_content)])

        test_args = [
            "read_email.py",
            "--limit", "1"
        ]
        
        with patch.object(sys, "argv", test_args):
            with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
                main()
        
        output = mock_stdout.getvalue()
        self.assertIn("Subject: Test Subject", output)
        self.assertIn("Test Body Content", output)

if __name__ == "__main__":
    unittest.main()
