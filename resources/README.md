# Risorse e dati locali

- `images/fce_logo.png`: background usato dall'interfaccia.
- `fonts/`: font distribuiti con l'applicazione.
- `qr_codes/`: QR generati a runtime; il contenuto è ignorato da Git.
- `log/`: posizione del vecchio log, conservata solo per la migrazione.
- `fastcharge.db`: database locale, ignorato da Git.
- `qr-signing.key`: chiave locale HMAC, ignorata da Git.
- `libs/` e le immagini non referenziate sono asset legacy conservati per
  compatibilità con distribuzioni precedenti.

I dati runtime non devono essere aggiunti al repository.
