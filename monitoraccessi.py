"""
Module Name: monitoraccessi
Description: This module checks if accessi.txt file contains data 
            and it sends to the RECEIVER_EMAIL address.
Author: Francesco Zompanti
"""
from datetime import date
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import sys
import time
from dotenv import load_dotenv

def resource_path(relative_path):
    """Ottiene il percorso assoluto del file, sia per PyInstaller che per lo script."""
    try:
        # Percorso quando viene eseguito come bundle PyInstaller
        base_path = sys._MEIPASS
    except AttributeError:
        # Percorso quando viene eseguito come script Python
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Carica il file .env usando il percorso corretto
dotenv_path = resource_path(".env")
load_dotenv(dotenv_path=dotenv_path)

# Configurazione del file di log e timer
LOG_FILE_PATH = "resources/log/accessi.txt"  # Percorso del file di log
EMAIL_INTERVAL = 15 * 60  # 15 minuti in secondi
MAX_FILE_SIZE = 1024  # Dimensione massima del file di log in byte prima dell'invio dell'email

def invia_email(data):
    """
    Invia un'email con i dati del file di log.
    """
    # Metodo Account Google (commentare per non utilizzare questo metodo)
    sender_email = os.getenv("SENDER_EMAIL")
    receiver_emails = os.getenv("RECEIVER_EMAIL")
    password = os.getenv("SENDER_PASSWORD")

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

    try:
        # Connessione al server SMTP
        # server = smtplib.SMTP("smtp.gmail.com", 587)
        # server.starttls()
        # server.login(sender_email, password)
        
        server = smtplib.SMTP("smtp.fceitalia.it", 587)
        server.starttls()
        server.login(sender_email, password)

        # Invio dell'email
        server.sendmail(sender_email, receiver_emails, message.as_string())
        print(f"Email inviata con successo agli indirizzi {', '.join(receiver_emails)}!")

    except (smtplib.SMTPException, ConnectionError) as e:
        print(f"Errore durante l'invio dell'email: {e}")

    finally:
        server.quit()

def monitor_log():
    """
    Monitora il file di log e invia un'email ogni 15 minuti 
    o quando il file raggiunge la dimensione massima.
    """
    last_email_time = time.time()
    while True:
        current_time = time.time()
        time_since_last_email = current_time - last_email_time

        # Controlla se il file di log esiste e contiene dati
        if os.path.exists(LOG_FILE_PATH) and os.path.getsize(LOG_FILE_PATH) > 0:
            # Se il file supera la dimensione massima o sono passati 15 minuti, invia un'email
            if (os.path.getsize(LOG_FILE_PATH) >= MAX_FILE_SIZE or
                time_since_last_email >= EMAIL_INTERVAL):
                # Leggi i dati dal file di log
                with open(LOG_FILE_PATH, "r", encoding='utf-8') as file:
                    log_data = file.read()

                # Invia l'email con i dati accumulati
                invia_email(log_data)

                # Svuota il file di log dopo l'invio
                with open(LOG_FILE_PATH, "w", encoding='utf-8') as file:
                    file.write("")

                # Aggiorna il tempo dell'ultimo invio email
                last_email_time = current_time

        # Attendi prima di ricontrollare
        time.sleep(1)

if __name__ == "__main__":
    monitor_log()
