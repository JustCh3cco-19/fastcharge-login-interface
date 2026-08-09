from datetime import datetime, timedelta, timezone
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from fastcharge.database import Database, DuplicateAccessError
from fastcharge.services.notifier import process_log_batch


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = TemporaryDirectory()
        self.database = Database(Path(self.temporary_directory.name) / "test.db")
        self.user = self.database.register_user("Mario Rossi", "Mario@Example.com")

    def tearDown(self):
        self.temporary_directory.cleanup()

    def test_registration_normalizes_and_reuses_email(self):
        updated = self.database.register_user("Mario B. Rossi", "mario@example.com")
        self.assertEqual(updated.id, self.user.id)
        self.assertEqual(updated.email, "mario@example.com")
        self.assertEqual(self.database.get_user(updated.id).full_name, "Mario B. Rossi")

    def test_duplicate_access_is_rejected_inside_window(self):
        self.database.record_access(self.user.id, "Riunione")
        with self.assertRaises(DuplicateAccessError):
            self.database.record_access(self.user.id, "Seconda scansione")

    @patch("fastcharge.services.notifier.invia_email", return_value=True)
    def test_success_marks_only_sent_rows(self, send_email):
        self.database.record_access(self.user.id, "Riunione")
        self.assertTrue(process_log_batch(self.database))
        self.assertEqual(self.database.pending_count(), 0)
        self.assertIn("Mario Rossi", send_email.call_args.args[0])

    @patch("fastcharge.services.notifier.invia_email", return_value=False)
    def test_failure_keeps_rows_pending(self, _send_email):
        self.database.record_access(self.user.id, "Riunione")
        self.assertFalse(process_log_batch(self.database))
        self.assertEqual(self.database.pending_count(), 1)

    def test_retention_deletes_only_old_notified_rows(self):
        access_id = self.database.record_access(self.user.id, "Riunione")
        self.database.mark_notified([access_id])
        cutoff = datetime.now(timezone.utc) + timedelta(seconds=1)
        self.assertEqual(self.database.purge_notified_before(cutoff), 1)

    def test_inactive_user_retention_invalidates_old_user(self):
        with self.database.connect() as connection:
            connection.execute(
                "UPDATE users SET created_at = ? WHERE id = ?",
                ((datetime.now(timezone.utc) - timedelta(days=400)).isoformat(), self.user.id),
            )
        cutoff = datetime.now(timezone.utc) - timedelta(days=365)
        self.assertEqual(self.database.purge_inactive_users_before(cutoff), 1)
        self.assertIsNone(self.database.get_user(self.user.id))

    def test_legacy_log_is_migrated_and_archived(self):
        legacy = Path(self.temporary_directory.name) / "accessi.txt"
        legacy.write_text(
            "Luigi Verdi\nluigi@example.com\nMotivazione Visita: Consegna\n",
            encoding="utf-8",
        )
        self.assertEqual(self.database.migrate_legacy_log(legacy), 1)
        self.assertFalse(legacy.exists())
        self.assertTrue(legacy.with_suffix(".txt.migrated").exists())
        self.assertEqual(self.database.pending_count(), 1)

    def test_existing_database_schema_is_upgraded(self):
        old_path = Path(self.temporary_directory.name) / "old.db"
        connection = sqlite3.connect(old_path)
        connection.execute(
            """
            CREATE TABLE users (
                id TEXT PRIMARY KEY, full_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE, created_at TEXT NOT NULL
            )
            """
        )
        connection.commit()
        connection.close()

        upgraded = Database(old_path)

        with upgraded.connect() as connection:
            columns = {row["name"] for row in connection.execute("PRAGMA table_info(users)")}
        self.assertIn("last_access_at", columns)


if __name__ == "__main__":
    unittest.main()
