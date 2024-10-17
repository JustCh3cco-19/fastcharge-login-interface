"""
Module Name: interfaccia
Description: This module creates the dashboard in order to make the login or the signup
Author: Francesco Zompanti
"""
import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import cv2
from pyzbar.pyzbar import decode
from generaqrcode import genera_qr_code
from styles import (
    STYLE_FONT, STYLE_BG, STYLE_FG, STYLE_ENTRY_BG, STYLE_ENTRY_FG,
    STYLE_BUTTON_BG, STYLE_BUTTON_FG, STYLE_CREDITS_BG, STYLE_CREDITS_FG
)
from utils import center_window

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class RoundedEntry(tk.Entry):
    """Classe personalizzata per creare Entry con bordi arrotondati"""
    def __init__(self, master=None, **kwargs):
        tk.Entry.__init__(self, master, **kwargs)
        self.configure(
            relief="flat",
            bd=0,
            highlightthickness=0
        )
        # Creare un frame arrotondato attorno all'entry
        self.frame = tk.Frame(
            master,
            borderwidth=2,
            relief="flat",
            background=STYLE_BUTTON_BG
        )
        # Binding per effetti hover
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self.frame.configure(background="#4a90e2")  # Blu più chiaro per hover

    def on_leave(self, e):
        self.frame.configure(background=STYLE_BUTTON_BG)

class RoundedButton(tk.Button):
    """Classe personalizzata per creare Button con bordi arrotondati"""
    def __init__(self, master=None, **kwargs):
        tk.Button.__init__(self, master, **kwargs)
        self.configure(
            relief="flat",
            bd=0,
            highlightthickness=0,
            padx=20,
            pady=10,
            cursor="hand2"  # Cambia il cursore quando sopra il bottone
        )
        # Binding per effetti hover
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self.configure(background="#4a90e2")  # Blu più chiaro per hover

    def on_leave(self, e):
        self.configure(background=STYLE_BUTTON_BG)

