#!/bin/bash

# Nome del sistema
SYSTEM_NAME="Accessi FCE"
BUILD_FOLDER="build/"
BUILD_FILE="AccessiFCE.spec"
EXECUTABLE_FOLDER="dist/"
EXECUTABLE_NAME="AccessiFCE"
ENVIRONMENT="../../../../FastCharge/bin/activate"

# Activate environment
if source "$ENVIRONMENT";then
    echo "Environment activated successfully."
else
    source "$ENVIRONMENT"
fi


# Torna nel main
cd ..
echo "Starting build for $SYSTEM_NAME"

# Esegui pyinstaller e controlla se ha successo
if pyinstaller --onefile --add-data "resources:resources" --hidden-import="PIL._tkinter_finder" --name "$EXECUTABLE_NAME" main.py; then
    # Controlla se l'eseguibile è stato creato
    if [ -f "$EXECUTABLE_FOLDER/$EXECUTABLE_NAME" ]; then
        # Sposta l'eseguibile fuori dalla cartella src
        echo "$SYSTEM_NAME build successfully."
        mv "$EXECUTABLE_FOLDER/$EXECUTABLE_NAME" .
    else
        echo "Error: Executable not found."
    fi
else
    echo "Error while building $SYSTEM_NAME."
fi

# Rimuovi le cartelle build, file .spec e cartella dist
rm -rf "$BUILD_FOLDER" "$BUILD_FILE" "$EXECUTABLE_FOLDER"
