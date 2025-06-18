#!/bin/bash
# Das script ist dafür da dass wir keine probleme mit versionen bekommen und alle auf dem gleichen stand sind

# ANPASSEN --- FUEGT HIER EUER PROJEKT-PFAD EIN !!!
PROJECT_DIR="$HOME/Documents/Projektwoche1/PiCarControl"

cd "$PROJECT_DIR" || { echo "Projektordner nicht gefunden: $PROJECT_DIR"; exit 1; }

echo "System aktualisieren..."
sudo apt update
sudo apt install -y python3 python3-venv

# Virtuelle Umgebung erstellen, falls nicht vorhanden
if [ ! -d "venv" ]; then
    echo "Virtuelle Umgebung wird erstellt..."
    python3 -m venv venv
fi

# venv aktivieren
source venv/bin/activate

echo "Python-Pakete werden installiert..."
pip install --upgrade pip
pip install dash plotly pandas

echo "✅ Setup abgeschlossen. Du kannst jetzt loslegen!"