class FastChargeInterface:
    """
	Classe che rappresenta l'interfaccia del programma per
	potersi registrare o accedere al sistema
	"""
    def __init__(self, root):
        self.root = root
        self.root.title("Accessi FCE")
        self.root.geometry("1280x720")
        self.root.resizable(False, False)

        # Configurazione dello stile per ttk
        self.style = ttk.Style()
        self.style.configure(
            "Rounded.TEntry",
            fieldbackground=STYLE_ENTRY_BG,
            borderwidth=0,
            relief="flat"
        )

        self.setup_background()
        self.setup_widgets()
        self.mostra_menu_principale()

    def setup_background(self):
        """
		Imposta l'immagine di sfondo ad una certa risoluzione
		"""
        background_path = resource_path('resources/images/fce_logo.png')
        self.background_image = Image.open(background_path)
        self.background_image = self.background_image.resize((1280, 720))
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        
        self.canvas = tk.Canvas(self.root, width=1280, height=720)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(640, 360, image=self.background_photo, anchor="center")

    def setup_widgets(self):
        """
		Crea i vari widgets usati in fase di registrazione ed accesso al sistema
		"""
        # Creare un frame centrale per contenere tutti i widget
        self.main_frame = tk.Frame(self.root, bg=STYLE_BG)
        
        # Configurazione delle etichette e campi di input
        self.label_nome_cognome = tk.Label(self.main_frame, text="Nome e Cognome",
                                     font=STYLE_FONT, bg=STYLE_BG, fg=STYLE_FG)
        self.entry_nome_cognome = RoundedEntry(self.main_frame, 
                                        bg=STYLE_ENTRY_BG,
                                        fg=STYLE_ENTRY_FG, 
                                        font=STYLE_FONT, 
                                        width=30)

        self.label_email = tk.Label(self.main_frame, text="Email", 
                                  font=STYLE_FONT, bg=STYLE_BG, fg=STYLE_FG)
        self.entry_email = RoundedEntry(self.main_frame, 
                                 bg=STYLE_ENTRY_BG,
                                 fg=STYLE_ENTRY_FG, 
                                 font=STYLE_FONT, 
                                 width=30)

        self.label_motivazione_visita = tk.Label(self.main_frame, text="Motivazione Visita",
                                           font=STYLE_FONT, bg=STYLE_BG, fg=STYLE_FG)
        self.entry_motivazione_visita = RoundedEntry(self.main_frame, 
                                              bg=STYLE_ENTRY_BG,
                                              fg=STYLE_ENTRY_FG, 
                                              font=STYLE_FONT, 
                                              width=30)

        # Configurazione dei pulsanti arrotondati
        self.btn_submit = RoundedButton(self.main_frame, 
                                    text="Conferma Registrazione",
                                    command=self.registra_utente,
                                    font=STYLE_FONT, 
                                    bg=STYLE_BUTTON_BG, 
                                    fg=STYLE_BUTTON_FG, 
                                    width=20)

        self.btn_back = RoundedButton(self.main_frame, 
                                  text="Indietro",
                                  command=self.torna_al_menu_principale,
                                  font=STYLE_FONT, 
                                  bg=STYLE_BUTTON_BG, 
                                  fg=STYLE_BUTTON_FG, 
                                  width=20)

        self.btn_registrati = RoundedButton(self.main_frame, 
                                        text="Registrati", 
                                        command=self.show_registration_form,
                                        font=STYLE_FONT, 
                                        bg=STYLE_BUTTON_BG, 
                                        fg=STYLE_BUTTON_FG, 
                                        width=20)

        self.btn_accedi = RoundedButton(self.main_frame, 
                                    text="Accedi", 
                                    command=self.accedi,
                                    font=STYLE_FONT, 
                                    bg=STYLE_BUTTON_BG, 
                                    fg=STYLE_BUTTON_FG, 
                                    width=20)

        self.author_label = tk.Label(self.root, 
                                text="Credits: Francesco Zompanti",
                                font=STYLE_FONT, 
                                fg=STYLE_CREDITS_FG, 
                                bg=STYLE_CREDITS_BG)

    def show_registration_form(self):
        self.nascondi_menu_principale()

        # Pulire i campi
        self.entry_nome_cognome.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_motivazione_visita.delete(0, tk.END)

        # Posizionare il frame principale al centro
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Disporre i widget verticalmente con spaziatura uniforme
        self.label_nome_cognome.pack(pady=5)
        self.entry_nome_cognome.pack(pady=(0, 15))
        
        self.label_email.pack(pady=5)
        self.entry_email.pack(pady=(0, 15))
        
        self.label_motivazione_visita.pack(pady=5)
        self.entry_motivazione_visita.pack(pady=(0, 15))
        
        self.btn_submit.pack(pady=10)
        self.btn_back.pack(pady=5)
        
        self.author_label.place(x=20, y=680)

    def torna_al_menu_principale(self):
        # Nascondere tutti i widget del form
        for widget in self.main_frame.winfo_children():
            widget.pack_forget()
        self.main_frame.place_forget()
        
        self.mostra_menu_principale()

    def mostra_menu_principale(self):
        # Posizionare il frame principale al centro
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Mostrare solo i pulsanti del menu principale
        self.btn_registrati.pack(pady=10)
        self.btn_accedi.pack(pady=10)
        self.author_label.place(x=20, y=680)

    def nascondi_menu_principale(self):
        self.btn_registrati.pack_forget()
        self.btn_accedi.pack_forget()

    def registra_utente(self):
        """
		Funzione che implementa la registrazione dell'utente
		"""
        nome_cognome = self.entry_nome_cognome.get()
        email = self.entry_email.get()
        motivazione_visita = self.entry_motivazione_visita.get()

        if nome_cognome and email:
            log_file_path = os.path.join(os.getcwd(), "resources", "log", "accessi.txt")
            os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

            with open(log_file_path, "a", encoding='utf-8') as file:
                file.write(f"{nome_cognome}\n{email}\nMotivazione visita: {motivazione_visita}\n\n")

            qr_img = genera_qr_code(nome_cognome, email, save_path=True)
            qr_img = qr_img.resize((300, 300))
            qr_photo = ImageTk.PhotoImage(qr_img)

            qr_window = tk.Toplevel(self.root)
            qr_window.title("QR Code")
            qr_window.geometry("400x550")
            qr_window.resizable(False, False)
            center_window(qr_window)

            qr_label = tk.Label(qr_window, image=qr_photo)
            qr_label.image = qr_photo
            qr_label.pack(padx=20, pady=20)

            msg_label1 = tk.Label(
                qr_window,
                text="Accesso effettuato, salva il QR Code per i futuri accessi.",
                font=('Helvetica', 14),
                wraplength=350
            )
            msg_label1.pack(pady=10)

            close_button = RoundedButton(qr_window, 
                                     text="Chiudi", 
                                     command=qr_window.destroy,
                                     font=('Helvetica', 14), 
                                     bg=STYLE_BUTTON_BG, 
                                     fg=STYLE_BUTTON_FG)
            close_button.pack(pady=20)

            self.torna_al_menu_principale()
        else:
            messagebox.showwarning("Errore", "Compila tutti i campi.")

    def accedi(self):
        """
		Sezione accedi, con decodifca qr code e scrittura dei dati in un file accessi.txt
		"""
        def leggi_qr_code(frame):
            qr_codes = decode(frame)
            for qr_code in qr_codes:
                dati_qr = qr_code.data.decode('utf-8')
                return dati_qr
            return None

        def contenuto_presente_nel_file(contenuto, percorso_file):
            try:
                with open(percorso_file, "r", encoding='utf-8') as file:
                    dati_salvati = file.read()
                    return contenuto in dati_salvati
            except FileNotFoundError:
                return False

        def mostra_finestra_motivazione(qr_data):
            # Creare una nuova finestra per la motivazione
            motivazione_window = tk.Toplevel(self.root)
            motivazione_window.title("Inserisci Motivazione")
            motivazione_window.geometry("400x250")
            motivazione_window.resizable(False, False)
            center_window(motivazione_window)
            
            # Frame principale per centrare gli elementi
            frame = tk.Frame(motivazione_window, bg=STYLE_BG)
            frame.place(relx=0.5, rely=0.5, anchor="center")

            # Label per la motivazione
            label_motivazione = tk.Label(frame, 
                                       text="Inserisci la motivazione della visita:",
                                       font=STYLE_FONT, 
                                       bg=STYLE_BG, 
                                       fg=STYLE_FG)
            label_motivazione.pack(pady=10)

            # Campo di input per la motivazione
            entry_motivazione = RoundedEntry(frame,
                                           bg=STYLE_ENTRY_BG,
                                           fg=STYLE_ENTRY_FG,
                                           font=STYLE_FONT,
                                           width=30)
            entry_motivazione.pack(pady=10)

            def conferma_accesso():
                motivazione = entry_motivazione.get()
                if not motivazione:
                    messagebox.showwarning("Errore", "Inserisci una motivazione per continuare.")
                    return

                log_file_path = "resources/log/accessi.txt"

                # Controlla se l'utente è già presente nel file
                if contenuto_presente_nel_file(qr_data, log_file_path):
                    messagebox.showinfo("Accesso", "Accesso già effettuato!")
                else:
                    # Scrive i dati nel file includendo la motivazione
                    with open(log_file_path, "a", encoding='utf-8') as file:
                        file.write(f"{qr_data}\nMotivazione visita: {motivazione}\n\n")
                    messagebox.showinfo("Accesso", "Accesso effettuato!")
                
                motivazione_window.destroy()

            # Bottone di conferma
            btn_conferma = RoundedButton(frame,
                                       text="Conferma Accesso",
                                       command=conferma_accesso,
                                       font=STYLE_FONT,
                                       bg=STYLE_BUTTON_BG,
                                       fg=STYLE_BUTTON_FG,
                                       width=20)
            btn_conferma.pack(pady=20)

        #log_file_path = "resources/log/accessi.txt"

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Errore", "Errore nell'apertura della webcam.")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                messagebox.showerror("Errore", "Errore nella lettura del frame.")
                break

            contenuto_qr = leggi_qr_code(frame)
            if contenuto_qr:
                cap.release()
                cv2.destroyAllWindows()
                mostra_finestra_motivazione(contenuto_qr)
                break

            cv2.imshow('Scansiona il QR Code', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

def run_interface():
    root = tk.Tk()
    app = FastChargeInterface(root)
    center_window(root)
    root.mainloop()

if __name__ == "__main__":
    run_interface()