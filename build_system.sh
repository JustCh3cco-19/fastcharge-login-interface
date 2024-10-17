#!/bin/bash

# Nome dell'environment che vuoi attivare
ENV_NAME="FastCharge"
SYSTEM_NAME="Accessi FCE"

# Controlla se l'environment è attivo
if [ "$CONDA_DEFAULT_ENV" != "$ENV_NAME" ]; then
    echo "Attivando l'environment $ENV_NAME..."
    conda activate $ENV_NAME
else
    echo "L'environment $ENV_NAME è già attivo."
fi

echo "Starting build for $SYSTEM_NAME"

pyinstaller --onefile --add-data "resources:resources" --hidden-import="PIL._tkinter
_finder" main.py