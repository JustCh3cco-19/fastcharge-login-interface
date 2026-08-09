"""Persistenza SQLite per utenti, accessi e stato delle notifiche."""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import re
import sqlite3
import threading
from typing import Iterator
from uuid import uuid4

from fastcharge.paths import database_path, log_file_path


_MIGRATION_LOCK = threading.Lock()


@dataclass(frozen=True)
class User:
    id: str
    full_name: str
    email: str


@dataclass(frozen=True)
class Access:
    id: int
    user_id: str
    full_name: str
    email: str
    reason: str
    occurred_at: str


class DuplicateAccessError(ValueError):
    pass


class Database:
    def __init__(self, path: Path | None = None):
        uses_default_path = path is None
        self.path = path or database_path()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()
        if uses_default_path:
            with _MIGRATION_LOCK:
                self.migrate_legacy_log()

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.path, timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA journal_mode = WAL")
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def _initialize(self) -> None:
        with self.connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    full_name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                    created_at TEXT NOT NULL,
                    last_access_at TEXT
                );
                CREATE TABLE IF NOT EXISTS accesses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL REFERENCES users(id),
                    reason TEXT NOT NULL,
                    occurred_at TEXT NOT NULL,
                    notified_at TEXT
                );
                CREATE INDEX IF NOT EXISTS idx_accesses_notification
                    ON accesses(notified_at, id);
                CREATE INDEX IF NOT EXISTS idx_accesses_user_time
                    ON accesses(user_id, occurred_at);
                CREATE TABLE IF NOT EXISTS metadata (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );
                """
            )
            columns = {
                row["name"] for row in connection.execute("PRAGMA table_info(users)").fetchall()
            }
            if "last_access_at" not in columns:
                connection.execute("ALTER TABLE users ADD COLUMN last_access_at TEXT")

    def register_user(self, full_name: str, email: str) -> User:
        normalized_email = email.strip().lower()
        normalized_name = " ".join(full_name.split())
        with self.connect() as connection:
            existing = connection.execute(
                "SELECT id FROM users WHERE email = ?", (normalized_email,)
            ).fetchone()
            if existing:
                connection.execute(
                    "UPDATE users SET full_name = ? WHERE id = ?",
                    (normalized_name, existing["id"]),
                )
                user_id = existing["id"]
            else:
                user_id = str(uuid4())
                connection.execute(
                    "INSERT INTO users(id, full_name, email, created_at) VALUES (?, ?, ?, ?)",
                    (user_id, normalized_name, normalized_email, _utc_now()),
                )
        return User(user_id, normalized_name, normalized_email)

    def get_user(self, user_id: str) -> User | None:
        with self.connect() as connection:
            row = connection.execute(
                "SELECT id, full_name, email FROM users WHERE id = ?", (user_id,)
            ).fetchone()
        return User(**dict(row)) if row else None

    def record_access(
        self, user_id: str, reason: str, duplicate_window_seconds: int = 60
    ) -> int:
        now = datetime.now(timezone.utc)
        with self.connect() as connection:
            last = connection.execute(
                "SELECT occurred_at FROM accesses WHERE user_id = ? ORDER BY id DESC LIMIT 1",
                (user_id,),
            ).fetchone()
            if last and duplicate_window_seconds > 0:
                previous = datetime.fromisoformat(last["occurred_at"])
                if (now - previous).total_seconds() < duplicate_window_seconds:
                    raise DuplicateAccessError("Accesso già registrato da pochi secondi.")
            cursor = connection.execute(
                "INSERT INTO accesses(user_id, reason, occurred_at) VALUES (?, ?, ?)",
                (user_id, reason.strip(), now.isoformat()),
            )
            connection.execute(
                "UPDATE users SET last_access_at = ? WHERE id = ?", (now.isoformat(), user_id)
            )
            return int(cursor.lastrowid)

    def pending_accesses(self, limit: int = 500) -> list[Access]:
        with self.connect() as connection:
            rows = connection.execute(
                """
                SELECT a.id, a.user_id, u.full_name, u.email, a.reason, a.occurred_at
                FROM accesses a JOIN users u ON u.id = a.user_id
                WHERE a.notified_at IS NULL ORDER BY a.id LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [Access(**dict(row)) for row in rows]

    def mark_notified(self, access_ids: list[int]) -> None:
        if not access_ids:
            return
        placeholders = ",".join("?" for _ in access_ids)
        with self.connect() as connection:
            connection.execute(
                f"UPDATE accesses SET notified_at = ? WHERE id IN ({placeholders})",
                (_utc_now(), *access_ids),
            )

    def pending_count(self) -> int:
        with self.connect() as connection:
            row = connection.execute(
                "SELECT COUNT(*) AS count FROM accesses WHERE notified_at IS NULL"
            ).fetchone()
        return int(row["count"])

    def purge_notified_before(self, cutoff: datetime) -> int:
        with self.connect() as connection:
            cursor = connection.execute(
                "DELETE FROM accesses WHERE notified_at IS NOT NULL AND occurred_at < ?",
                (cutoff.astimezone(timezone.utc).isoformat(),),
            )
            return cursor.rowcount

    def purge_inactive_users_before(self, cutoff: datetime) -> int:
        """Elimina utenti senza accessi recenti, invalidandone intenzionalmente il QR."""
        cutoff_value = cutoff.astimezone(timezone.utc).isoformat()
        with self.connect() as connection:
            cursor = connection.execute(
                """
                DELETE FROM users
                WHERE COALESCE(last_access_at, created_at) < ?
                  AND NOT EXISTS (SELECT 1 FROM accesses WHERE accesses.user_id = users.id)
                """,
                (cutoff_value,),
            )
            return cursor.rowcount

    def migrate_legacy_log(self, path: Path | None = None) -> int:
        """Importa, una sola volta, i record riconoscibili del vecchio file TXT."""
        legacy = path or log_file_path()
        if not legacy.exists() or legacy.stat().st_size == 0:
            return 0
        imported = 0
        lines = [line.strip() for line in legacy.read_text(encoding="utf-8").splitlines()]
        with self.connect() as connection:
            done = connection.execute(
                "SELECT 1 FROM metadata WHERE key = 'legacy_log_migrated'"
            ).fetchone()
            if done:
                return 0
            for index, line in enumerate(lines):
                if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", line):
                    continue
                full_name = lines[index - 1] if index else "Utente importato"
                reason_line = lines[index + 1] if index + 1 < len(lines) else ""
                reason = reason_line.split(":", 1)[-1].strip() or "Importato dal log precedente"
                existing = connection.execute(
                    "SELECT id FROM users WHERE email = ?", (line.lower(),)
                ).fetchone()
                user_id = existing["id"] if existing else str(uuid4())
                if not existing:
                    connection.execute(
                        "INSERT INTO users(id, full_name, email, created_at) VALUES (?, ?, ?, ?)",
                        (user_id, full_name, line.lower(), _utc_now()),
                    )
                connection.execute(
                    "INSERT INTO accesses(user_id, reason, occurred_at) VALUES (?, ?, ?)",
                    (user_id, reason, _utc_now()),
                )
                connection.execute(
                    "UPDATE users SET last_access_at = ? WHERE id = ?", (_utc_now(), user_id)
                )
                imported += 1
            connection.execute(
                "INSERT INTO metadata(key, value) VALUES ('legacy_log_migrated', ?)",
                (_utc_now(),),
            )
        archive = legacy.with_suffix(legacy.suffix + ".migrated")
        legacy.replace(archive)
        return imported


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()
