"""Validazione dei dati inseriti dall'utente."""

from __future__ import annotations

from email.utils import parseaddr
import re


EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def validate_registration(full_name: str, email: str, reason: str) -> list[str]:
    errors = []
    normalized_name = " ".join(full_name.split())
    normalized_email = email.strip()
    if len(normalized_name) < 3 or len(normalized_name) > 120:
        errors.append("Inserisci un nome e cognome validi.")
    parsed = parseaddr(normalized_email)[1]
    if parsed != normalized_email or not EMAIL_PATTERN.fullmatch(normalized_email) or len(normalized_email) > 254:
        errors.append("Inserisci un indirizzo email valido.")
    if not reason.strip() or len(reason.strip()) > 300:
        errors.append("Inserisci una motivazione (massimo 300 caratteri).")
    return errors


def validate_reason(reason: str) -> str | None:
    normalized = reason.strip()
    if not normalized:
        return "Inserisci una motivazione per continuare."
    if len(normalized) > 300:
        return "La motivazione non può superare 300 caratteri."
    return None
