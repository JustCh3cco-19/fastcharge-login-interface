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
    window.geometry(f'{width}x{height}+{x}+{y}')

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

def registra_accesso():
    nome = entry_nome.get()
    cognome = entry_cognome.get()
    email = entry_email.get()

    if nome and cognome and email:
        qr_img = genera_qr_code(nome, cognome, email)
        qr_img = qr_img.resize((300, 300))  # Ridimensiona il QR code
        qr_photo = ImageTk.PhotoImage(qr_img)
        
        qr_window = tk.Toplevel(root)
        qr_window.title("QR Code")
        qr_window.geometry("400x550")
        qr_window.resizable(False, False)
        
        qr_label = tk.Label(qr_window, image=qr_photo)
        qr_label.image = qr_photo
        qr_label.pack(padx=20, pady=20)
        
        msg_label1 = tk.Label(qr_window, text="Salva sul tuo telefono questo QR Code per accedere al sistema.", 
                              font=('Helvetica', 14), wraplength=350)
        msg_label1.pack(pady=10)
        
        close_button = tk.Button(qr_window, text="Chiudi", command=qr_window.destroy, 
                                 font=('Helvetica', 14), bg=style_button_bg, fg=style_button_fg)
        close_button.pack(pady=20)
        
        entry_nome.delete(0, tk.END)
        entry_cognome.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        
        torna_al_menu_principale()
    else:
        messagebox.showwarning("Errore", "Compila tutti i campi.")

def show_registration_form():
    nascondi_menu_principale()
    
    label_nome.place(x=440, y=260)
    entry_nome.place(x=640, y=260, width=300)
    label_cognome.place(x=440, y=320)
    entry_cognome.place(x=640, y=320, width=300)
    label_email.place(x=440, y=380)
    entry_email.place(x=640, y=380, width=300)
    btn_submit.place(x=540, y=460)
    author_label.place(x=20, y=680)  # Place author label

def torna_al_menu_principale():
    label_nome.place_forget()
    entry_nome.place_forget()
    label_cognome.place_forget()
    entry_cognome.place_forget()
    label_email.place_forget()
    entry_email.place_forget()
    btn_submit.place_forget()

    mostra_menu_principale()

def accedi():
    messagebox.showinfo("Accesso", "Funzionalità di accesso non implementata.")

def nascondi_menu_principale():
    btn_registrati.place_forget()
    btn_accedi.place_forget()

def mostra_menu_principale():
    btn_registrati.place(x=540, y=300)
    btn_accedi.place(x=540, y=380)
    author_label.place(x=20, y=680)  # Place author label

root = tk.Tk()
root.title("FastCharge")
root.geometry("1280x720")
root.resizable(False, False)

# Carica lo sfondo e ridimensionalo per adattarlo alla finestra
background_image = Image.open(BACKGROUND_LOGO)
background_image = background_image.resize((1280, 720))
background_photo = ImageTk.PhotoImage(background_image)

canvas = tk.Canvas(root, width=1280, height=720)
canvas.pack(fill="both", expand=True)
canvas.create_image(640, 360, image=background_photo, anchor="center")

style_font = ('Helvetica', 16, 'bold')
style_bg = '#000000'
style_fg = '#FFA500'
style_entry_bg = '#2E2E2E'
style_entry_fg = '#FFFFFF'
style_button_bg = '#FFA500'
style_button_fg = '#000000'

root.configure(bg=style_bg)

label_nome = tk.Label(root, text="Nome:", font=style_font, bg=style_bg, fg=style_fg)
entry_nome = tk.Entry(root, bg=style_entry_bg, fg=style_entry_fg, font=style_font)
label_cognome = tk.Label(root, text="Cognome:", font=style_font, bg=style_bg, fg=style_fg)
entry_cognome = tk.Entry(root, bg=style_entry_bg, fg=style_entry_fg, font=style_font)
label_email = tk.Label(root, text="Email:", font=style_font, bg=style_bg, fg=style_fg)
entry_email = tk.Entry(root, bg=style_entry_bg, fg=style_entry_fg, font=style_font)

btn_submit = tk.Button(root, text="Conferma Registrazione", command=registra_accesso, font=style_font, bg=style_button_bg, fg=style_button_fg, width=20)

btn_registrati = tk.Button(root, text="Registrati", command=show_registration_form, font=style_font, bg=style_button_bg, fg=style_button_fg, width=20)
btn_accedi = tk.Button(root, text="Accedi", command=accedi, font=style_font, bg=style_button_bg, fg=style_button_fg, width=20)

# Add author label
author_label = tk.Label(root, text="Made by Francesco Zompanti", font=('Helvetica', 14), fg=style_fg, bg=style_bg)

mostra_menu_principale()

if __name__ == "__main__":
    center_window(root)
    root.mainloop()