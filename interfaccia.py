import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from generaqrcode import genera_qr_code
import cv2
from pyzbar.pyzbar import decode
from styles import *
from utils import center_window

class FastChargeInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("FastCharge")
        self.root.geometry("1280x720")
        self.root.resizable(False, False)

        self.setup_background()
        self.setup_widgets()
        self.mostra_menu_principale()

    def setup_background(self):
        background_image = Image.open(BACKGROUND_LOGO)
        background_image = background_image.resize((1280, 720))
        self.background_photo = ImageTk.PhotoImage(background_image)

        self.canvas = tk.Canvas(self.root, width=1280, height=720)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(640, 360, image=self.background_photo, anchor="center")

    def setup_widgets(self):
        self.label_nome = tk.Label(self.root, text="Nome:", font=STYLE_FONT, bg=STYLE_BG, fg=STYLE_FG)
        self.entry_nome = tk.Entry(self.root, bg=STYLE_ENTRY_BG, fg=STYLE_ENTRY_FG, font=STYLE_FONT)

        self.label_cognome = tk.Label(self.root, text="Cognome:", font=STYLE_FONT, bg=STYLE_BG, fg=STYLE_FG)
        self.entry_cognome = tk.Entry(self.root, bg=STYLE_ENTRY_BG, fg=STYLE_ENTRY_FG, font=STYLE_FONT)

        self.label_email = tk.Label(self.root, text="Email:", font=STYLE_FONT, bg=STYLE_BG, fg=STYLE_FG)
        self.entry_email = tk.Entry(self.root, bg=STYLE_ENTRY_BG, fg=STYLE_ENTRY_FG, font=STYLE_FONT)

        self.btn_submit = tk.Button(self.root, text="Conferma Registrazione", 
                               command=self.registra_utente, 
                               font=STYLE_FONT, bg=STYLE_BUTTON_BG, fg=STYLE_BUTTON_FG, width=20)

        self.btn_registrati = tk.Button(self.root, text="Registrati", command=self.show_registration_form, 
                                   font=STYLE_FONT, bg=STYLE_BUTTON_BG, fg=STYLE_BUTTON_FG, width=20)
        self.btn_accedi = tk.Button(self.root, text="Accedi", command=self.accedi, 
                               font=STYLE_FONT, bg=STYLE_BUTTON_BG, fg=STYLE_BUTTON_FG, width=20)

        self.author_label = tk.Label(self.root, text="Made by Francesco Zompanti", 
                                font=('Helvetica', 14), fg=STYLE_FG, bg=STYLE_BG)

    def registra_utente(self):
        nome = self.entry_nome.get()
        cognome = self.entry_cognome.get()
        email = self.entry_email.get()

        if nome and cognome and email:
            qr_img = genera_qr_code(nome, cognome, email, save_path=True)
            qr_img = qr_img.resize((300, 300))
            qr_photo = ImageTk.PhotoImage(qr_img)
            
            qr_window = tk.Toplevel(self.root)
            qr_window.title("QR Code")
            qr_window.geometry("400x550")
            qr_window.resizable(False, False)
            
            qr_label = tk.Label(qr_window, image=qr_photo)
            qr_label.image = qr_photo
            qr_label.pack(padx=20, pady=20)
            
            msg_label1 = tk.Label(qr_window, text="Salva sul tuo telefono questo QR Code per accedere", 
                                  font=('Helvetica', 14), wraplength=350)
            msg_label1.pack(pady=10)
            
            close_button = tk.Button(qr_window, text="Chiudi", command=qr_window.destroy, 
                                     font=('Helvetica', 14), bg=STYLE_BUTTON_BG, fg=STYLE_BUTTON_FG)
            close_button.pack(pady=20)
            
            self.entry_nome.delete(0, tk.END)
            self.entry_cognome.delete(0, tk.END)
            self.entry_email.delete(0, tk.END)
            
            self.torna_al_menu_principale()
        else:
            messagebox.showwarning("Errore", "Compila tutti i campi.")

    def show_registration_form(self):
        self.nascondi_menu_principale()
        
        self.label_nome.place(x=440, y=260)
        self.entry_nome.place(x=640, y=260, width=300)
        self.label_cognome.place(x=440, y=320)
        self.entry_cognome.place(x=640, y=320, width=300)
        self.label_email.place(x=440, y=380)
        self.entry_email.place(x=640, y=380, width=300)
        self.btn_submit.place(x=540, y=460)
        self.author_label.place(x=20, y=680)

    def torna_al_menu_principale(self):
        self.label_nome.place_forget()
        self.entry_nome.place_forget()
        self.label_cognome.place_forget()
        self.entry_cognome.place_forget()
        self.label_email.place_forget()
        self.entry_email.place_forget()
        self.btn_submit.place_forget()

        self.mostra_menu_principale()

    def accedi(self):
        def leggi_qr_code(frame):
            qr_codes = decode(frame)
            for qr_code in qr_codes:
                dati_qr = qr_code.data.decode('utf-8')
                return dati_qr
            return None

        def contenuto_presente_nel_file(contenuto, percorso_file):
            try:
                with open(percorso_file, "r") as file:
                    dati_salvati = file.read()
                    if contenuto in dati_salvati:
                        return True
            except FileNotFoundError:
                return False
            return False

        LOG_FILE_PATH = "resources/log/accessi.txt"

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
                if contenuto_presente_nel_file(contenuto_qr, LOG_FILE_PATH):
                    messagebox.showinfo("Accesso", "Accesso gia' effettuato!")
                else:
                    with open(LOG_FILE_PATH, "a") as file:
                        file.write(contenuto_qr + "\n")
                    messagebox.showinfo("Accesso", "Accesso effettuato!")
                break

            cv2.imshow('Scansiona il QR Code', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def nascondi_menu_principale(self):
        self.btn_registrati.place_forget()
        self.btn_accedi.place_forget()

    def mostra_menu_principale(self):
        self.btn_registrati.place(x=540, y=300)
        self.btn_accedi.place(x=540, y=380)
        self.author_label.place(x=20, y=680)

def run_interface():
    root = tk.Tk()
    app = FastChargeInterface(root)
    center_window(root)
    root.mainloop()

if __name__ == "__main__":
    run_interface()