from datetime import date
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import time
from dotenv import load_dotenv

# Carica la password per l'app Google, altrimenti non funziona il codice e non viene inviata la mail
load_dotenv()

# Configurazione del file di log e timer
LOG_FILE_PATH = "resources/log/accessi.txt"  # Percorso del file di log
EMAIL_INTERVAL = 1 * 60  # 15 minuti in secondi
MAX_FILE_SIZE = 1024  # Dimensione massima del file di log in byte prima dell'invio dell'email

def invia_email(data):
    """
    Invia un'email con i dati del file di log.
    """
    # Metodo Account Google (commentare per non utilizzare questo metodo)
    sender_email = os.getenv("SENDER_EMAIL")
    receiver_email = os.getenv("RECEIVER_EMAIL")
    password = os.getenv("EMAIL_APP_PASSWORD")
    
    # Metodo Aruba (togliere hashtag per utilizzare Aruba)
    # sender_email = os.getenv("SENDER_EMAIL")
    # receiver_email = os.getenv("RECEIVER_EMAIL")
    # password = os.getenv("SENDER_PASSWORD")

    # Crea l'oggetto MIMEMultipart
    message = MIMEMultipart("alternative")
    today = date.today().strftime("%d/%m/%Y")
    message["Subject"] = f"Accessi FastCharge {today}"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Corpo dell'email
    text = f"{data}"
    part1 = MIMEText(text, "plain")
    message.attach(part1)

    try:
        # Connessione al server SMTP di Gmail (commentare per non utilizzare questo metodo)
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)

        # Connessione al server SMTP di Aruba (togliere hashtag per utilizzare Aruba)
        # server = smtplib.SMTP("smtps.aruba.it", 465)
        # server.starttls()
        # server.login(sender_email, password)

        # Invio dell'email (unico)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print(f"Email inviata con successo all'indirizzo {receiver_email}!")

    except Exception as e:
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
            if os.path.getsize(LOG_FILE_PATH) >= MAX_FILE_SIZE or time_since_last_email >= EMAIL_INTERVAL:
                # Leggi i dati dal file di log
                with open(LOG_FILE_PATH, "r") as file:
                    log_data = file.read()

                # Invia l'email con i dati accumulati
                invia_email(log_data)

                # Svuota il file di log dopo l'invio
                with open(LOG_FILE_PATH, "w") as file:
                    file.write("")

                # Aggiorna il tempo dell'ultimo invio email
                last_email_time = current_time

        # Attendi prima di ricontrollare
        time.sleep(5)

if __name__ == "__main__":
    print("MONITOR ACCESSI ONLINE")
    monitor_log()
