import os
import unittest
from unittest.mock import patch

from fastcharge.settings import email_configuration_status


class SettingsTests(unittest.TestCase):
    @patch.dict(os.environ, {}, clear=True)
    def test_missing_email_configuration(self):
        configured, message = email_configuration_status()
        self.assertFalse(configured)
        self.assertIn("mittente", message)

    @patch.dict(
        os.environ,
        {
            "SENDER_EMAIL": "sender@example.com",
            "SENDER_PASSWORD": "secret",
            "RECEIVER_EMAIL": "receiver@example.com",
        },
        clear=True,
    )
    def test_complete_email_configuration(self):
        self.assertEqual(email_configuration_status(), (True, "Notifiche email configurate"))


if __name__ == "__main__":
    unittest.main()
