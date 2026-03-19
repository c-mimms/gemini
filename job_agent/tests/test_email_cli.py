import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import io

# Add the parent directory to sys.path to import from bin/
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from bin.send_email import main

class TestEmailCLI(unittest.TestCase):
    @patch("bin.send_email.smtplib.SMTP")
    @patch("bin.send_email.load_dotenv")
    @patch.dict(os.environ, {
        "SMTP_HOST": "smtp.test.com",
        "SMTP_PORT": "587",
        "SMTP_USER": "test@test.com",
        "SMTP_PASS": "password"
    })
    def test_send_email_success(self, mock_dotenv, mock_smtp):
        # Mock values
        mock_server = mock_smtp.return_value.__enter__.return_value
        
        # Simulate CLI arguments
        test_args = [
            "send_email.py",
            "--to", "recipient@test.com",
            "--subject", "Test Subject",
            "--body", "Test Body"
        ]
        
        with patch.object(sys, "argv", test_args):
            with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
                main()
                
        # Verify SMTP interactions
        mock_smtp.assert_called_with("smtp.test.com", 587)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_with("test@test.com", "password")
        mock_server.send_message.assert_called_once()
        
        # Check output
        self.assertIn("Successfully sent email to recipient@test.com", mock_stdout.getvalue())

    @patch("bin.send_email.smtplib.SMTP")
    @patch.dict(os.environ, {
        "SMTP_HOST": "smtp.test.com",
        "SMTP_PORT": "587",
        "SMTP_USER": "test@test.com",
        "SMTP_PASS": "password"
    })
    def test_dry_run(self, mock_smtp):
        test_args = [
            "send_email.py",
            "--to", "recipient@test.com",
            "--subject", "Test Subject",
            "--body", "Test Body",
            "--dry-run"
        ]
        
        with patch.object(sys, "argv", test_args):
            with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
                main()
        
        # Verify SMTP was NOT called
        mock_smtp.assert_not_called()
        
        # Check output
        output = mock_stdout.getvalue()
        self.assertIn("--- DRY RUN ---", output)
        self.assertIn("To: recipient@test.com", output)
        self.assertIn("Subject: Test Subject", output)

    @patch("bin.send_email.sys.stdin", new=io.StringIO("Piped Body Content"))
    @patch("bin.send_email.smtplib.SMTP")
    @patch.dict(os.environ, {
        "SMTP_HOST": "smtp.test.com",
        "SMTP_PORT": "587",
        "SMTP_USER": "test@test.com",
        "SMTP_PASS": "password"
    })
    def test_piped_input(self, mock_smtp):
        # We need to mock isatty to return False to trigger stdin reading
        with patch("bin.send_email.sys.stdin.isatty", return_value=False):
            test_args = [
                "send_email.py",
                "--to", "recipient@test.com",
                "--subject", "Test Subject",
                "--dry-run"
            ]
            
            with patch.object(sys, "argv", test_args):
                with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
                    main()
            
            self.assertIn("Piped Body Content", mock_stdout.getvalue())

    @patch("bin.send_email.smtplib.SMTP")
    @patch.dict(os.environ, {
        "SMTP_HOST": "smtp.test.com",
        "SMTP_PORT": "587",
        "SMTP_USER": "test@test.com",
        "SMTP_PASS": "password"
    })
    def test_send_email_from_file(self, mock_smtp):
        # Create a temp file
        import tempfile
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("File Content")
            temp_path = f.name
        
        try:
            test_args = [
                "send_email.py",
                "--to", "recipient@test.com",
                "--subject", "Test Subject",
                "--file", temp_path,
                "--dry-run"
            ]
            
            with patch.object(sys, "argv", test_args):
                with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
                    main()
            
            self.assertIn("File Content", mock_stdout.getvalue())
        finally:
            os.remove(temp_path)

if __name__ == "__main__":
    unittest.main()
