"""
launch.py — Lanceur de l'application Todo-Engine.
Ouvre automatiquement le navigateur une fois le serveur prêt.
Appelé par lancer.bat, ne pas exécuter directement en développement.
"""

import threading
import time
import webbrowser

HOST = "localhost"
PORT = 8050
URL = f"http://{HOST}:{PORT}"


def _open_browser():
    """Attend que le serveur soit prêt puis ouvre le navigateur."""
    time.sleep(1.5)
    webbrowser.open(URL)


if __name__ == "__main__":
    threading.Thread(target=_open_browser, daemon=True).start()

    # Import tardif pour que le thread soit lancé avant le démarrage de Dash
    from app import app

    app.run(host=HOST, port=PORT, debug=False)
