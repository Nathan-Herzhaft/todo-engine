"""
layout.py — Shell HTML de l'application : header, onglets, modaux et écran d'accueil.
Construit le html.Div racine assigné à app.layout. Aucun callback ici.
"""

from pathlib import Path

import dash_bootstrap_components as dbc
from dash import dcc, html

from theme import (
    COLORS,
    FONT_MONO,
    FONT_SANS,
    GLOBAL_STYLE,
    TAB_SELECTED_STYLE,
    TAB_STYLE,
)

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS INTERNES — MODAUX ET ÉCRANS
# ══════════════════════════════════════════════════════════════════════════════


def _input_style(width: str = "100%") -> dict:
    return {
        "background": COLORS["card"],
        "border": f"1px solid {COLORS['border']}",
        "color": COLORS["text"],
        "fontSize": "13px",
        "borderRadius": "8px",
        "width": width,
        "padding": "8px 12px",
        "fontFamily": FONT_MONO,
        "boxSizing": "border-box",
    }


def _label(text: str) -> html.Div:
    return html.Div(
        text,
        style={
            "fontSize": "11px",
            "color": COLORS["muted"],
            "marginBottom": "6px",
            "fontFamily": FONT_SANS,
        },
    )


def _section_title(text: str) -> html.Div:
    return html.Div(
        text,
        style={
            "fontSize": "13px",
            "fontWeight": "600",
            "color": COLORS["text"],
            "marginBottom": "10px",
        },
    )


def _plain_card(children, style_extra: dict | None = None) -> html.Div:
    style = {
        "background": COLORS["card"],
        "border": f"1px solid {COLORS['border']}",
        "borderRadius": "12px",
        "padding": "20px 22px",
    }
    if style_extra:
        style.update(style_extra)
    return html.Div(children, style=style)


def _file_row(path: str) -> html.Div:
    return html.Div(
        [
            html.Span(
                Path(path).name,
                style={
                    "fontFamily": FONT_MONO,
                    "fontSize": "13px",
                    "color": COLORS["text"],
                    "flex": "1",
                },
            ),
            dbc.Button(
                "Charger",
                id={"type": "btn-load-existing", "path": path},
                style={
                    "background": COLORS["accent"],
                    "border": "none",
                    "color": COLORS["bg"],
                    "fontSize": "12px",
                    "fontWeight": "600",
                    "padding": "4px 14px",
                    "borderRadius": "6px",
                    "cursor": "pointer",
                },
            ),
        ],
        style={
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "space-between",
            "padding": "8px 12px",
            "borderRadius": "8px",
            "marginBottom": "6px",
            "background": COLORS["surface"],
            "border": f"1px solid {COLORS['border']}",
        },
    )


def _file_selection_ui(existing_jsons: list[str], error: str = "") -> html.Div:
    file_rows = [_file_row(p) for p in existing_jsons] or [
        html.Div(
            "Aucun fichier .json trouvé dans le répertoire courant.",
            style={"color": COLORS["muted"], "fontSize": "13px"},
        )
    ]
    error_div = (
        html.Div(
            error,
            style={
                "color": COLORS["danger"],
                "fontSize": "12px",
                "marginTop": "8px",
                "minHeight": "18px",
            },
        )
        if error
        else html.Div(style={"minHeight": "18px"})
    )

    return html.Div(
        [
            _section_title("Charger un fichier existant"),
            html.Div(file_rows, style={"marginBottom": "28px"}),
            _section_title("Créer un nouveau repo"),
            _label("Nom du fichier (sans extension)"),
            dbc.Input(
                id="new-repo-name",
                placeholder="ex: travail, perso, 2025…",
                style=_input_style(),
            ),
            error_div,
            dbc.Button(
                "Créer et charger",
                id="btn-create-repo",
                style={
                    "background": COLORS["accent"],
                    "border": "none",
                    "color": COLORS["bg"],
                    "fontSize": "13px",
                    "fontWeight": "600",
                    "padding": "8px 20px",
                    "borderRadius": "8px",
                    "cursor": "pointer",
                    "marginTop": "4px",
                    "boxShadow": "0 2px 8px rgba(108,142,245,0.2)",
                },
            ),
        ],
        style={"width": "100%"},
    )


# ══════════════════════════════════════════════════════════════════════════════
# ÉCRANS ET MODAUX — API PUBLIQUE (utilisée par les callbacks)
# ══════════════════════════════════════════════════════════════════════════════


