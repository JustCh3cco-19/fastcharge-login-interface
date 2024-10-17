#!/bin/bash

# Nome dell'environment che vuoi attivare
ENV_NAME="FastCharge"
SYSTEM_NAME="Accessi FCE"
BUILD_FOLDER="build/"
BUILD_FILE="AccessiFCE.spec"
EXECUTABLE_FOLDER="dist/"
EXECUTABLE_NAME="dist/AccessiFCE"

# Controlla se l'environment è attivo
if [ "$CONDA_DEFAULT_ENV" != "$ENV_NAME" ]; then
    echo "Activating $ENV_NAME environment."
    conda activate $ENV_NAME
else
    echo "$ENV_NAME environment is already active."
fi

echo "Starting build for $SYSTEM_NAME"

# Esegui pyinstaller e controlla se ha successo
if pyinstaller --onefile --add-data "resources:resources" --hidden-import="PIL._tkinter_finder" --name "AccessiFCE" main.py; then
    # Sposta l'eseguibile solo se pyinstaller ha avuto successo
    mv "$EXECUTABLE_NAME" .
    echo "$SYSTEM_NAME build successfully."
else
    echo "Error while building $SYSTEM_NAME."
fi

# Rimuovi le cartelle build, file .spec e cartella dist
rm -rf "$BUILD_FOLDER" "$BUILD_FILE" "$EXECUTABLE_FOLDER"
