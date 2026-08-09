# Creazione dell'eseguibile

## Linux

```bash
pyinstaller --onefile --collect-all PIL --add-data "resources:resources" --hidden-import="PIL._tkinter_finder" --name "AccessiFCE" main.py
```

## Windows

```powershell
pyinstaller --onefile --collect-all PIL --add-data "resources;resources" --hidden-import="PIL._tkinter_finder" --clean --name "AccessiFCE" main.py
```

Il file `.env` deve rimanere esterno al bundle, accanto all'eseguibile. In questo
modo le credenziali SMTP non vengono incorporate nel programma distribuibile.
