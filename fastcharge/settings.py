"""Caricamento e controllo della configurazione applicativa."""

from __future__ import annotations

import os

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*_args, **_kwargs):
        return False

from fastcharge.paths import dotenv_path


def load_settings() -> None:
    load_dotenv(dotenv_path=dotenv_path())


def email_configuration_status() -> tuple[bool, str]:
    required = {
        "mittente": os.getenv("SENDER_EMAIL"),
        "password": os.getenv("SENDER_PASSWORD") or os.getenv("EMAIL_APP_PASSWORD"),
        "destinatario": os.getenv("RECEIVER_EMAIL"),
    }
    missing = [name for name, value in required.items() if not value]
    if missing:
        return False, f"Email non configurata: manca {', '.join(missing)}"
    return True, "Notifiche email configurate"
