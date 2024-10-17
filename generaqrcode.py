"""
Module Name: generaqrcode
Description: This module generates and saves the qrcode associated to the user
Author: Francesco Zompanti
"""
import os
import qrcode

QR_CODE_DIR = "resources/qr_codes"

def genera_qr_code(nome_cognome, email, save_path=None):
    """
    Genera un QR code in fase di registrazione utente
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr_data = f"{nome_cognome} - {email}"
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    if save_path:
        # Verifica che la cartella esista, altrimenti la crea
        if not os.path.exists(QR_CODE_DIR):
            os.makedirs(QR_CODE_DIR)

        # Crea il nome del file QR code con nome, cognome e email
        file_name = f"{email}.png"
        full_path = os.path.join(QR_CODE_DIR, file_name)

        # Salva l'immagine come file PNG
        img.save(full_path)

    return img
