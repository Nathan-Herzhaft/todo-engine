"""
ui.py — Composants visuels, thème et cards
Importé par app.py ; ne contient aucune logique Dash (pas de callbacks, pas d'app).
"""

import dash_bootstrap_components as dbc
from dash import dcc, html

# ══════════════════════════════════════════════════════════════════════════════
# THÈME
# ══════════════════════════════════════════════════════════════════════════════

FONT_SANS = "'Inter', 'DM Sans', 'Segoe UI', sans-serif"
FONT_MONO = "'JetBrains Mono', 'Fira Code', monospace"

GOOGLE_FONTS = (
    "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700"
    "&family=DM+Sans:wght@400;500;600"
    "&family=JetBrains+Mono:wght@400;600&display=swap"
)

COLORS = {
    "bg": "#111318",
    "surface": "#1a1d24",
    "card": "#21252f",
    "border": "#2e3340",
    "accent": "#6c8ef5",  # bleu lavande
    "accent2": "#a78bfa",  # violet doux
    "text": "#dde2ed",
    "muted": "#5c6479",
    "danger": "#f06b7a",
    "dur_bg": "#1e3a5f",
    "dur_fg": "#7eb8f7",
}

# Couleur fg par niveau de priorité (1 = urgent)
PRIO_COLORS = {
    1: "#f97316",
    2: "#f59e0b",
    3: "#eab308",
    4: "#a3a84a",
    5: "#6b9e6e",
}
# Fond foncé associé
PRIO_BG = {
    1: "#3d1f0a",
    2: "#3b2700",
    3: "#332d00",
    4: "#252a10",
    5: "#152518",
}

GLOBAL_STYLE = {
    "backgroundColor": COLORS["bg"],
    "color": COLORS["text"],
    "fontFamily": FONT_SANS,
    "minHeight": "100vh",
    "padding": "0 0 80px 0",
    "letterSpacing": "0.01em",
}

TAB_STYLE = {
    "fontSize": "13px",
    "background": "transparent",
    "color": COLORS["muted"],
    "border": "none",
    "borderBottom": "2px solid transparent",
    "padding": "8px 20px",
    "fontWeight": "500",
}

TAB_SELECTED_STYLE = {
    "fontSize": "13px",
    "background": "transparent",
    "color": COLORS["accent"],
    "border": "none",
    "borderBottom": f"2px solid {COLORS['accent']}",
    "padding": "8px 20px",
    "fontWeight": "600",
}


def prio_color(p: int) -> str:
    return PRIO_COLORS.get(int(p), COLORS["muted"])


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS — ATOMES UI
# ══════════════════════════════════════════════════════════════════════════════


def badge(label, bg, fg, mono=True):
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


def prio_badge(p: int):
    """Badge de priorité coloré selon le niveau."""
    return badge(f"P{p}", PRIO_BG.get(int(p), COLORS["border"]), prio_color(p))


def dur_badge(val):
    """Badge de durée en jours."""
    return badge(f"⏱ {val}j", COLORS["dur_bg"], COLORS["dur_fg"])


def tag_badge(label):
    """Badge neutre pour afficher un nom de projet ou de tâche."""
    return badge(label, "#252a38", "#8892aa", mono=False)


def delete_btn(btn_id: dict):
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
            "opacity": "0.55",
        },
    )


def styled_input(id_, placeholder, width="200px"):
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
            "boxShadow": "inset 0 1px 3px rgba(0,0,0,0.2)",
        },
    )


def small_btn(label, id_, color=None):
    return dbc.Button(
        label,
        id=id_,
        style={
            "background": color or COLORS["accent"],
            "border": "none",
            "color": "#fff" if color else COLORS["bg"],
            "fontSize": "12px",
            "fontWeight": "600",
            "padding": "6px 16px",
            "borderRadius": "8px",
            "cursor": "pointer",
            "boxShadow": "0 2px 8px rgba(108,142,245,0.2)",
        },
    )


def field_group(label, input_component):
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


def summary_link(label, color=None):
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


# ══════════════════════════════════════════════════════════════════════════════
# CARDS
# ══════════════════════════════════════════════════════════════════════════════


