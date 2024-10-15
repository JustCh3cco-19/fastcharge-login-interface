import cv2
from pyzbar.pyzbar import decode
import tkinter as tk
from tkinter import messagebox

LOG_FILE_PATH = "resources/log/accessi.txt"  # Percorso del file di log

# Funzione per decodificare un frame e cercare QR code
def leggi_qr_code(frame):
    qr_codes = decode(frame)
    for qr_code in qr_codes:
        dati_qr = qr_code.data.decode('utf-8')
        return dati_qr
    return None

# Funzione per controllare se il contenuto è già presente nel file di log
def contenuto_presente_nel_file(contenuto, percorso_file):
    try:
        with open(percorso_file, "r") as file:
            dati_salvati = file.read()
            if contenuto in dati_salvati:
                return True
    except FileNotFoundError:
        # Se il file non esiste, lo consideriamo vuoto
        return False
    return False

# Funzione per mostrare la finestra di dialogo con Tkinter
def mostra_messaggio(titolo, messaggio):
    root = tk.Tk()
    root.withdraw()  # Nasconde la finestra principale di Tkinter
    messagebox.showinfo(titolo, messaggio)  # Mostra il messaggio
    root.destroy()  # Chiude la finestra principale di Tkinter

# Aprire lo stream della webcam
cap = cv2.VideoCapture(0)  # 0 per la webcam predefinita

# Verifica se la webcam è stata aperta correttamente
if not cap.isOpened():
    print("Errore nell'apertura della webcam.")
    exit()

# Loop per leggere i frame della webcam
while True:
    ret, frame = cap.read()  # Leggi un frame

    if not ret:
        print("Errore nella lettura del frame.")
        break

    # Prova a decodificare il QR code dal frame
    contenuto_qr = leggi_qr_code(frame)

    # Se trovi un QR code, mostra il suo contenuto
    if contenuto_qr:
        print(f"Contenuto del QR code: {contenuto_qr}")

        # Controlla se il contenuto è già presente nel file di log
        if contenuto_presente_nel_file(contenuto_qr, LOG_FILE_PATH):
            # Mostra il messaggio di "Accesso già effettuato" con Tkinter
            mostra_messaggio("", "Accesso gia' effettuato!")
        else:
            # Salva il contenuto in un file .txt
            with open(LOG_FILE_PATH, "a") as file:  # Usa "a" per aggiungere al file
                file.write(contenuto_qr + "\n")
            # Mostra il messaggio "Accesso registrato" con Tkinter
            mostra_messaggio("", "Accesso effettuato!")

        # Esci dal ciclo e chiudi tutto una volta controllato il QR code
        break

    # Mostra il video in tempo reale
    cv2.imshow('Scansiona il QR Code', frame)

    # Aggiungi una piccola pausa per consentire la visualizzazione del frame
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Rilascia la webcam e chiudi le finestre di OpenCV
cap.release()
cv2.destroyAllWindows()
