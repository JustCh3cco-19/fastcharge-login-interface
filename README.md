# FastCharge Login Interface

Applicazione desktop Python/Tkinter per registrare visitatori, generare QR personali,
scansionare gli accessi e inviare riepiloghi periodici via email.

## Funzionalità

- archivio SQLite transazionale per utenti e accessi;
- QR opachi firmati HMAC-SHA256, senza nome o email in chiaro;
- protezione contro QR alterati e scansioni duplicate ravvicinate;
- invio SMTP configurabile a uno o più destinatari;
- accessi marcati come notificati soltanto dopo un invio riuscito;
- retry automatico e conservazione configurabile dei dati;
- importazione automatica del vecchio `resources/log/accessi.txt`;
- percorsi persistenti compatibili con PyInstaller;
- layout ridimensionabile, informativa visibile e validazione dei dati inseriti.

## Installazione

Richiede Python 3.10 o successivo e Tk.

Su Debian/Ubuntu:

```bash
sudo apt-get install python3-tk
uv sync --locked
```

Su Windows, Tk è incluso normalmente nell'installazione ufficiale di Python.

## Configurazione

Copia il modello e modifica i valori:

```bash
cp .env.example .env
```

Impostazioni principali:

```dotenv
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USE_TLS=true
SMTP_TIMEOUT=15
SENDER_EMAIL=mittente@example.com
SENDER_PASSWORD=password_o_app_password
RECEIVER_EMAIL=destinatario@example.com,altro@example.com
```

`EMAIL_APP_PASSWORD` è accettata come alias retrocompatibile di
`SENDER_PASSWORD`. Non inserire mai `.env` nel repository o nell'eseguibile.

Altre impostazioni:

- `EMAIL_INTERVAL_SECONDS`: intervallo normale, predefinito 900;
- `EMAIL_RETRY_SECONDS`: pausa tra tentativi falliti, predefinita 60;
- `MAX_BATCH_ENTRIES`: invio anticipato al raggiungimento della soglia;
- `DATA_RETENTION_DAYS`: eliminazione degli accessi già notificati, predefinita 90;
- `USER_RETENTION_DAYS`: eliminazione degli utenti rimasti senza accessi, predefinita 365;
- `FASTCHARGE_DATA_DIR`: directory alternativa per database, QR e chiave;
- `FASTCHARGE_CONFIG_FILE`: posizione alternativa del file `.env`;
- `QR_SIGNING_SECRET`: chiave esplicita per installazioni che devono condividere QR.

Senza `QR_SIGNING_SECRET`, al primo avvio viene generata una chiave locale con
permessi limitati. Va conservata insieme ai dati: perdendola, i QR già emessi non
saranno più verificabili.

## Avvio

```bash
python3 -m fastcharge
```

I dati sono salvati in `resources/fastcharge.db` durante lo sviluppo e nella
directory `data` accanto all'eseguibile quando l'app è pacchettizzata.

Se esiste un vecchio log testuale, i record riconoscibili vengono importati una sola
volta e il file viene rinominato con suffisso `.migrated`.

## Test e qualità

```bash
uv run python -m unittest discover -s tests -p 'test_*.py' -v
uv run ruff check .
```

La workflow GitHub Actions esegue entrambi i controlli a ogni push e pull request.
`uv.lock` contiene le versioni esatte usate localmente e in CI. Dopo aver modificato
le dipendenze in `pyproject.toml`, rigeneralo con `uv lock`.

## Build

Consulta [docs/build.md](docs/build.md). Il file `.env`
deve restare esterno al bundle, accanto all'eseguibile.

Per i confini tra moduli e il flusso dei dati consulta
[docs/architecture.md](docs/architecture.md).

## Struttura della repository

```text
fastcharge-login-interface/
├── fastcharge/
│   ├── application.py       # ciclo di vita dell'applicazione
│   ├── database.py          # persistenza SQLite e migrazioni
│   ├── paths.py             # percorsi risorse e dati persistenti
│   ├── security.py          # firma e verifica dei QR
│   ├── settings.py          # caricamento configurazione
│   ├── validation.py        # validazione degli input
│   ├── services/
│   │   ├── notifier.py      # invio email e monitor periodico
│   │   └── qr.py            # generazione immagini QR
│   └── ui/
│       ├── interface.py     # schermate e flussi Tkinter
│       ├── widgets.py       # controlli grafici riutilizzabili
│       ├── styles.py        # palette e font
│       └── window.py        # utility per le finestre
├── tests/                   # test unitari e di integrazione
├── resources/               # immagini, font e dati locali ignorati
├── docs/                    # documentazione operativa
├── main.py                  # entry point compatibile per PyInstaller
└── pyproject.toml           # metadati e configurazione tooling
```

## Privacy e sicurezza

L'app raccoglie nome, email, motivazione e orario dell'accesso. Prima dell'uso reale
è necessario fornire un'informativa privacy adatta all'organizzazione e definire una
base giuridica, i destinatari e un periodo di conservazione adeguato. I QR non
contengono dati personali, ma database, chiave e credenziali devono essere protetti
da backup e permessi del sistema operativo.