def subtask_card(subtask, st_idx, task_name, project_name):
    pc = prio_color(subtask.priority)

    edit_form = html.Details(
        [
            html.Summary(
                "Modifier",
                style={
                    "color": COLORS["muted"],
                    "fontSize": "11px",
                    "cursor": "pointer",
                    "userSelect": "none",
                    "marginTop": "8px",
                },
            ),
            html.Div(
                [
                    field_group(
                        "Description",
                        styled_input(
                            {
                                "type": "edit-st-desc",
                                "project": project_name,
                                "task": task_name,
                                "index": st_idx,
                            },
                            subtask.description,
                            "100%",
                        ),
                    ),
                    field_group(
                        "Priorité (1–5)",
                        styled_input(
                            {
                                "type": "edit-st-prio",
                                "project": project_name,
                                "task": task_name,
                                "index": st_idx,
                            },
                            str(subtask.priority),
                            "80px",
                        ),
                    ),
                    field_group(
                        "Durée (j)",
                        styled_input(
                            {
                                "type": "edit-st-dur",
                                "project": project_name,
                                "task": task_name,
                                "index": st_idx,
                            },
                            str(subtask.duration),
                            "80px",
                        ),
                    ),
                    html.Div(
                        [
                            html.Span(
                                "\u00a0",
                                style={
                                    "display": "block",
                                    "fontSize": "11px",
                                    "marginBottom": "4px",
                                },
                            ),
                            dbc.Button(
                                "Enregistrer",
                                id={
                                    "type": "save-subtask",
                                    "project": project_name,
                                    "task": task_name,
                                    "index": st_idx,
                                },
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
                            ),
                        ],
                        style={"display": "flex", "flexDirection": "column"},
                    ),
                ],
                style={
                    "display": "flex",
                    "gap": "10px",
                    "flexWrap": "wrap",
                    "marginTop": "10px",
                    "alignItems": "flex-end",
                },
            ),
        ]
    )

    return html.Div(
        [
            # ── Ligne principale : prio + description | durée + suppr ──────────
            html.Div(
                [
                    html.Div(
                        [
                            prio_badge(subtask.priority),
                            html.Span(
                                subtask.description,
                                style={"fontSize": "13px", "color": COLORS["text"]},
                            ),
                        ],
                        style={
                            "flex": "1",
                            "display": "flex",
                            "alignItems": "center",
                            "gap": "10px",
                        },
                    ),
                    html.Div(
                        [
                            dur_badge(subtask.duration),
                            delete_btn(
                                {
                                    "type": "del-subtask",
                                    "project": project_name,
                                    "task": task_name,
                                    "index": st_idx,
                                }
                            ),
                        ],
                        style={"display": "flex", "alignItems": "center", "gap": "8px"},
                    ),
                ],
                style={
                    "display": "flex",
                    "justifyContent": "space-between",
                    "alignItems": "center",
                },
            ),
            # ── Formulaire d'édition dépliable ────────────────────────────────
            edit_form,
        ],
        style={
            "background": COLORS["surface"],
            "border": f"1px solid {COLORS['border']}",
            "borderLeft": f"3px solid {pc}",
            "borderRadius": "6px",
            "padding": "8px 14px",
            "marginBottom": "6px",
        },
    )


