"""
app.py — Point d'entrée de l'application Dash TODO
Lancement : python app.py

Dépendances : dash, dash-bootstrap-components, pydantic
Structure   :
  app.py       ← ce fichier  (Dash init, layout, callbacks)
  ui.py        ← thème, composants, cards
  core.py      ← lecture/écriture JSON, add/clear
  structure.py ← modèles Pydantic
"""

import json as _json
from pathlib import Path

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback_context, html

from core import (
    add_project,
    add_subtask,
    add_task,
    clear_project,
    clear_subtask,
    clear_task,
    load_repo,
    save_repo,
)
from ui import (
    COLORS,
    FONT_MONO,
    FONT_SANS,
    GOOGLE_FONTS,
    build_layout,
    field_group,
    priority_section,
    project_card,
    small_btn,
    styled_input,
)

# ══════════════════════════════════════════════════════════════════════════════
# INIT DASH
# ══════════════════════════════════════════════════════════════════════════════

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, GOOGLE_FONTS],
    suppress_callback_exceptions=True,
)
app.title = "TODO Repo"
app.layout = build_layout()


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS UI (modaux / écrans)
# ══════════════════════════════════════════════════════════════════════════════


def _input_style(width="100%"):
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


def _label(text):
    return html.Div(
        text,
        style={
            "fontSize": "11px",
            "color": COLORS["muted"],
            "marginBottom": "6px",
            "fontFamily": FONT_SANS,
        },
    )


def _section_title(text):
    return html.Div(
        text,
        style={
            "fontSize": "13px",
            "fontWeight": "600",
            "color": COLORS["text"],
            "marginBottom": "10px",
        },
    )


def _card(children, style_extra=None):
    style = {
        "background": COLORS["card"],
        "border": f"1px solid {COLORS['border']}",
        "borderRadius": "12px",
        "padding": "20px 22px",
    }
    if style_extra:
        style.update(style_extra)
    return html.Div(children, style=style)


