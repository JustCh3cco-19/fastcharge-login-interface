"""Percorsi condivisi per risorse, configurazione e dati scrivibili."""

from __future__ import annotations

import os
from pathlib import Path
import sys


PROJECT_DIR = Path(__file__).resolve().parent.parent


def resource_path(relative_path: str | Path) -> Path:
    """Restituisce una risorsa inclusa nel progetto o nel bundle PyInstaller."""
    base = Path(getattr(sys, "_MEIPASS", PROJECT_DIR))
    return base / relative_path


def data_dir() -> Path:
    """Directory persistente e scrivibile, mai interna al bundle temporaneo."""
    configured = os.getenv("FASTCHARGE_DATA_DIR")
    if configured:
        return Path(configured).expanduser().resolve()
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent / "data"
    return PROJECT_DIR / "resources"


def log_file_path() -> Path:
    return data_dir() / "log" / "accessi.txt"


def database_path() -> Path:
    return data_dir() / "fastcharge.db"


def secret_key_path() -> Path:
    return data_dir() / "qr-signing.key"


def qr_code_dir() -> Path:
    return data_dir() / "qr_codes"


def dotenv_path() -> Path:
    configured = os.getenv("FASTCHARGE_CONFIG_FILE")
    if configured:
        return Path(configured).expanduser().resolve()
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent / ".env"
    return PROJECT_DIR / ".env"
