"""
Module Name: generaqrcode
Description: This module generates and saves the qrcode associated to the user
Author: Francesco Zompanti
"""
import qrcode
from fastcharge.paths import qr_code_dir


def genera_qr_code(qr_data, file_id, save_path=None):
    """
    Genera un QR code in fase di registrazione utente
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    if save_path:
        # Verifica che la cartella esista, altrimenti la crea
        output_dir = qr_code_dir()
        output_dir.mkdir(parents=True, exist_ok=True)

        # L'identificatore opaco evita nomi file contenenti dati personali.
        file_name = f"{file_id}.png"
        full_path = output_dir / file_name

        # Salva l'immagine come file PNG
        img.save(full_path)

    return img
