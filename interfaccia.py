"""
Module Name: interfaccia
Description: This module creates the dashboard in order to make the login or the signup
Author: Francesco Zompanti
"""
import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import font as tkfont
from PIL import Image, ImageTk
import cv2
from pyzbar.pyzbar import decode
from generaqrcode import genera_qr_code
from styles import (
    STYLE_BG, STYLE_FG, STYLE_ENTRY_BG, STYLE_ENTRY_FG,
    STYLE_BUTTON_BG, STYLE_BUTTON_FG, STYLE_CREDITS_BG, STYLE_CREDITS_FG, get_font
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
            padx=30,  # Aumentato il padding orizzontale
            pady=15,  # Aumentato il padding verticale
            cursor="hand2"
        )
        # Binding per effetti hover
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self.configure(background="#4a90e2")

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
        self.root.geometry("1920x1080")

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
        self.background_image = self.background_image.resize((1920, 1080))
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        
        self.canvas = tk.Canvas(self.root, width=1920, height=1080)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(960, 540, image=self.background_photo, anchor="center")

    def setup_widgets(self):
        """
        Crea i vari widgets usati in fase di registrazione ed accesso al sistema
        """
        self.main_frame = tk.Frame(self.root, bg=STYLE_BG, width=800, height=600)

        self.credits_frame = tk.Frame(self.root, bg=STYLE_CREDITS_BG)
        self.credits_frame.place(relx=0.00, rely=0.99, anchor="sw")
        
        # Usare il font FiraSans per tutto
        large_font = get_font(24, "bold")
        entry_font = get_font(20)
        
        self.label_nome_cognome = tk.Label(self.main_frame, text="Nome e Cognome",
                                     font=large_font, bg=STYLE_BG, fg=STYLE_FG)
        self.entry_nome_cognome = RoundedEntry(self.main_frame, 
                                        bg=STYLE_ENTRY_BG,
                                        fg=STYLE_ENTRY_FG, 
                                        font=entry_font, 
                                        width=40)

        self.label_email = tk.Label(self.main_frame, text="Email", 
                                  font=large_font, bg=STYLE_BG, fg=STYLE_FG)
        self.entry_email = RoundedEntry(self.main_frame, 
                                 bg=STYLE_ENTRY_BG,
                                 fg=STYLE_ENTRY_FG, 
                                 font=entry_font, 
                                 width=40)

        self.label_motivazione_visita = tk.Label(self.main_frame, text="Motivazione Visita",
                                           font=large_font, bg=STYLE_BG, fg=STYLE_FG)
        self.entry_motivazione_visita = RoundedEntry(self.main_frame, 
                                              bg=STYLE_ENTRY_BG,
                                              fg=STYLE_ENTRY_FG, 
                                              font=entry_font, 
                                              width=40)

        # Bottoni più grandi con il font FiraSans
        self.btn_submit = RoundedButton(self.main_frame, 
                                    text="Conferma Registrazione",
                                    command=self.registra_utente,
                                    font=large_font, 
                                    bg=STYLE_BUTTON_BG, 
                                    fg=STYLE_BUTTON_FG, 
                                    width=25)

        self.btn_back = RoundedButton(self.main_frame, 
                                  text="Indietro",
                                  command=self.torna_al_menu_principale,
                                  font=large_font, 
                                  bg=STYLE_BUTTON_BG, 
                                  fg=STYLE_BUTTON_FG, 
                                  width=25)

        self.btn_registrati = RoundedButton(self.main_frame, 
                                        text="Registrati", 
                                        command=self.show_registration_form,
                                        font=large_font, 
                                        bg=STYLE_BUTTON_BG, 
                                        fg=STYLE_BUTTON_FG, 
                                        width=25)

        self.btn_accedi = RoundedButton(self.main_frame, 
                                    text="Scansiona", 
                                    command=self.accedi,
                                    font=large_font, 
                                    bg=STYLE_BUTTON_BG, 
                                    fg=STYLE_BUTTON_FG, 
                                    width=25)

        # Credits con il font FiraSans
        self.author_label = tk.Label(
            self.credits_frame, 
            text="Credits: Francesco Zompanti",
            font=get_font(20, "bold"),  # Font FiraSans in grassetto
            fg=STYLE_CREDITS_FG, 
            bg=STYLE_CREDITS_BG,
            padx=10,  
            pady=5    
        )
        self.author_label.pack()

    def show_registration_form(self):
        self.nascondi_menu_principale()

        # Pulire i campi
        self.entry_nome_cognome.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_motivazione_visita.delete(0, tk.END)

        # Posizionare il frame principale più in basso
        self.main_frame.place(relx=0.5, rely=0.6, anchor="center")

        # Disporre i widget verticalmente con spaziatura maggiore
        self.label_nome_cognome.pack(pady=10)
        self.entry_nome_cognome.pack(pady=(0, 25))
    
        self.label_email.pack(pady=10)
        self.entry_email.pack(pady=(0, 25))
    
        self.label_motivazione_visita.pack(pady=10)
        self.entry_motivazione_visita.pack(pady=(0, 25))
    
        self.btn_submit.pack(pady=20)
        self.btn_back.pack(pady=10)

    def torna_al_menu_principale(self):
        # Nascondere tutti i widget del form
        for widget in self.main_frame.winfo_children():
            widget.pack_forget()
        self.main_frame.place_forget()
        
        self.mostra_menu_principale()
    
    def mostra_menu_principale(self):
        # Posizionare il frame principale al centro
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Mostrare i pulsanti del menu principale con spaziatura maggiore
        self.btn_registrati.pack(pady=20)
        self.btn_accedi.pack(pady=20)
        # I credits rimangono visibili grazie al frame separato

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
                file.write(f"{nome_cognome}\n{email}\nMotivazione Visita: {motivazione_visita}\n")
                print(f"{nome_cognome}\n{email}\nMotivazione Visita: {motivazione_visita}")

            qr_img = genera_qr_code(nome_cognome, email, save_path=True)
            qr_img = qr_img.resize((400, 400))  # QR code più grande
            qr_photo = ImageTk.PhotoImage(qr_img)

            qr_window = tk.Toplevel(self.root)
            qr_window.title("QR Code")
            qr_window.geometry("600x800")  # Finestra QR più grande
            qr_window.resizable(False, False)
            center_window(qr_window)

            qr_label = tk.Label(qr_window, image=qr_photo)
            qr_label.image = qr_photo
            qr_label.pack(padx=30, pady=30)

            msg_label1 = tk.Label(
                qr_window,
                text="Accesso effettuato, salva il QR Code per i futuri accessi.",
                font=('Helvetica', 20),
                wraplength=500
            )
            msg_label1.pack(pady=20)

            close_button = RoundedButton(qr_window, 
                                     text="Chiudi", 
                                     command=qr_window.destroy,
                                     font=('Helvetica', 20), 
                                     bg=STYLE_BUTTON_BG, 
                                     fg=STYLE_BUTTON_FG)
            close_button.pack(pady=30)

            self.torna_al_menu_principale()
        else:
            messagebox.showwarning("Errore", "Compila tutti i campi.")

    def accedi(self):
        """
        Sezione accedi, con decodifica qr code integrata nell'interfaccia
        e scrittura dei dati in un file accessi.txt
        """
        def leggi_qr_code(frame):
            """Decodifica il QR code dal frame della fotocamera"""
            qr_codes = decode(frame)
            for qr_code in qr_codes:
                dati_qr = qr_code.data.decode('utf-8')
                return dati_qr
            return None

        def contenuto_presente_nel_file(contenuto, percorso_file):
            """Verifica se i dati del QR sono già presenti nel file"""
            try:
                with open(percorso_file, "r", encoding='utf-8') as file:
                    dati_salvati = file.read()
                    return contenuto in dati_salvati
            except FileNotFoundError:
                return False

        def mostra_finestra_motivazione(qr_data):
            """Mostra la finestra per inserire la motivazione della visita"""
            motivazione_window = tk.Toplevel(self.root)
            motivazione_window.title("Inserisci Motivazione")
            motivazione_window.geometry("600x400")
            motivazione_window.resizable(False, False)
            
            # Rendi la finestra trasparente per vedere lo sfondo
            motivazione_window.configure(bg=STYLE_BG)
            motivazione_window.attributes('-alpha', 0.95)
            
            # Frame principale per centrare gli elementi
            frame = tk.Frame(motivazione_window, bg=STYLE_BG)
            frame.place(relx=0.5, rely=0.5, anchor="center")

            # Label per la motivazione
            label_motivazione = tk.Label(
                frame, 
                text="Motivazione visita",
                font=('Helvetica', 20, 'bold'),
                bg=STYLE_BG,
                fg=STYLE_FG
            )
            label_motivazione.pack(pady=20)

            # Campo di input per la motivazione
            entry_motivazione = RoundedEntry(
                frame,
                bg=STYLE_ENTRY_BG,
                fg=STYLE_ENTRY_FG,
                font=('Helvetica', 16),
                width=40
            )
            entry_motivazione.pack(pady=20)

            def conferma_accesso():
                """Gestisce la conferma dell'accesso e la scrittura su file"""
                motivazione = entry_motivazione.get()
                if not motivazione:
                    messagebox.showwarning(
                        "Errore", 
                        "Inserisci una motivazione per continuare."
                    )
                    return

                log_file_path = os.path.join("resources", "log", "accessi.txt")
                os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

                if contenuto_presente_nel_file(qr_data, log_file_path):
                    messagebox.showinfo("Accesso", "Accesso già effettuato!")
                else:
                    with open(log_file_path, "a", encoding='utf-8') as file:
                        file.write(f"{qr_data}\nMotivazione visita: {motivazione}\n\n")
                        print(f"{qr_data}\nMotivazione visita: {motivazione}")
                    messagebox.showinfo("Accesso", "Accesso effettuato con successo!")
                
                motivazione_window.destroy()

            # Bottone di conferma
            btn_conferma = RoundedButton(
                frame,
                text="Conferma Accesso",
                command=conferma_accesso,
                font=('Helvetica', 18, 'bold'),
                bg=STYLE_BUTTON_BG,
                fg=STYLE_BUTTON_FG,
                width=20
            )
            btn_conferma.pack(pady=30)
            
            # Centra la finestra
            center_window(motivazione_window)

        def setup_camera_window():
            """Configura la finestra della fotocamera"""
            camera_window = tk.Toplevel(self.root)
            camera_window.title("Scansiona il tuo QR Code")
            
            # Configura dimensioni e posizione
            window_width = 800
            window_height = 600
            camera_window.geometry(f"{window_width}x{window_height}")
            camera_window.resizable(False, False)
            
            # Rendi la finestra semi-trasparente
            camera_window.configure(bg=STYLE_BG)
            camera_window.attributes('-alpha', 0.95)
            
            # Frame principale
            main_frame = tk.Frame(camera_window, bg=STYLE_BG)
            main_frame.pack(expand=True, fill="both", padx=20, pady=20)
            
            # Label istruzioni
            instructions = tk.Label(
                main_frame,
                text="Posiziona il QR Code davanti alla fotocamera",
                font=('Helvetica', 18, 'bold'),
                bg=STYLE_BG,
                fg=STYLE_FG
            )
            instructions.pack(pady=20)
            
            # Frame per il feed della fotocamera
            camera_frame = tk.Frame(
                main_frame,
                bg=STYLE_BG,
                width=640,
                height=480
            )
            camera_frame.pack(pady=10)
            
            # Label per il feed della fotocamera
            camera_label = tk.Label(camera_frame)
            camera_label.pack()
            
            center_window(camera_window)
            return camera_window, camera_label

        def aggiorna_camera(cap, camera_label, camera_window):
            """Aggiorna il feed della fotocamera e cerca QR codes"""
            if not cap.isOpened():
                camera_window.destroy()
                messagebox.showerror("Errore", "La fotocamera si è disconnessa.")
                return

            ret, frame = cap.read()
            if ret:
                # Ridimensiona il frame mantenendo le proporzioni
                frame = cv2.resize(frame, (640, 480))
                
                # Converti il frame per Tkinter
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                imgtk = ImageTk.PhotoImage(image=img)
                camera_label.imgtk = imgtk
                camera_label.configure(image=imgtk)
                
                # Cerca QR code
                contenuto_qr = leggi_qr_code(frame)
                if contenuto_qr:
                    cap.release()
                    camera_window.destroy()
                    mostra_finestra_motivazione(contenuto_qr)
                    return
                
                camera_window.after(10, lambda: aggiorna_camera(cap, camera_label, camera_window))

        # Inizializza la fotocamera
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Errore", "Impossibile accedere alla fotocamera.")
            return

        # Configura e mostra la finestra della fotocamera
        camera_window, camera_label = setup_camera_window()
        
        # Avvia l'aggiornamento della fotocamera
        aggiorna_camera(cap, camera_label, camera_window)
        
        def on_closing():
            """Gestisce la chiusura pulita della finestra della fotocamera"""
            cap.release()
            camera_window.destroy()
        
        camera_window.protocol("WM_DELETE_WINDOW", on_closing)

def run_interface():
    root = tk.Tk()
    app = FastChargeInterface(root)
    center_window(root)
    root.mainloop()

if __name__ == "__main__":
    run_interface()