def task_card(task, project_name):
    subtask_items = [
        subtask_card(st, idx, task.name, project_name)
        for idx, st in enumerate(task.subtasks)
    ]

    form = html.Details(
        [
            summary_link("+ Ajouter une sous-tâche"),
            html.Div(
                [
                    field_group(
                        "Description",
                        styled_input(
                            {
                                "type": "st-desc",
                                "project": project_name,
                                "task": task.name,
                            },
                            "ex: Rédiger le brief",
                            "100%",
                        ),
                    ),
                    field_group(
                        "Priorité (1–5)",
                        styled_input(
                            {
                                "type": "st-prio",
                                "project": project_name,
                                "task": task.name,
                            },
                            "1 à 5",
                            "90px",
                        ),
                    ),
                    field_group(
                        "Durée (j)",
                        styled_input(
                            {
                                "type": "st-dur",
                                "project": project_name,
                                "task": task.name,
                            },
                            "ex: 0.5",
                            "90px",
                        ),
                    ),
                    html.Div(
                        [
                            html.Span(
                                "\u00a0",
                                style={
                                    "display": "block",
                                    "fontSize": "11px",
                                    "marginBottom": "4px",
                                },
                            ),
                            small_btn(
                                "Ajouter",
                                {
                                    "type": "add-subtask",
                                    "project": project_name,
                                    "task": task.name,
                                },
                            ),
                        ],
                        style={"display": "flex", "flexDirection": "column"},
                    ),
                ],
                style={
                    "display": "flex",
                    "gap": "12px",
                    "flexWrap": "wrap",
                    "marginTop": "12px",
                    "alignItems": "flex-end",
                },
            ),
        ]
    )

    rename_form = html.Details(
        [
            html.Summary(
                "Renommer",
                style={
                    "color": COLORS["muted"],
                    "fontSize": "11px",
                    "cursor": "pointer",
                    "userSelect": "none",
                },
            ),
            html.Div(
                [
                    field_group(
                        "Nouveau nom",
                        styled_input(
                            {
                                "type": "edit-task-name",
                                "project": project_name,
                                "task": task.name,
                            },
                            task.name,
                            "220px",
                        ),
                    ),
                    html.Div(
                        [
                            html.Span(
                                "\u00a0",
                                style={
                                    "display": "block",
                                    "fontSize": "11px",
                                    "marginBottom": "4px",
                                },
                            ),
                            dbc.Button(
                                "Enregistrer",
                                id={
                                    "type": "save-task",
                                    "project": project_name,
                                    "task": task.name,
                                },
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
                            ),
                        ],
                        style={"display": "flex", "flexDirection": "column"},
                    ),
                ],
                style={
                    "display": "flex",
                    "gap": "10px",
                    "flexWrap": "wrap",
                    "marginTop": "10px",
                    "alignItems": "flex-end",
                },
            ),
        ]
    )

    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.Span(
                                task.name,
                                style={
                                    "fontWeight": "600",
                                    "fontSize": "14px",
                                    "color": COLORS["text"],
                                },
                            ),
                            dur_badge(task.duration),
                        ],
                        style={
                            "display": "flex",
                            "alignItems": "center",
                            "gap": "8px",
                            "flex": "1",
                        },
                    ),
                    delete_btn(
                        {"type": "del-task", "project": project_name, "task": task.name}
                    ),
                ],
                style={
                    "display": "flex",
                    "justifyContent": "space-between",
                    "alignItems": "center",
                    "paddingBottom": "8px",
                    "borderBottom": f"1px solid {COLORS['border']}",
                },
            ),
            rename_form,
            html.Div(style={"marginBottom": "10px"}),
            *subtask_items,
            form,
        ],
        style={
            "background": COLORS["card"],
            "border": f"1px solid {COLORS['border']}",
            "borderRadius": "10px",
            "padding": "14px 16px",
            "marginBottom": "10px",
            "boxShadow": "0 2px 8px rgba(0,0,0,0.25)",
        },
    )


def project_card(project):
    task_items = [task_card(t, project.name) for t in project.tasks.values()]

    form = html.Details(
        [
            summary_link("+ Ajouter une tâche", COLORS["accent"]),
            html.Div(
                [
                    field_group(
                        "Nom de la tâche",
                        styled_input(
                            {"type": "task-name", "project": project.name},
                            "ex: Développement front",
                            "100%",
                        ),
                    ),
                    html.Div(
                        [
                            html.Span(
                                "\u00a0",
                                style={
                                    "display": "block",
                                    "fontSize": "11px",
                                    "marginBottom": "4px",
                                },
                            ),
                            small_btn(
                                "Ajouter", {"type": "add-task", "project": project.name}
                            ),
                        ],
                        style={"display": "flex", "flexDirection": "column"},
                    ),
                ],
                style={
                    "display": "flex",
                    "gap": "12px",
                    "flexWrap": "wrap",
                    "marginTop": "12px",
                    "alignItems": "flex-end",
                },
            ),
        ]
    )

    rename_form = html.Details(
        [
            html.Summary(
                "Renommer le projet",
                style={
                    "color": COLORS["muted"],
                    "fontSize": "11px",
                    "cursor": "pointer",
                    "userSelect": "none",
                },
            ),
            html.Div(
                [
                    field_group(
                        "Nouveau nom",
                        styled_input(
                            {"type": "edit-project-name", "project": project.name},
                            project.name,
                            "240px",
                        ),
                    ),
                    html.Div(
                        [
                            html.Span(
                                "\u00a0",
                                style={
                                    "display": "block",
                                    "fontSize": "11px",
                                    "marginBottom": "4px",
                                },
                            ),
                            dbc.Button(
                                "Enregistrer",
                                id={"type": "save-project", "project": project.name},
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
                            ),
                        ],
                        style={"display": "flex", "flexDirection": "column"},
                    ),
                ],
                style={
                    "display": "flex",
                    "gap": "10px",
                    "flexWrap": "wrap",
                    "marginTop": "10px",
                    "alignItems": "flex-end",
                },
            ),
        ]
    )

    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.Span(
                                project.name,
                                style={
                                    "fontWeight": "700",
                                    "fontSize": "17px",
                                    "color": COLORS["text"],
                                    "letterSpacing": "0.01em",
                                },
                            ),
                            dur_badge(project.duration),
                        ],
                        style={
                            "display": "flex",
                            "alignItems": "center",
                            "gap": "10px",
                            "flex": "1",
                        },
                    ),
                    delete_btn({"type": "del-project", "project": project.name}),
                ],
                style={
                    "display": "flex",
                    "justifyContent": "space-between",
                    "alignItems": "center",
                    "paddingBottom": "10px",
                    "borderBottom": f"1px solid {COLORS['border']}",
                },
            ),
            rename_form,
            html.Div(style={"marginBottom": "14px"}),
            *task_items,
            form,
        ],
        style={
            "background": COLORS["surface"],
            "border": f"1px solid {COLORS['border']}",
            "borderTop": f"3px solid {COLORS['accent2']}",
            "borderRadius": "14px",
            "padding": "22px 26px",
            "marginBottom": "22px",
            "boxShadow": "0 4px 18px rgba(0,0,0,0.35)",
        },
    )


