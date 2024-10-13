import tkinter as tk
from tkinter import messagebox, font
from PIL import Image, ImageTk
import os

LOG_FILE_PATH = "resources/log/accessi.txt"
BACKGROUND_LOGO = "resources/images/fast_charge_logo.png"

def registra_accesso():
    nome = entry_nome.get()
    cognome = entry_cognome.get()
    email = entry_email.get()
    
    if nome and cognome and email:
        with open(LOG_FILE_PATH, "a") as log_file:
            log_file.write(f"{nome} {cognome} - {email}\n")
        
        messagebox.showinfo("", "Accesso effettuato")
        entry_nome.delete(0, tk.END)
        entry_cognome.delete(0, tk.END)
        entry_email.delete(0, tk.END)
    else:
        messagebox.showerror("Errore", "Compila tutti i campi")

def setup_background():
    global background_image
    canvas_width = root.winfo_width()
    canvas_height = root.winfo_height()

    if canvas_width > 0 and canvas_height > 0:
        resized_image = background.copy().resize((canvas_width, canvas_height), Image.LANCZOS)
        background_image = ImageTk.PhotoImage(resized_image)
        canvas.create_image(0, 0, anchor=tk.NW, image=background_image)
    else:
        root.after(100, setup_background)

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

# Configurazione interfaccia
root = tk.Tk()
root.title("Accedi a FastCharge")
root.configure(bg='black')
root.resizable(False, False)  # Blocca il ridimensionamento della finestra

# Centra la finestra sullo schermo
window_width = 800
window_height = 600
center_window(root, window_width, window_height)

text_font = font.Font(family="Helvetica", size=12)
text_bold_font = font.Font(family="Helvetica", size=12, weight="bold")

# Canvas per l'immagine di sfondo
canvas = tk.Canvas(root, highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)

# Carica l'immagine di sfondo
try:
    background = Image.open(BACKGROUND_LOGO)
except FileNotFoundError:
    print("Immagine di sfondo non trovata. L'interfaccia verrà mostrata senza sfondo.")
    background = Image.new('RGB', (window_width, window_height), color='black')

# Frame per i campi di input
input_frame = tk.Frame(root, bg='black')
input_frame.place(relx=0.5, rely=0.5, anchor='center')

# Stile per le etichette e i campi di input
label_style = {'bg': 'black', 'fg': 'orange', 'font': text_bold_font, 'padx': 5, 'pady': 2}
entry_style = {'font': text_font, 'width': 30, 'bg': 'black', 'fg': 'white', 'insertbackground': 'white'}

# Campi Nome, Cognome e Email
tk.Label(input_frame, text="Nome:", **label_style).grid(row=0, column=0, sticky='w', pady=(0, 5))
entry_nome = tk.Entry(input_frame, **entry_style)
entry_nome.grid(row=1, column=0, pady=(0, 10))

tk.Label(input_frame, text="Cognome:", **label_style).grid(row=2, column=0, sticky='w', pady=(0, 5))
entry_cognome = tk.Entry(input_frame, **entry_style)
entry_cognome.grid(row=3, column=0, pady=(0, 10))

tk.Label(input_frame, text="Email:", **label_style).grid(row=4, column=0, sticky='w', pady=(0, 5))
entry_email = tk.Entry(input_frame, **entry_style)
entry_email.grid(row=5, column=0, pady=(0, 10))

# Bottone Invia
btn_invia = tk.Button(input_frame, text="Invia", command=registra_accesso, font=text_bold_font, bg='orange', fg='black', padx=20, pady=10)
btn_invia.grid(row=6, column=0, pady=(20, 0), sticky='ew')  # Modificato per centrare il bottone

# Testo "Made by Francesco Zompanti"
credits_label = tk.Label(root, text="Made by Francesco Zompanti", bg='black', fg='white', font=text_font)
credits_label.place(relx=0.5, rely=0.95, anchor='center')

if __name__ == "__main__":
    root.update_idletasks()
    root.after(100, setup_background)
    root.mainloop()