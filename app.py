"""
app.py — Point d'entrée de l'application Todo-Engine.
Lancement : python app.py

Structure du projet :
  app.py        ← ce fichier : init Dash + enregistrement des callbacks
  callbacks.py  ← tous les @app.callback
  cards.py      ← composants Project / Task / SubTask
  components.py ← atomes UI (badges, boutons, inputs)
  core.py       ← modèles Pydantic + méthodes métier (inchangé)
  dashboard.py  ← KPIs et graphes Plotly
  layout.py     ← shell HTML, header, onglets, modaux
  theme.py      ← couleurs, polices, styles globaux
"""

import dash
import dash_bootstrap_components as dbc

from callbacks import register_callbacks
from layout import build_layout
from theme import GOOGLE_FONTS

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, GOOGLE_FONTS],
    suppress_callback_exceptions=True,
)
app.title = "Todo-Engine"
app.layout = build_layout()

register_callbacks(app)

if __name__ == "__main__":
    app.run()