def _file_selection_ui(existing_jsons: list[str], error: str = ""):
    """
    Génère le contenu du panneau de sélection de fichier.
    existing_jsons : liste de chemins JSON trouvés dans le répertoire courant.
    """
    existing_items = []
    for path in existing_jsons:
        name = Path(path).name
        existing_items.append(
            html.Div(
                [
                    html.Span(
                        name,
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
        )

    if not existing_items:
        existing_items = [
            html.Div(
                "Aucun fichier .json trouvé dans le répertoire courant.",
                style={
                    "color": COLORS["muted"],
                    "fontSize": "13px",
                },
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
            # ── Charger un fichier existant ───────────────────────────────────
            _section_title("Charger un fichier existant"),
            html.Div(existing_items, style={"marginBottom": "28px"}),
            # ── Créer un nouveau fichier ──────────────────────────────────────
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


def _welcome_screen(existing_jsons: list[str]):
    """Écran d'accueil affiché avant qu'un fichier soit choisi."""
    return html.Div(
        _card(
            [
                html.Div(
                    "Bienvenue dans Todo Repo",
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


def _file_modal(existing_jsons: list[str], error: str = ""):
    """Modal flottant pour changer de fichier depuis l'app."""
    return html.Div(
        [
            # Fond semi-transparent cliquable
            html.Div(
                id="modal-backdrop",
                style={
                    "position": "fixed",
                    "inset": "0",
                    "background": "rgba(0,0,0,0.6)",
                    "zIndex": "200",
                },
            ),
            # Panneau central
            html.Div(
                _card(
                    [
                        html.Div(
                            [
                                html.Span(
                                    "Changer de fichier",
                                    style={
                                        "fontWeight": "700",
                                        "fontSize": "17px",
                                        "color": COLORS["text"],
                                    },
                                ),
                            ],
                            style={
                                "display": "flex",
                                "justifyContent": "space-between",
                                "alignItems": "center",
                                "marginBottom": "22px",
                            },
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
                ),
            ),
        ]
    )


def _scan_json_files() -> list[str]:
    """Retourne les fichiers .json du répertoire courant (hors node_modules etc.)."""
    return sorted(str(p) for p in Path(".").glob("*.json"))


# ══════════════════════════════════════════════════════════════════════════════
# CALLBACKS — GESTION DES FICHIERS
# ══════════════════════════════════════════════════════════════════════════════

# ── Écran d'accueil au démarrage ──────────────────────────────────────────────


@app.callback(
    Output("welcome-screen", "children"),
    Input("repo-path", "data"),
)
def render_welcome(repo_path):
    if repo_path is not None:
        return []  # fichier déjà chargé, écran d'accueil masqué
    return _welcome_screen(_scan_json_files())


# ── Afficher / masquer le contenu principal ───────────────────────────────────


@app.callback(
    Output("main-content", "style"),
    Output("header-filename", "children"),
    Input("repo-path", "data"),
)
def toggle_main_content(repo_path):
    if repo_path is None:
        return {"display": "none"}, ""
    return {"display": "block"}, Path(repo_path).name


# ── Modal "Changer de fichier" ────────────────────────────────────────────────


@app.callback(
    Output("file-modal-container", "children"),
    Input("btn-open-file-modal", "n_clicks"),
    Input("repo-path", "data"),
    prevent_initial_call=True,
)
def toggle_file_modal(open_clicks, repo_path):
    ctx = callback_context
    trigger = ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger == "btn-open-file-modal":
        return _file_modal(_scan_json_files())
    return []  # fermeture


# ── Charger un JSON existant ─────────────────────────────────────────────────


@app.callback(
    Output("repo-path", "data", allow_duplicate=True),
    Output("refresh-trigger", "data", allow_duplicate=True),
    Output("file-modal-container", "children", allow_duplicate=True),
    Output("welcome-screen", "children", allow_duplicate=True),
    Input({"type": "btn-load-existing", "path": dash.ALL}, "n_clicks"),
    State("refresh-trigger", "data"),
    prevent_initial_call=True,
)
def cb_load_existing(n_clicks_list, trigger):
    ctx = callback_context
    if not ctx.triggered or not any(n for n in n_clicks_list if n):
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update
    btn_id = _json.loads(ctx.triggered[0]["prop_id"].rsplit(".", 1)[0])
    path = btn_id["path"]
    # Vérifie que le fichier est lisible comme Repo
    try:
        load_repo(Path(path))
    except Exception:
        return (
            dash.no_update,
            dash.no_update,
            _file_modal(_scan_json_files(), f"Impossible de lire {path}"),
            dash.no_update,
        )
    return path, trigger + 1, [], []


# ── Créer un nouveau JSON ─────────────────────────────────────────────────────


@app.callback(
    Output("repo-path", "data", allow_duplicate=True),
    Output("refresh-trigger", "data", allow_duplicate=True),
    Output("file-modal-container", "children", allow_duplicate=True),
    Output("welcome-screen", "children", allow_duplicate=True),
    Input("btn-create-repo", "n_clicks"),
    State("new-repo-name", "value"),
    State("repo-path", "data"),
    State("refresh-trigger", "data"),
    prevent_initial_call=True,
)
def cb_create_repo(n_clicks, name, current_path, trigger):
    if not n_clicks or not name:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update

    name = name.strip().rstrip(".json")
    if not name:
        err = "Nom invalide."
        modal = _file_modal(_scan_json_files(), err) if current_path else dash.no_update
        welcome = (
            _welcome_screen(_scan_json_files()) if not current_path else dash.no_update
        )
        return dash.no_update, dash.no_update, modal, welcome

    path = Path(f"{name}.json")
    if path.exists():
        err = f"{path.name} existe déjà — utilisez « Charger »."
        modal = _file_modal(_scan_json_files(), err) if current_path else dash.no_update
        welcome = (
            _welcome_screen(_scan_json_files()) if not current_path else dash.no_update
        )
        return dash.no_update, dash.no_update, modal, welcome

    from structure import Repo

    save_repo(Repo(), path)
    return str(path), trigger + 1, [], []


# ══════════════════════════════════════════════════════════════════════════════
# CALLBACKS — RENDU DES ONGLETS
# ══════════════════════════════════════════════════════════════════════════════


@app.callback(
    Output("tab-content", "children"),
    Input("main-tabs", "value"),
    Input("refresh-trigger", "data"),
    State("repo-path", "data"),
)
def render_tab(tab, _, repo_path):
    if not repo_path:
        return []
    repo = load_repo(Path(repo_path))

    if tab == "tab-projects":
        cards = [project_card(p) for p in repo.projects.values()]
        add_project_form = html.Div(
            [
                html.Hr(
                    style={"borderColor": COLORS["border"], "margin": "4px 0 16px 0"}
                ),
                html.Div(
                    [
                        field_group(
                            "Nouveau projet",
                            styled_input(
                                "new-project-name", "ex: Refonte site", "280px"
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
                                    "+ Projet", "btn-add-project", COLORS["accent2"]
                                ),
                            ],
                            style={"display": "flex", "flexDirection": "column"},
                        ),
                    ],
                    style={
                        "display": "flex",
                        "gap": "12px",
                        "alignItems": "flex-end",
                        "flexWrap": "wrap",
                    },
                ),
            ]
        )
        return html.Div([*cards, add_project_form])

    else:  # tab-priority
        all_subtasks = repo.get_subtasks()
        priorities = sorted({st.priority for st in all_subtasks})
        sections = [
            priority_section(p, repo.get_subtasks(priority=p)) for p in priorities
        ]
        return (
            html.Div(sections)
            if sections
            else html.Div(
                "Aucune sous-tâche.",
                style={"color": COLORS["muted"], "fontFamily": FONT_MONO},
            )
        )


# ══════════════════════════════════════════════════════════════════════════════
# CALLBACKS — CRUD
# ══════════════════════════════════════════════════════════════════════════════


@app.callback(
    Output("refresh-trigger", "data", allow_duplicate=True),
    Input("btn-add-project", "n_clicks"),
    State("new-project-name", "value"),
    State("repo-path", "data"),
    State("refresh-trigger", "data"),
    prevent_initial_call=True,
)
def cb_add_project(n_clicks, name, repo_path, trigger):
    if not n_clicks or not name or not repo_path:
        return dash.no_update
    repo = load_repo(Path(repo_path))
    if name not in repo.projects:
        add_project(repo, name)
        save_repo(repo, Path(repo_path))
    return trigger + 1


@app.callback(
    Output("refresh-trigger", "data", allow_duplicate=True),
    Input({"type": "add-task", "project": dash.ALL}, "n_clicks"),
    State({"type": "task-name", "project": dash.ALL}, "value"),
    State("repo-path", "data"),
    State("refresh-trigger", "data"),
    prevent_initial_call=True,
)
def cb_add_task(n_clicks_list, names, repo_path, trigger):
    ctx = callback_context
    if not ctx.triggered or not repo_path:
        return dash.no_update
    raw = ctx.triggered[0]["prop_id"].rsplit(".", 1)[0]
    btn_id = _json.loads(raw)
    project_name = btn_id["project"]

    task_name = None
    for key, val in ctx.states.items():
        try:
            sid = _json.loads(key.rsplit(".", 1)[0])
            if (
                isinstance(sid, dict)
                and sid.get("type") == "task-name"
                and sid.get("project") == project_name
            ):
                task_name = val
                break
        except Exception:
            continue

    if not task_name:
        return dash.no_update
    repo = load_repo(Path(repo_path))
    project = repo.projects.get(project_name)
    if project and task_name not in project.tasks:
        add_task(project, task_name)
        save_repo(repo, Path(repo_path))
    return trigger + 1


@app.callback(
    Output("refresh-trigger", "data", allow_duplicate=True),
    Input({"type": "add-subtask", "project": dash.ALL, "task": dash.ALL}, "n_clicks"),
    State({"type": "st-desc", "project": dash.ALL, "task": dash.ALL}, "value"),
    State({"type": "st-prio", "project": dash.ALL, "task": dash.ALL}, "value"),
    State({"type": "st-dur", "project": dash.ALL, "task": dash.ALL}, "value"),
    State("repo-path", "data"),
    State("refresh-trigger", "data"),
    prevent_initial_call=True,
)
def cb_add_subtask(n_clicks_list, descs, prios, durs, repo_path, trigger):
    ctx = callback_context
    if not ctx.triggered or not repo_path:
        return dash.no_update
    raw = ctx.triggered[0]["prop_id"].rsplit(".", 1)[0]
    btn_id = _json.loads(raw)
    project_name = btn_id["project"]
    task_name = btn_id["task"]

    desc = prio = dur = None
    for key, val in ctx.states.items():
        try:
            sid = _json.loads(key.rsplit(".", 1)[0])
        except Exception:
            continue
        if not isinstance(sid, dict):
            continue
        if sid.get("project") != project_name or sid.get("task") != task_name:
            continue
        t = sid.get("type")
        if t == "st-desc":
            desc = val
        elif t == "st-prio":
            prio = val
        elif t == "st-dur":
            dur = val

    if not desc or not prio:
        return dash.no_update
    try:
        prio = int(prio)
        dur = float(dur) if dur else 0.0
    except ValueError:
        return dash.no_update

    repo = load_repo(Path(repo_path))
    project = repo.projects.get(project_name)
    if not project:
        return dash.no_update
    task = project.tasks.get(task_name)
    if not task:
        return dash.no_update
    add_subtask(task, desc, prio, dur)
    save_repo(repo, Path(repo_path))
    return trigger + 1


@app.callback(
    Output("refresh-trigger", "data", allow_duplicate=True),
    Input({"type": "del-project", "project": dash.ALL}, "n_clicks"),
    State("repo-path", "data"),
    State("refresh-trigger", "data"),
    prevent_initial_call=True,
)
def cb_del_project(n_clicks_list, repo_path, trigger):
    ctx = callback_context
    if not ctx.triggered or not repo_path or not any(n for n in n_clicks_list if n):
        return dash.no_update
    btn_id = _json.loads(ctx.triggered[0]["prop_id"].rsplit(".", 1)[0])
    project_name = btn_id["project"]
    repo = load_repo(Path(repo_path))
    if project_name in repo.projects:
        clear_project(repo, project_name)
        save_repo(repo, Path(repo_path))
    return trigger + 1


@app.callback(
    Output("refresh-trigger", "data", allow_duplicate=True),
    Input({"type": "del-task", "project": dash.ALL, "task": dash.ALL}, "n_clicks"),
    State("repo-path", "data"),
    State("refresh-trigger", "data"),
    prevent_initial_call=True,
)
def cb_del_task(n_clicks_list, repo_path, trigger):
    ctx = callback_context
    if not ctx.triggered or not repo_path or not any(n for n in n_clicks_list if n):
        return dash.no_update
    btn_id = _json.loads(ctx.triggered[0]["prop_id"].rsplit(".", 1)[0])
    project_name = btn_id["project"]
    task_name = btn_id["task"]
    repo = load_repo(Path(repo_path))
    project = repo.projects.get(project_name)
    if project and task_name in project.tasks:
        clear_task(project, task_name)
        save_repo(repo, Path(repo_path))
    return trigger + 1


@app.callback(
    Output("refresh-trigger", "data", allow_duplicate=True),
    Input(
        {
            "type": "del-subtask",
            "project": dash.ALL,
            "task": dash.ALL,
            "index": dash.ALL,
        },
        "n_clicks",
    ),
    State("repo-path", "data"),
    State("refresh-trigger", "data"),
    prevent_initial_call=True,
)
def cb_del_subtask(n_clicks_list, repo_path, trigger):
    ctx = callback_context
    if not ctx.triggered or not repo_path or not any(n for n in n_clicks_list if n):
        return dash.no_update
    btn_id = _json.loads(ctx.triggered[0]["prop_id"].rsplit(".", 1)[0])
    project_name = btn_id["project"]
    task_name = btn_id["task"]
    st_index = btn_id["index"]
    repo = load_repo(Path(repo_path))
    project = repo.projects.get(project_name)
    if not project:
        return dash.no_update
    task = project.tasks.get(task_name)
    if task and 0 <= st_index < len(task.subtasks):
        clear_subtask(task, st_index)
        save_repo(repo, Path(repo_path))
    return trigger + 1


# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app.run(debug=True)
