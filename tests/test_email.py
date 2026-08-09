import os
import smtplib
import unittest
from unittest.mock import MagicMock, patch

from fastcharge.services.notifier import invia_email


SMTP_ENV = {
    "SENDER_EMAIL": "sender@example.com",
    "SENDER_PASSWORD": "secret",
    "RECEIVER_EMAIL": "one@example.com,two@example.com",
    "SMTP_HOST": "smtp.example.com",
    "SMTP_PORT": "2525",
    "SMTP_USE_TLS": "true",
}


class EmailTests(unittest.TestCase):
    @patch.dict(os.environ, SMTP_ENV, clear=True)
    @patch("fastcharge.services.notifier.smtplib.SMTP")
    def test_smtp_settings_and_success_result(self, smtp_class):
        server = MagicMock()
        smtp_class.return_value = server

        self.assertTrue(invia_email("dati"))

        smtp_class.assert_called_once_with("smtp.example.com", 2525, timeout=15.0)
        server.starttls.assert_called_once_with()
        server.login.assert_called_once_with("sender@example.com", "secret")
        server.quit.assert_called_once_with()

    @patch.dict(os.environ, SMTP_ENV, clear=True)
    @patch(
        "fastcharge.services.notifier.smtplib.SMTP",
        side_effect=smtplib.SMTPException("offline"),
    )
    def test_connection_failure_returns_false(self, _smtp_class):
        self.assertFalse(invia_email("dati"))

    @patch.dict(os.environ, {}, clear=True)
    def test_missing_credentials_are_rejected(self):
        with self.assertRaises(EnvironmentError):
            invia_email("dati")


if __name__ == "__main__":
    unittest.main()
