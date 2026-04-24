@echo off
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Environnement virtuel introuvable.
    echo Assure-toi qu'un dossier .venv existe dans le meme dossier que ce fichier.
    pause
    exit /b 1
)

echo Lancement de Todo-Engine...
start "" http://localhost:8050
.venv\Scripts\python.exe app.py