def priority_section(priority: int, subtasks_with_idx):
    """
    subtasks_with_idx : liste de tuples (subtask, real_index_in_task).
    Chaque tuple est produit par get_subtasks_with_idx() dans app.py.
    """
    pc = prio_color(priority)

    items = [
        html.Div(
            [
                html.Span(
                    st.description,
                    style={"fontSize": "13px", "color": COLORS["text"], "flex": "1"},
                ),
                html.Div(
                    [
                        tag_badge(st.parent_project),
                        tag_badge(st.parent_task),
                        dur_badge(st.duration),
                        delete_btn(
                            {
                                "type": "del-subtask",
                                "project": st.parent_project,
                                "task": st.parent_task,
                                "index": real_idx,
                            }
                        ),
                    ],
                    style={"display": "flex", "alignItems": "center", "gap": "6px"},
                ),
            ],
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "alignItems": "center",
                "background": COLORS["card"],
                "border": f"1px solid {COLORS['border']}",
                "borderLeft": f"3px solid {pc}",
                "borderRadius": "8px",
                "padding": "10px 16px",
                "marginBottom": "8px",
                "boxShadow": "0 2px 6px rgba(0,0,0,0.2)",
            },
        )
        for st, real_idx in subtasks_with_idx
    ]

    return html.Div(
        [
            html.Div(
                [
                    html.Span(
                        f"Priorité {priority}",
                        style={
                            "fontWeight": "700",
                            "fontSize": "15px",
                            "color": pc,
                        },
                    ),
                    html.Span(
                        f"{len(subtasks_with_idx)} sous-tâche{'s' if len(subtasks_with_idx) > 1 else ''}",
                        style={
                            "color": COLORS["muted"],
                            "fontSize": "12px",
                            "marginLeft": "10px",
                        },
                    ),
                ],
                style={
                    "marginBottom": "12px",
                    "paddingBottom": "10px",
                    "borderBottom": f"1px solid {COLORS['border']}",
                },
            ),
            *items,
        ],
        style={
            "background": COLORS["surface"],
            "border": f"1px solid {COLORS['border']}",
            "borderTop": f"3px solid {pc}",
            "borderRadius": "14px",
            "padding": "22px 26px",
            "marginBottom": "22px",
            "boxShadow": "0 4px 18px rgba(0,0,0,0.35)",
        },
    )


# ══════════════════════════════════════════════════════════════════════════════
# LAYOUT SHELL (header + onglets + contenu)
# Appelé depuis app.py pour construire app.layout
# ══════════════════════════════════════════════════════════════════════════════


def build_layout():
    """Retourne le html.Div racine à assigner à app.layout.
    Le nom du fichier courant est géré dynamiquement via dcc.Store dans app.py.
    """

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
            # Nom du fichier courant — mis à jour via callback depuis app.py
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
            # Bouton changer de fichier, poussé à droite
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
                    label="Par projet",
                    value="tab-projects",
                    style=TAB_STYLE,
                    selected_style=TAB_SELECTED_STYLE,
                ),
                dcc.Tab(
                    label="Par priorité",
                    value="tab-priority",
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
            dcc.Store(id="repo-path", data=None),  # chemin du JSON courant (str)
            dcc.Store(id="refresh-trigger", data=0),
            header,
            # Contenu principal masqué tant qu'aucun fichier n'est chargé
            html.Div(
                id="main-content", children=[tabs, content], style={"display": "none"}
            ),
            # Écran d'accueil affiché au démarrage
            html.Div(id="welcome-screen"),
            # Modal de sélection de fichier
            html.Div(id="file-modal-container"),
        ],
        style=GLOBAL_STYLE,
    )
