"""
Module Name: interfaccia
Description: This module creates the dashboard in order to make the login or the signup
Author: Francesco Zompanti
"""
import os
import sys
import tkinter as tk
from tkinter import messagebox
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

		self.setup_background()
		self.setup_widgets()
		self.mostra_menu_principale()

	def setup_background(self):
		"""
		Imposta l'immagine di sfondo ad una certa risoluzione
		"""
		# Usa resource_path per ottenere il percorso dell'immagine del logo
		background_path = resource_path('resources/images/fce_logo.png')

		# Carica e ridimensiona l'immagine di sfondo
		self.background_image = Image.open(background_path)
		self.background_image = self.background_image.resize((1280, 720))  # Ridimensiona l'immagine

		# Converti l'immagine in un formato compatibile con Tkinter
		self.background_photo = ImageTk.PhotoImage(self.background_image)

		# Crea un canvas per mostrare l'immagine di sfondo
		self.canvas = tk.Canvas(self.root, width=1280, height=720)
		self.canvas.pack(fill="both", expand=True)

		# Imposta l'immagine di sfondo al centro del canvas
		self.canvas.create_image(640, 360, image=self.background_photo, anchor="center")

	def setup_widgets(self):
		"""
		Crea i vari widgets usati in fase di registrazione ed accesso al sistema
		"""
		self.label_nome_cognome = tk.Label(self.root, text="Nome e Cognome",
									 font=STYLE_FONT, bg=STYLE_BG, fg=STYLE_FG)
		self.entry_nome_cognome = tk.Entry(self.root, bg=STYLE_ENTRY_BG,
									 fg=STYLE_ENTRY_FG, font=STYLE_FONT)

		self.label_email = tk.Label(self.root, text="Email", font=STYLE_FONT, bg=STYLE_BG, fg=STYLE_FG)
		self.entry_email = tk.Entry(self.root, bg=STYLE_ENTRY_BG, fg=STYLE_ENTRY_FG, font=STYLE_FONT)

		self.label_motivazione_visita = tk.Label(self.root, text="Motivazione Visita",
										   font=STYLE_FONT, bg=STYLE_BG, fg=STYLE_FG)
		self.entry_motivazione_visita = tk.Entry(self.root, bg=STYLE_ENTRY_BG,
										   fg=STYLE_ENTRY_FG, font=STYLE_FONT)

		self.btn_submit = tk.Button(self.root, text="Conferma Registrazione",
							   command=self.registra_utente,
							   font=STYLE_FONT, bg=STYLE_BUTTON_BG, fg=STYLE_BUTTON_FG, width=20)

		self.btn_back = tk.Button(self.root, text="Indietro",
							   command=self.torna_al_menu_principale,
							   font=STYLE_FONT, bg=STYLE_BUTTON_BG, fg=STYLE_BUTTON_FG, width=20)

		self.btn_registrati = tk.Button(self.root, text="Registrati", command=self.show_registration_form,
								   font=STYLE_FONT, bg=STYLE_BUTTON_BG, fg=STYLE_BUTTON_FG, width=20)

		self.btn_accedi = tk.Button(self.root, text="Accedi", command=self.accedi,
							   font=STYLE_FONT, bg=STYLE_BUTTON_BG, fg=STYLE_BUTTON_FG, width=20)

		self.author_label = tk.Label(self.root, text="Credits: Francesco Zompanti",
								font=STYLE_FONT, fg=STYLE_CREDITS_FG, bg=STYLE_CREDITS_BG)

	def registra_utente(self):
		"""
		Funzione che implementa la registrazione dell'utente
		"""
		nome_cognome = self.entry_nome_cognome.get()
		email = self.entry_email.get()
		motivazione_visita = self.entry_motivazione_visita.get()

		if nome_cognome and email:
			# Usa resource_path per ottenere il percorso corretto
			log_file_path = os.path.join(os.getcwd(), "resources", "log", "accessi.txt")

			# Creazione automatica della cartella se non esiste
			os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

			print("Log Accessi al percorso: ", log_file_path)

			# Scrittura dei dati nel file
			with open(log_file_path, "a", encoding='utf-8') as file:
				file.write(f"{nome_cognome} - {email},\nMotivazione visita: {motivazione_visita}\n")

			# Genera e mostra il QR Code (resto del codice invariato)
			qr_img = genera_qr_code(nome_cognome, email, save_path=True)
			qr_img = qr_img.resize((300, 300))
			qr_photo = ImageTk.PhotoImage(qr_img)

			qr_window = tk.Toplevel(self.root)
			qr_window.title("QR Code")
			qr_window.geometry("400x550")
			qr_window.resizable(False, False)

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

			close_button = tk.Button(qr_window, text="Chiudi", command=qr_window.destroy,
									 font=('Helvetica', 14), bg=STYLE_BUTTON_BG, fg=STYLE_BUTTON_FG)
			close_button.pack(pady=20)

			self.entry_nome_cognome.delete(0, tk.END)
			# self.entry_cognome.delete(0, tk.END)
			self.entry_email.delete(0, tk.END)
			self.entry_motivazione_visita.delete(0, tk.END)

			self.torna_al_menu_principale()
		else:
			messagebox.showwarning("Errore", "Compila tutti i campi.")


	def show_registration_form(self):
		"""
		Mostra la schermata di registrazione del profilo
		"""
		self.nascondi_menu_principale()

		# Resetta i campi di input
		self.entry_nome_cognome.delete(0, tk.END)
		#self.entry_cognome.delete(0, tk.END)
		self.entry_email.delete(0, tk.END)
		self.entry_motivazione_visita.delete(0, tk.END)

		self.label_nome_cognome.place(x=440, y=260)
		self.entry_nome_cognome.place(x=640, y=260, width=300)
		# self.label_cognome.place(x=440, y=320)
		# self.entry_cognome.place(x=640, y=320, width=300)
		self.label_email.place(x=440, y=380)
		self.entry_email.place(x=640, y=380, width=300)
		self.label_motivazione_visita.place(x=440, y=440)
		self.entry_motivazione_visita.place(x=640, y=440, width=300)
		self.btn_submit.place(x=540, y=480)
		self.btn_back.place(x=540, y=540)
		self.author_label.place(x=20, y=680)

	def torna_al_menu_principale(self):
		"""
		Funzione per tornare al menu principale dalla registrazione
		"""
		self.label_nome_cognome.place_forget()
		self.entry_nome_cognome.place_forget()
		# self.label_cognome.place_forget()
		# self.entry_cognome.place_forget()
		self.label_email.place_forget()
		self.entry_email.place_forget()
		self.btn_submit.place_forget()
		self.btn_back.place_forget()
		self.label_motivazione_visita.place_forget()
		self.entry_motivazione_visita.place_forget()

		self.mostra_menu_principale()

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
					if contenuto in dati_salvati:
						return True
			except FileNotFoundError:
				return False
			return False

		log_file_path = "resources/log/accessi.txt"

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
				if contenuto_presente_nel_file(contenuto_qr, log_file_path):
					messagebox.showinfo("Accesso", "Accesso gia' effettuato!")
				else:
					with open(log_file_path, "a", encoding='utf-8') as file:
						file.write(contenuto_qr + "\n")
					messagebox.showinfo("Accesso", "Accesso effettuato!")
				break

			cv2.imshow('Scansiona il QR Code', frame)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

		cap.release()
		cv2.destroyAllWindows()

	def nascondi_menu_principale(self):
		"""
		Nascondi il menu principale
		"""
		self.btn_registrati.place_forget()
		self.btn_accedi.place_forget()

	def mostra_menu_principale(self):
		"""
		Mostra menu principale
		"""
		self.btn_registrati.place(x=540, y=300)
		self.btn_accedi.place(x=540, y=380)
		self.author_label.place(x=20, y=680)

def run_interface():
	"""
	Avvia l'interfaccia
	"""
	root = tk.Tk()
	app = FastChargeInterface(root)
	center_window(root)
	root.mainloop()

if __name__ == "__main__":
	run_interface()
