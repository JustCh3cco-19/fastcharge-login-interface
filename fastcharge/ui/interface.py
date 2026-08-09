"""
Module Name: interfaccia
Description: This module creates the dashboard in order to make the login or the signup
Author: Francesco Zompanti
"""
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import cv2
from fastcharge.services.qr import genera_qr_code
from fastcharge.database import Database, DuplicateAccessError
from fastcharge.paths import resource_path
from fastcharge.security import create_token, verify_token
from fastcharge.settings import load_settings
from fastcharge.validation import validate_reason, validate_registration
from fastcharge.ui.styles import (
    STYLE_BG, STYLE_FG, STYLE_ENTRY_BG, STYLE_ENTRY_FG,
    STYLE_BUTTON_BG, STYLE_BUTTON_FG,
    STYLE_SECONDARY_BG, STYLE_SECONDARY_HOVER, STYLE_PANEL_BG,
    STYLE_PANEL_BORDER, STYLE_CREDITS_BG, STYLE_CREDITS_FG, get_font
)

from fastcharge.ui.window import center_window
from fastcharge.ui.widgets import RoundedButton, RoundedEntry

class FastChargeInterface:
    """
	Classe che rappresenta l'interfaccia del programma per
	potersi registrare o accedere al sistema
	"""
    def __init__(self, root):
        self.root = root
        self.root.title("Accessi FCE")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        initial_width = min(1440, max(760, round(screen_width * 0.92)))
        initial_height = min(900, max(540, round(screen_height * 0.88)))
        self.root.geometry(f"{initial_width}x{initial_height}")
        self.root.minsize(720, 520)
        self._current_scale = 1.0
        self._resize_job = None
        load_settings()
        self.database = Database()
        self.qr_detector = cv2.QRCodeDetector()

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
        self.background_source = Image.open(background_path)
        self.background_photo = ImageTk.PhotoImage(self.background_source)
        
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.background_item = self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")
        self.root.bind("<Configure>", self.resize_background)

    def resize_background(self, event):
        if event.widget is not self.root or event.width < 2 or event.height < 2:
            return
        if self._resize_job is not None:
            self.root.after_cancel(self._resize_job)
        self._resize_job = self.root.after(
            40, lambda: self.apply_responsive_layout(event.width, event.height)
        )

    def apply_responsive_layout(self, width, height):
        """Adatta sfondo e controlli alla dimensione effettiva della finestra."""
        image = self.background_source.copy()
        image.thumbnail((width, height), Image.Resampling.LANCZOS)
        background = Image.new("RGB", (width, height), STYLE_BG)
        offset = ((width - image.width) // 2, (height - image.height) // 2)
        background.paste(image, offset)
        self.background_photo = ImageTk.PhotoImage(background)
        self.canvas.itemconfigure(self.background_item, image=self.background_photo)
        scale = max(0.68, min(1.35, width / 1280, height / 800))
        if abs(scale - self._current_scale) < 0.02:
            return
        self._current_scale = scale
        self.main_frame.configure(
            padx=round(48 * scale),
            pady=round(36 * scale),
        )
        self.menu_title.configure(font=get_font(max(18, round(28 * scale)), "bold"))
        self.menu_subtitle.configure(font=get_font(max(11, round(14 * scale))))
        self.menu_subtitle.configure(wraplength=round(520 * scale))
        field_label_font = get_font(max(15, round(24 * scale)), "bold")
        field_font = get_font(max(13, round(20 * scale)))
        for label in (
            self.label_nome_cognome,
            self.label_email,
            self.label_motivazione_visita,
        ):
            label.configure(font=field_label_font)
        for entry in (
            self.entry_nome_cognome,
            self.entry_email,
            self.entry_motivazione_visita,
        ):
            entry.configure(font=field_font, width=36)
        self.privacy_notice.configure(
            font=get_font(max(10, round(12 * scale))),
            wraplength=round(620 * scale),
        )
        self.author_label.configure(font=get_font(max(12, round(20 * scale)), "bold"))
        for button in (
            self.btn_submit,
            self.btn_back,
            self.btn_registrati,
            self.btn_accedi,
        ):
            button.apply_scale(scale)

    def fit_window_size(self, preferred_width, preferred_height, ratio=0.9):
        """Limita una finestra secondaria allo spazio realmente disponibile."""
        max_width = round(self.root.winfo_screenwidth() * ratio)
        max_height = round(self.root.winfo_screenheight() * ratio)
        return min(preferred_width, max_width), min(preferred_height, max_height)

    def setup_widgets(self):
        """
        Crea i vari widgets usati in fase di registrazione ed accesso al sistema
        """
        self.main_frame = tk.Frame(
            self.root,
            bg=STYLE_PANEL_BG,
            padx=48,
            pady=36,
            highlightbackground=STYLE_PANEL_BORDER,
            highlightthickness=1,
        )

        self.credits_frame = tk.Frame(self.root, bg=STYLE_CREDITS_BG)
        self.credits_frame.place(relx=0.00, rely=0.99, anchor="sw")
        
        # Usare il font FiraSans per tutto
        large_font = get_font(24, "bold")
        entry_font = get_font(20)

        self.menu_title = tk.Label(
            self.main_frame,
            text="Gestione accessi",
            font=get_font(28, "bold"),
            bg=STYLE_PANEL_BG,
            fg=STYLE_FG,
        )
        self.menu_subtitle = tk.Label(
            self.main_frame,
            text="Registra un visitatore oppure scansiona un QR Code",
            font=get_font(14),
            bg=STYLE_PANEL_BG,
            fg="#555555",
            wraplength=520,
        )
        
        self.label_nome_cognome = tk.Label(self.main_frame, text="Nome e Cognome",
                                     font=large_font, bg=STYLE_PANEL_BG, fg=STYLE_FG)
        self.entry_nome_cognome = RoundedEntry(self.main_frame, 
                                        bg=STYLE_ENTRY_BG,
                                        fg=STYLE_ENTRY_FG, 
                                        font=entry_font, 
                                        width=40)

        self.label_email = tk.Label(self.main_frame, text="Email", 
                                  font=large_font, bg=STYLE_PANEL_BG, fg=STYLE_FG)
        self.entry_email = RoundedEntry(self.main_frame, 
                                 bg=STYLE_ENTRY_BG,
                                 fg=STYLE_ENTRY_FG, 
                                 font=entry_font, 
                                 width=40)

        self.label_motivazione_visita = tk.Label(self.main_frame, text="Motivazione Visita",
                                           font=large_font, bg=STYLE_PANEL_BG, fg=STYLE_FG)
        self.entry_motivazione_visita = RoundedEntry(self.main_frame, 
                                              bg=STYLE_ENTRY_BG,
                                              fg=STYLE_ENTRY_FG, 
                                              font=entry_font, 
                                              width=40)
        self.privacy_notice = tk.Label(
            self.main_frame,
            text=(
                "I dati inseriti saranno utilizzati esclusivamente per registrare "
                "e notificare l'accesso."
            ),
            bg=STYLE_PANEL_BG,
            fg=STYLE_FG,
            font=get_font(12),
            wraplength=620,
        )

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
                                  bg=STYLE_SECONDARY_BG,
                                  fg=STYLE_BUTTON_FG, 
                                  hover_bg=STYLE_SECONDARY_HOVER,
                                  border_color=STYLE_BUTTON_BG,
                                  width=25)

        self.btn_registrati = RoundedButton(self.main_frame, 
                                        text="REGISTRA VISITATORE",
                                        command=self.show_registration_form,
                                        font=get_font(20, "bold"),
                                        bg=STYLE_BUTTON_BG, 
                                        fg=STYLE_BUTTON_FG, 
                                        width=40)

        self.btn_accedi = RoundedButton(self.main_frame, 
                                    text="SCANSIONA QR CODE",
                                    command=self.accedi,
                                    font=get_font(20, "bold"),
                                    bg=STYLE_SECONDARY_BG,
                                    fg=STYLE_BUTTON_FG, 
                                    hover_bg=STYLE_SECONDARY_HOVER,
                                    border_color="#222222",
                                    width=40)

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
        self.main_frame.place(relx=0.5, rely=0.52, anchor="center")

        # Disporre i widget verticalmente con spaziatura maggiore
        self.label_nome_cognome.pack(pady=10)
        self.entry_nome_cognome.pack(pady=(0, 25))
    
        self.label_email.pack(pady=10)
        self.entry_email.pack(pady=(0, 25))
    
        self.label_motivazione_visita.pack(pady=10)
        self.entry_motivazione_visita.pack(pady=(0, 25))
        self.privacy_notice.pack(pady=(0, 10))
    
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
        self.menu_title.pack(pady=(0, 8))
        self.menu_subtitle.pack(pady=(0, 28))
        self.btn_registrati.pack(pady=(0, 14))
        self.btn_accedi.pack(pady=(0, 4))
        # I credits rimangono visibili grazie al frame separato

    def nascondi_menu_principale(self):
        self.menu_title.pack_forget()
        self.menu_subtitle.pack_forget()
        self.btn_registrati.pack_forget()
        self.btn_accedi.pack_forget()

    def registra_utente(self):
        """
        Funzione che implementa la registrazione dell'utente
        """
        nome_cognome = self.entry_nome_cognome.get()
        email = self.entry_email.get()
        motivazione_visita = self.entry_motivazione_visita.get()

        errors = validate_registration(nome_cognome, email, motivazione_visita)
        if not errors:
            user = self.database.register_user(nome_cognome, email)
            try:
                self.database.record_access(user.id, motivazione_visita)
            except DuplicateAccessError:
                pass
            qr_token = create_token(user.id)
            qr_img = genera_qr_code(qr_token, user.id, save_path=True)

            qr_window = tk.Toplevel(self.root)
            qr_window.title("QR Code")
            qr_width, qr_height = self.fit_window_size(520, 650, 0.86)
            qr_window.geometry(f"{qr_width}x{qr_height}")
            qr_window.resizable(True, True)
            center_window(qr_window)

            qr_display_size = min(320, qr_width - 80, qr_height - 260)
            qr_img = qr_img.resize((qr_display_size, qr_display_size))
            qr_photo = ImageTk.PhotoImage(qr_img)
            qr_label = tk.Label(qr_window, image=qr_photo)
            qr_label.image = qr_photo
            qr_label.pack(padx=30, pady=30)

            msg_label1 = tk.Label(
                qr_window,
                text="Accesso effettuato, salva il QR Code per i futuri accessi.",
                font=("Helvetica", 18),
                wraplength=460,
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
            messagebox.showwarning("Dati non validi", "\n".join(errors))

    def accedi(self):
        """
        Sezione accedi, con decodifica qr code integrata nell'interfaccia
        e registrazione dell'accesso nel database.
        """
        def leggi_qr_code(frame):
            """Decodifica il QR code dal frame della fotocamera"""
            data, _points, _straight = self.qr_detector.detectAndDecode(frame)
            return data or None

        def mostra_finestra_motivazione(user):
            """Mostra la finestra per inserire la motivazione della visita"""
            motivazione_window = tk.Toplevel(self.root)
            motivazione_window.title("Inserisci Motivazione")
            reason_width, reason_height = self.fit_window_size(600, 400, 0.86)
            motivazione_window.geometry(f"{reason_width}x{reason_height}")
            motivazione_window.resizable(True, True)
            
            # Rendi la finestra trasparente per vedere lo sfondo
            motivazione_window.configure(bg=STYLE_BG)
            motivazione_window.attributes("-alpha", 0.95)
            
            # Frame principale per centrare gli elementi
            frame = tk.Frame(motivazione_window, bg=STYLE_BG)
            frame.place(relx=0.5, rely=0.5, anchor="center")

            # Label per la motivazione
            label_motivazione = tk.Label(
                frame, 
                text="Motivazione visita",
                font=("Helvetica", 20, "bold"),
                bg=STYLE_BG,
                fg=STYLE_FG
            )
            label_motivazione.pack(pady=20)

            # Campo di input per la motivazione
            entry_motivazione = RoundedEntry(
                frame,
                bg=STYLE_ENTRY_BG,
                fg=STYLE_ENTRY_FG,
                font=("Helvetica", 16),
                width=40
            )
            entry_motivazione.pack(pady=20)

            def conferma_accesso():
                """Gestisce la conferma dell'accesso e la scrittura su file"""
                motivazione = entry_motivazione.get()
                reason_error = validate_reason(motivazione)
                if reason_error:
                    messagebox.showwarning("Errore", reason_error)
                    return
                try:
                    self.database.record_access(user.id, motivazione)
                except DuplicateAccessError as error:
                    messagebox.showinfo("Accesso", str(error))
                else:
                    messagebox.showinfo(
                        "Accesso", f"Benvenuto, {user.full_name}. Accesso registrato!"
                    )
                
                motivazione_window.destroy()

            # Bottone di conferma
            btn_conferma = RoundedButton(
                frame,
                text="Conferma Accesso",
                command=conferma_accesso,
                font=("Helvetica", 18, "bold"),
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
            
            # Configura dimensioni e posizione in base allo schermo disponibile
            window_width, window_height = self.fit_window_size(800, 650, 0.88)
            feed_width = max(320, min(640, window_width - 80))
            feed_height = max(240, min(480, window_height - 150))
            camera_window.geometry(f"{window_width}x{window_height}")
            camera_window.resizable(True, True)
            
            # Rendi la finestra semi-trasparente
            camera_window.configure(bg=STYLE_BG)
            camera_window.attributes("-alpha", 0.95)
            
            # Frame principale
            main_frame = tk.Frame(camera_window, bg=STYLE_BG)
            main_frame.pack(expand=True, fill="both", padx=20, pady=20)
            
            # Label istruzioni
            instructions = tk.Label(
                main_frame,
                text="Posiziona il QR Code davanti alla fotocamera",
                font=("Helvetica", 18, "bold"),
                bg=STYLE_BG,
                fg=STYLE_FG
            )
            instructions.pack(pady=20)
            
            # Frame per il feed della fotocamera
            camera_frame = tk.Frame(
                main_frame,
                bg=STYLE_BG,
                width=feed_width,
                height=feed_height,
            )
            camera_frame.pack(pady=10)
            
            # Label per il feed della fotocamera
            camera_label = tk.Label(camera_frame)
            camera_label.pack()

            status_label = tk.Label(
                main_frame,
                text="Fotocamera attiva — in attesa di un QR valido",
                bg=STYLE_BG,
                fg=STYLE_FG,
            )
            status_label.pack(pady=5)
            
            center_window(camera_window)
            return camera_window, camera_label, status_label, feed_width, feed_height

        def aggiorna_camera(
            cap, camera_label, camera_window, status_label, feed_width, feed_height
        ):
            """Aggiorna il feed della fotocamera e cerca QR codes"""
            if not camera_window.winfo_exists():
                cap.release()
                return
            if not cap.isOpened():
                camera_window.destroy()
                messagebox.showerror("Errore", "La fotocamera si è disconnessa.")
                return

            ret, frame = cap.read()
            if ret:
                # Ridimensiona il frame mantenendo le proporzioni
                frame = cv2.resize(frame, (feed_width, feed_height))
                
                # Converti il frame per Tkinter
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                imgtk = ImageTk.PhotoImage(image=img)
                camera_label.imgtk = imgtk
                camera_label.configure(image=imgtk)
                
                # Cerca QR code
                contenuto_qr = leggi_qr_code(frame)
                if contenuto_qr:
                    status_label.configure(text="QR rilevato, verifica in corso…")
                    cap.release()
                    camera_window.destroy()
                    user_id = verify_token(contenuto_qr)
                    user = self.database.get_user(user_id) if user_id else None
                    if user is None:
                        messagebox.showerror(
                            "QR non valido", "Il codice non è autentico o non è più registrato."
                        )
                    else:
                        mostra_finestra_motivazione(user)
                    return
                
                camera_window.after(
                    20,
                    lambda: aggiorna_camera(
                        cap, camera_label, camera_window, status_label, feed_width, feed_height
                    ),
                )
            else:
                status_label.configure(text="Impossibile leggere il video dalla fotocamera")
                camera_window.after(
                    250,
                    lambda: aggiorna_camera(
                        cap, camera_label, camera_window, status_label, feed_width, feed_height
                    ),
                )

        # Inizializza la fotocamera
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Errore", "Impossibile accedere alla fotocamera.")
            return

        # Configura e mostra la finestra della fotocamera
        camera_window, camera_label, status_label, feed_width, feed_height = setup_camera_window()
        
        # Avvia l'aggiornamento della fotocamera
        aggiorna_camera(
            cap, camera_label, camera_window, status_label, feed_width, feed_height
        )
        
        def on_closing():
            """Gestisce la chiusura pulita della finestra della fotocamera"""
            cap.release()
            camera_window.destroy()
        
        camera_window.protocol("WM_DELETE_WINDOW", on_closing)

def run_interface():
    root = tk.Tk()
    FastChargeInterface(root)
    center_window(root)
    root.mainloop()

if __name__ == "__main__":
    run_interface()
