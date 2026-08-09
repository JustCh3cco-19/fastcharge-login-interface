from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from fastcharge.database import Database
from fastcharge.security import create_token, verify_token
from fastcharge.services.notifier import process_log_batch


class IntegrationFlowTests(unittest.TestCase):
    @patch("fastcharge.services.notifier.invia_email", return_value=True)
    def test_registration_qr_scan_and_notification(self, send_email):
        with TemporaryDirectory() as directory:
            database = Database(Path(directory) / "fastcharge.db")
            user = database.register_user("Ada Lovelace", "ada@example.com")
            token = create_token(user.id, b"integration-secret")

            scanned_user_id = verify_token(token, b"integration-secret")
            scanned_user = database.get_user(scanned_user_id)
            database.record_access(scanned_user.id, "Visita tecnica")

            self.assertTrue(process_log_batch(database))
            message = send_email.call_args.args[0]
            self.assertIn("Ada Lovelace", message)
            self.assertIn("Visita tecnica", message)
            self.assertEqual(database.pending_count(), 0)


if __name__ == "__main__":
    unittest.main()
