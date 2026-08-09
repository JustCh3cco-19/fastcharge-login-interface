# Architettura

FastCharge è organizzato in livelli con dipendenze orientate verso il dominio:

```text
main.py / fastcharge.__main__
              │
              ▼
       application.py
        ┌─────┴─────┐
        ▼           ▼
 ui/interface.py  services/notifier.py
        │           │
        ├─────┬─────┤
        ▼     ▼     ▼
   validation security database
```

- `application.py` avvia GUI e monitor email.
- `ui/` contiene esclusivamente presentazione e widget Tkinter.
- `services/` contiene integrazioni e processi applicativi.
- `database.py` è l'unico punto di accesso a SQLite.
- `security.py` gestisce token QR e chiave HMAC.
- `settings.py` e `paths.py` isolano configurazione e filesystem.

## Flusso dei dati

1. La GUI valida i dati e registra utente/accesso tramite `Database`.
2. `security` genera un token firmato contenente solo l'identificatore opaco.
3. `services.qr` converte il token in immagine.
4. Il monitor legge gli accessi non notificati da SQLite.
5. Solo dopo un invio SMTP riuscito marca il batch come notificato.

I moduli UI non aprono file o connessioni SMTP direttamente. I servizi non
dipendono da Tkinter, quindi possono essere testati senza interfaccia grafica.