def welcome_screen(existing_jsons: list[str]) -> html.Div:
    """Écran d'accueil affiché avant qu'un fichier soit choisi."""
    return html.Div(
        _plain_card(
            [
                html.Div(
                    "Bienvenue dans Todo-Engine",
                    style={
                        "fontWeight": "700",
                        "fontSize": "22px",
                        "color": COLORS["text"],
                        "marginBottom": "6px",
                    },
                ),
                html.Div(
                    "Choisissez ou créez un fichier pour commencer.",
                    style={
                        "color": COLORS["muted"],
                        "fontSize": "14px",
                        "marginBottom": "28px",
                    },
                ),
                _file_selection_ui(existing_jsons),
            ],
            {"maxWidth": "560px", "margin": "0 auto", "marginTop": "80px"},
        ),
        style={"padding": "0 36px"},
    )


def file_modal(existing_jsons: list[str], error: str = "") -> html.Div:
    """Modal flottant pour changer de fichier depuis l'app."""
    return html.Div(
        [
            html.Div(
                id="modal-backdrop",
                style={
                    "position": "fixed",
                    "inset": "0",
                    "background": COLORS["overlay"],
                    "zIndex": "200",
                },
            ),
            html.Div(
                _plain_card(
                    [
                        html.Div(
                            html.Span(
                                "Changer de fichier",
                                style={
                                    "fontWeight": "700",
                                    "fontSize": "17px",
                                    "color": COLORS["text"],
                                },
                            ),
                            style={"marginBottom": "22px"},
                        ),
                        _file_selection_ui(existing_jsons, error),
                    ],
                    {
                        "position": "fixed",
                        "top": "50%",
                        "left": "50%",
                        "transform": "translate(-50%, -50%)",
                        "zIndex": "201",
                        "width": "520px",
                        "maxWidth": "92vw",
                        "maxHeight": "85vh",
                        "overflowY": "auto",
                    },
                )
            ),
        ]
    )


# ══════════════════════════════════════════════════════════════════════════════
# LAYOUT PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════


def build_layout() -> html.Div:
    """Retourne le html.Div racine à assigner à app.layout."""

    header = html.Div(
        [
            html.Span(
                "Todo-Engine",
                style={
                    "fontWeight": "700",
                    "fontSize": "20px",
                    "color": COLORS["text"],
                },
            ),
            html.Span(
                id="header-filename",
                style={
                    "fontFamily": FONT_MONO,
                    "fontSize": "12px",
                    "color": COLORS["muted"],
                    "marginLeft": "12px",
                    "background": COLORS["card"],
                    "padding": "2px 8px",
                    "borderRadius": "4px",
                },
            ),
            html.Div(style={"flex": "1"}),
            dbc.Button(
                "Changer de fichier",
                id="btn-open-file-modal",
                style={
                    "background": "transparent",
                    "border": f"1px solid {COLORS['border']}",
                    "color": COLORS["muted"],
                    "fontSize": "12px",
                    "padding": "4px 12px",
                    "borderRadius": "6px",
                    "cursor": "pointer",
                },
            ),
        ],
        style={
            "background": COLORS["surface"],
            "borderBottom": f"1px solid {COLORS['border']}",
            "padding": "14px 36px",
            "display": "flex",
            "alignItems": "center",
            "position": "sticky",
            "top": "0",
            "zIndex": "100",
        },
    )

    tabs = html.Div(
        dcc.Tabs(
            id="main-tabs",
            value="tab-projects",
            children=[
                dcc.Tab(
                    label="Projets",
                    value="tab-projects",
                    style=TAB_STYLE,
                    selected_style=TAB_SELECTED_STYLE,
                ),
                dcc.Tab(
                    label="Priorités",
                    value="tab-priority",
                    style=TAB_STYLE,
                    selected_style=TAB_SELECTED_STYLE,
                ),
                dcc.Tab(
                    label="Dashboard",
                    value="tab-dashboard",
                    style=TAB_STYLE,
                    selected_style=TAB_SELECTED_STYLE,
                ),
            ],
            style={"marginBottom": "0"},
        ),
        style={
            "padding": "20px 36px 0 36px",
            "width": "100%",
            "boxSizing": "border-box",
        },
    )

    content = html.Div(
        id="tab-content",
        style={"width": "100%", "padding": "28px 36px", "boxSizing": "border-box"},
    )

    return html.Div(
        [
            dcc.Store(id="repo-path", data=None),
            dcc.Store(id="refresh-trigger", data=0),
            header,
            html.Div(
                id="main-content", children=[tabs, content], style={"display": "none"}
            ),
            html.Div(id="welcome-screen"),
            html.Div(id="file-modal-container"),
        ],
        style=GLOBAL_STYLE,
    )
