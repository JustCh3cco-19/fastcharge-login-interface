"""
Module Name: monitoraccessi
Description: invia periodicamente gli accessi SQLite non ancora notificati.
Author: Francesco Zompanti
"""
from datetime import date, datetime, timedelta, timezone
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import time
from fastcharge.database import Access, Database
from fastcharge.settings import load_settings

# Carica il file .env usando il percorso corretto
load_settings()

# Configurazione del file di log e timer
EMAIL_INTERVAL = int(os.getenv("EMAIL_INTERVAL_SECONDS", str(15 * 60)))
MAX_BATCH_ENTRIES = int(os.getenv("MAX_BATCH_ENTRIES", "100"))
RETRY_INTERVAL = int(os.getenv("EMAIL_RETRY_SECONDS", "60"))
DATA_RETENTION_DAYS = int(os.getenv("DATA_RETENTION_DAYS", "90"))
USER_RETENTION_DAYS = int(os.getenv("USER_RETENTION_DAYS", "365"))
LOGGER = logging.getLogger(__name__)

def invia_email(data):
    """
    Invia un'email con i dati del file di log.
    """
    # Metodo Account Google (commentare per non utilizzare questo metodo)
    sender_email = os.getenv("SENDER_EMAIL")
    receiver_emails = os.getenv("RECEIVER_EMAIL")
    password = os.getenv("SENDER_PASSWORD") or os.getenv("EMAIL_APP_PASSWORD")

    # Verifica che le variabili d'ambiente siano valide
    if not sender_email or not receiver_emails or not password:
        raise EnvironmentError("Le credenziali email non sono configurate correttamente. Verifica il file .env.")

    # Divide gli indirizzi email separati da virgole in una lista
    receiver_emails = [email.strip() for email in receiver_emails.split(",")]

    # Crea l'oggetto MIMEMultipart
    message = MIMEMultipart("alternative")
    today = date.today().strftime("%d/%m/%Y")
    message["Subject"] = f"Accessi FastCharge {today}"
    message["From"] = sender_email
    message["To"] = ", ".join(receiver_emails)

    # Corpo dell'email
    text = f"{data}"
    part1 = MIMEText(text, "plain")
    message.attach(part1)

    smtp_host = os.getenv("SMTP_HOST", "smtp.fceitalia.it")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_use_tls = os.getenv("SMTP_USE_TLS", "true").lower() in {"1", "true", "yes", "on"}
    smtp_timeout = float(os.getenv("SMTP_TIMEOUT", "15"))

    server = None
    try:
        server = smtplib.SMTP(smtp_host, smtp_port, timeout=smtp_timeout)
        if smtp_use_tls:
            server.starttls()
        server.login(sender_email, password)

        # Invio dell'email
        server.sendmail(sender_email, receiver_emails, message.as_string())
        LOGGER.info("Email inviata con successo a %d destinatari", len(receiver_emails))
        return True

    except (smtplib.SMTPException, ConnectionError, OSError) as e:
        LOGGER.error("Errore durante l'invio dell'email: %s", e)
        return False

    finally:
        if server is not None:
            try:
                server.quit()
            except (smtplib.SMTPException, OSError):
                pass


def format_accesses(accesses: list[Access]) -> str:
    lines = []
    for access in accesses:
        occurred = datetime.fromisoformat(access.occurred_at).astimezone()
        lines.append(
            f"{occurred:%d/%m/%Y %H:%M:%S}\n"
            f"Nome: {access.full_name}\nEmail: {access.email}\n"
            f"Motivazione: {access.reason}"
        )
    return "\n\n".join(lines)


def process_log_batch(database=None):
    """Invia gli accessi pendenti e li marca solo dopo il successo SMTP."""
    store = database or Database()
    accesses = store.pending_accesses(MAX_BATCH_ENTRIES)
    if not accesses:
        return False
    try:
        sent = invia_email(format_accesses(accesses))
    except Exception as error:
        LOGGER.error("Errore durante la preparazione dell'email: %s", error)
        sent = False
    if sent:
        store.mark_notified([access.id for access in accesses])
        return True
    return False

def monitor_log():
    """
    Monitora SQLite e invia periodicamente gli accessi ancora pendenti.
    """
    database = Database()
    database.purge_notified_before(
        datetime.now(timezone.utc) - timedelta(days=DATA_RETENTION_DAYS)
    )
    database.purge_inactive_users_before(
        datetime.now(timezone.utc) - timedelta(days=USER_RETENTION_DAYS)
    )
    last_email_time = time.monotonic()
    last_attempt_time = 0.0
    while True:
        current_time = time.monotonic()
        time_since_last_email = current_time - last_email_time
        pending = database.pending_count()
        ready = pending >= MAX_BATCH_ENTRIES or time_since_last_email >= EMAIL_INTERVAL
        retry_ready = current_time - last_attempt_time >= RETRY_INTERVAL
        if pending and ready and retry_ready:
            last_attempt_time = current_time
            if process_log_batch(database):
                last_email_time = current_time

        # Attendi prima di ricontrollare
        time.sleep(1)

if __name__ == "__main__":
    monitor_log()
