import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import qrcode

BACKGROUND_LOGO = "resources/images/fast_charge_logo.png"
QR_CODE_DIR = "resources/qr_codes"

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

# Funzione per generare il QR code
def genera_qr_code(nome, cognome, email):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr_data = f"{nome} {cognome} - {email}"
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill='black', back_color='white')
    return img

# Funzione per registrare l'accesso e mostrare il QR code
def registra_accesso():
    nome = entry_nome.get()
    cognome = entry_cognome.get()
    email = entry_email.get()

    if nome and cognome and email:
        # Genera QR code
        qr_img = genera_qr_code(nome, cognome, email)
        
        # Converti l'immagine QR in formato compatibile con tkinter
        qr_photo = ImageTk.PhotoImage(qr_img)
        
        # Crea una nuova finestra per mostrare il QR code
        qr_window = tk.Toplevel(root)
        qr_window.title("QR Code")
        qr_window.resizable(False, False)  # Impedisce il ridimensionamento

        
        # Mostra il QR code
        qr_label = tk.Label(qr_window, image=qr_photo)
        qr_label.image = qr_photo  # Mantieni un riferimento!
        qr_label.pack(padx=10, pady=10)
        
        # Aggiungi un messaggio
        msg_label = tk.Label(qr_window, text="Salva sul tuo telefono questo QR Code per i futuri accessi.", font=('Helvetica', 12))
        msg_label.pack(pady=10)
        
        # Aggiungi un pulsante per chiudere la finestra
        close_button = tk.Button(qr_window, text="Chiudi", command=qr_window.destroy)
        close_button.pack(pady=10)
        
        # Dopo la registrazione, ritorna al menu principale
        torna_al_menu_principale()
    else:
        messagebox.showwarning("Errore", "Compila tutti i campi.")

def show_registration_form():
    nascondi_menu_principale()
    
    label_nome.pack()
    entry_nome.pack()
    label_cognome.pack()
    entry_cognome.pack()
    label_email.pack()
    entry_email.pack()
    btn_submit.pack()

# Funzione per accedere (placeholder)
def accedi():
    messagebox.showinfo("Accesso", "Funzionalità di accesso non implementata.")

# Funzione per tornare al menu principale
def torna_al_menu_principale():
    # Nascondi i campi di registrazione e mostra il menu principale
    label_nome.pack_forget()
    entry_nome.pack_forget()
    label_cognome.pack_forget()
    entry_cognome.pack_forget()
    label_email.pack_forget()
    entry_email.pack_forget()
    btn_submit.pack_forget()

    mostra_menu_principale()

# Funzione per nascondere il menu principale
def nascondi_menu_principale():
    btn_registrati.pack_forget()
    btn_accedi.pack_forget()

# Funzione per mostrare il menu principale
def mostra_menu_principale():
    btn_registrati.pack(pady=10)
    btn_accedi.pack(pady=10)

# Creazione della finestra principale
root = tk.Tk()
root.title("FastCharge")
root.resizable(False, False)  # Impedisce il ridimensionamento della finestra principale

# Carica lo sfondo
background_image = Image.open(BACKGROUND_LOGO)
background_photo = ImageTk.PhotoImage(background_image)

canvas = tk.Canvas(root, width=background_image.width, height=background_image.height)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=background_photo, anchor="nw")

# Cambiare lo stile dei campi e dei pulsanti
style_font = ('Helvetica', 14, 'bold')
style_bg = '#000000'
style_fg = '#FFA500'
style_entry_bg = '#2E2E2E'
style_entry_fg = '#FFFFFF'
style_button_bg = '#FFA500'
style_button_fg = '#000000'

root.configure(bg=style_bg)

# Campi per la registrazione (inizialmente nascosti)
label_nome = tk.Label(root, text="Nome:", font=style_font, bg=style_bg, fg=style_fg)
entry_nome = tk.Entry(root, bg=style_entry_bg, fg=style_entry_fg, font=style_font)
label_cognome = tk.Label(root, text="Cognome:", font=style_font, bg=style_bg, fg=style_fg)
entry_cognome = tk.Entry(root, bg=style_entry_bg, fg=style_entry_fg, font=style_font)
label_email = tk.Label(root, text="Email:", font=style_font, bg=style_bg, fg=style_fg)
entry_email = tk.Entry(root, bg=style_entry_bg, fg=style_entry_fg, font=style_font)

btn_submit = tk.Button(root, text="Conferma Registrazione", command=registra_accesso, font=style_font, bg=style_button_bg, fg=style_button_fg)

# Pulsanti iniziali
btn_registrati = tk.Button(root, text="Registrati", command=show_registration_form, font=style_font, bg=style_button_bg, fg=style_button_fg)
btn_accedi = tk.Button(root, text="Accedi", command=accedi, font=style_font, bg=style_button_bg, fg=style_button_fg)

# Mostra il menu principale all'avvio
mostra_menu_principale()

if __name__ == "__main__":
    center_window(root)
    root.mainloop()