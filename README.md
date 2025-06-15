# FastCharge Login Interface

> **Email notifications for new login entries, sent every 15 minutes – with Gmail or Aruba support.**

A Python-based interface that periodically checks for user logins and sends notification emails every 15 minutes—only if new logins are detected in `accessi.txt`.

---

## 🛠️ Installation

```bash
git clone https://github.com/JustCh3cco-19/fastcharge-login-interface.git
cd fastcharge-login-interface
pip install -r requirements.txt
```

---

## ⚙️ Configuration

Create a `.env` file in the root directory with the appropriate settings.

### Gmail Method

```dotenv
EMAIL_APP_PASSWORD=<your_app_password>
SENDER_EMAIL=<your_email@gmail.com>
RECEIVER_EMAIL=<recipient_email@gmail.com>
```

### Aruba Method

1. In `monitoraccessi.py`, **comment out** the Gmail section and **uncomment** the Aruba section.  
2. Then set in `.env`:

```dotenv
SENDER_EMAIL=<your_email@aruba.it>
SENDER_PASSWORD=<your_password>
RECEIVER_EMAIL=<recipient_email@example.com>
```

---

## ▶️ Run

```bash
python3 main.py
```

The script checks `accessi.txt` every 15 minutes and sends a summary email if new login entries are found.

---

## 🗂️ Project Structure

- `main.py` – entry point  
- `monitoraccessi.py` – handles file monitoring and email notifications  
- `interfaccia.py`, `styles.py`, `generaqrcode.py` – GUI and QR code generation  
- `utils.py` – utility functions  
- `requirements.txt` – Python dependencies

---

## 📦 Features

- Monitors `accessi.txt` every 15 minutes
- Sends emails only when new entries are found
- Supports Gmail (via app password) and Aruba email accounts
