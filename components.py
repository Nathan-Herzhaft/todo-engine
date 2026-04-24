"""
components.py — Atomes UI réutilisables (badges, boutons, inputs, formulaires).
Aucune référence au domaine métier (Repo/Project/Task) ni aux callbacks Dash.
"""

import dash_bootstrap_components as dbc
from dash import html

from theme import COLORS, FONT_MONO, FONT_SANS, PRIO_BG, prio_color

# ── Badges ────────────────────────────────────────────────────────────────────


def badge(label, bg: str, fg: str, mono: bool = True) -> html.Span:
    """Badge coloré générique."""
    return html.Span(
        label,
        style={
            "background": bg,
            "color": fg,
            "fontFamily": FONT_MONO if mono else FONT_SANS,
            "fontSize": "11px",
            "fontWeight": "600",
            "padding": "3px 9px",
            "borderRadius": "6px",
            "whiteSpace": "nowrap",
        },
    )


def prio_badge(p: int) -> html.Span:
    """Badge de priorité coloré selon le niveau."""
    return badge(f"P{p}", PRIO_BG.get(int(p), COLORS["border"]), prio_color(p))


def dur_badge(val) -> html.Span:
    """Badge de durée en jours."""
    return badge(f"⏱ {val}j", COLORS["dur_bg"], COLORS["dur_fg"])


def tag_badge(label: str) -> html.Span:
    """Badge neutre pour afficher un nom de projet ou de tâche."""
    return badge(label, COLORS["tag_bg"], COLORS["tag_fg"], mono=False)


# ── Boutons ───────────────────────────────────────────────────────────────────


def delete_btn(btn_id: dict) -> dbc.Button:
    return dbc.Button(
        "✕",
        id=btn_id,
        color="link",
        title="Supprimer",
        style={
            "color": COLORS["muted"],
            "fontSize": "14px",
            "padding": "2px 6px",
            "lineHeight": "1",
            "opacity": "0.45",
        },
    )


def save_btn(btn_id: dict) -> dbc.Button:
    return dbc.Button(
        "Enregistrer",
        id=btn_id,
        style={
            "background": COLORS["accent"],
            "border": "none",
            "color": COLORS["bg"],
            "fontSize": "11px",
            "fontWeight": "600",
            "padding": "5px 12px",
            "borderRadius": "6px",
            "cursor": "pointer",
        },
    )


def small_btn(label: str, id_, color: str | None = None) -> dbc.Button:
    return dbc.Button(
        label,
        id=id_,
        style={
            "background": color or COLORS["accent"],
            "border": "none",
            "color": COLORS["white"] if color else COLORS["bg"],
            "fontSize": "12px",
            "fontWeight": "600",
            "padding": "6px 16px",
            "borderRadius": "8px",
            "cursor": "pointer",
            "boxShadow": f"0 1px 4px {COLORS['shadow_btn']}",
        },
    )


# ── Inputs & formulaires ──────────────────────────────────────────────────────


def styled_input(id_, placeholder: str, width: str = "200px") -> dbc.Input:
    return dbc.Input(
        id=id_,
        placeholder=placeholder,
        debounce=False,
        style={
            "background": COLORS["card"],
            "border": f"1px solid {COLORS['border']}",
            "color": COLORS["text"],
            "fontSize": "13px",
            "borderRadius": "8px",
            "width": width,
            "padding": "6px 12px",
            "boxShadow": f"inset 0 1px 2px {COLORS['shadow_input_inset']}",
        },
    )


def field_group(label: str, input_component) -> html.Div:
    """Groupe label + input pour les formulaires."""
    return html.Div(
        [
            html.Span(
                label,
                style={
                    "color": COLORS["muted"],
                    "fontSize": "11px",
                    "marginBottom": "4px",
                    "display": "block",
                },
            ),
            input_component,
        ],
        style={"display": "flex", "flexDirection": "column"},
    )


def summary_link(label: str, color: str | None = None) -> html.Summary:
    return html.Summary(
        label,
        style={
            "color": color or COLORS["muted"],
            "fontSize": "12px",
            "cursor": "pointer",
            "marginTop": "10px",
            "userSelect": "none",
        },
    )


def spacer(mb: str = "4px") -> html.Span:
    """Span vide pour aligner verticalement les boutons dans un field_group."""
    return html.Span(
        "\u00a0",
        style={"display": "block", "fontSize": "11px", "marginBottom": mb},
    )
