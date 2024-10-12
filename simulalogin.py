import time
import locale
from datetime import datetime

LOG_FILE_PATH = "accessi.txt"  # Percorso del file di log

# Imposta la localizzazione italiana
locale.setlocale(locale.LC_TIME, "it_IT.UTF-8")

def simula_accessi(n_persone):
    """
    Simula l'inserimento di n persone nel file di log con data in formato italiano.
    """
    with open(LOG_FILE_PATH, "a") as log_file:
        for i in range(n_persone):
            # Ottieni la data corrente formattata in italiano
            data_corrente = datetime.now().strftime("%A %d %B %Y, %H:%M:%S")
            log_file.write(f"Persona_{i+1} ha fatto l'accesso in data: {data_corrente}\n")
            print(f"Persona_{i+1} ha fatto l'accesso in data: {data_corrente}")

# Simula il login di 5 persone
simula_accessi(5)
