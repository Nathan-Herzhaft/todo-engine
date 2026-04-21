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
import sys
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
    GOOGLE_FONTS,
    build_layout,
    field_group,
    priority_section,
    project_card,
    small_btn,
    styled_input,
)

# ── Path du JSON (modifiable) ─────────────────────────────────────────────────
REPO_PATH = Path("toy_repo.json")

# ── Imports locaux ────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent))

# ══════════════════════════════════════════════════════════════════════════════
# INIT DASH
# ══════════════════════════════════════════════════════════════════════════════

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, GOOGLE_FONTS],
    suppress_callback_exceptions=True,
)
app.title = "TODO Repo"
app.layout = build_layout(REPO_PATH.name)


# ══════════════════════════════════════════════════════════════════════════════
# CALLBACKS
# ══════════════════════════════════════════════════════════════════════════════

# ── Rendu des onglets ─────────────────────────────────────────────────────────


@app.callback(
    Output("tab-content", "children"),
    Input("main-tabs", "value"),
    Input("refresh-trigger", "data"),
)
def render_tab(tab, _):
    repo = load_repo(REPO_PATH)

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


# ── Ajout projet ──────────────────────────────────────────────────────────────


@app.callback(
    Output("refresh-trigger", "data", allow_duplicate=True),
    Input("btn-add-project", "n_clicks"),
    State("new-project-name", "value"),
    State("refresh-trigger", "data"),
    prevent_initial_call=True,
)
def cb_add_project(n_clicks, name, trigger):
    if not n_clicks or not name:
        return dash.no_update
    repo = load_repo(REPO_PATH)
    if name not in repo.projects:
        add_project(repo, name)
        save_repo(repo, REPO_PATH)
    return trigger + 1


# ── Ajout tâche ───────────────────────────────────────────────────────────────


@app.callback(
    Output("refresh-trigger", "data", allow_duplicate=True),
    Input({"type": "add-task", "project": dash.ALL}, "n_clicks"),
    State({"type": "task-name", "project": dash.ALL}, "value"),
    State("refresh-trigger", "data"),
    prevent_initial_call=True,
)
def cb_add_task(n_clicks_list, names, trigger):
    ctx = callback_context
    if not ctx.triggered:
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
    repo = load_repo(REPO_PATH)
    project = repo.projects.get(project_name)
    if project and task_name not in project.tasks:
        add_task(project, task_name)
        save_repo(repo, REPO_PATH)
    return trigger + 1


# ── Ajout sous-tâche ──────────────────────────────────────────────────────────


@app.callback(
    Output("refresh-trigger", "data", allow_duplicate=True),
    Input({"type": "add-subtask", "project": dash.ALL, "task": dash.ALL}, "n_clicks"),
    State({"type": "st-desc", "project": dash.ALL, "task": dash.ALL}, "value"),
    State({"type": "st-prio", "project": dash.ALL, "task": dash.ALL}, "value"),
    State({"type": "st-dur", "project": dash.ALL, "task": dash.ALL}, "value"),
    State("refresh-trigger", "data"),
    prevent_initial_call=True,
)
def cb_add_subtask(n_clicks_list, descs, prios, durs, trigger):
    ctx = callback_context
    if not ctx.triggered:
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

    repo = load_repo(REPO_PATH)
    project = repo.projects.get(project_name)
    if not project:
        return dash.no_update
    task = project.tasks.get(task_name)
    if not task:
        return dash.no_update
    add_subtask(task, desc, prio, dur)
    save_repo(repo, REPO_PATH)
    return trigger + 1


# ── Suppression projet ────────────────────────────────────────────────────────


@app.callback(
    Output("refresh-trigger", "data", allow_duplicate=True),
    Input({"type": "del-project", "project": dash.ALL}, "n_clicks"),
    State("refresh-trigger", "data"),
    prevent_initial_call=True,
)
def cb_del_project(n_clicks_list, trigger):
    ctx = callback_context
    if not ctx.triggered or not any(n for n in n_clicks_list if n):
        return dash.no_update
    btn_id = _json.loads(ctx.triggered[0]["prop_id"].rsplit(".", 1)[0])
    project_name = btn_id["project"]

    repo = load_repo(REPO_PATH)
    if project_name in repo.projects:
        clear_project(repo, project_name)
        save_repo(repo, REPO_PATH)
    return trigger + 1


# ── Suppression tâche ─────────────────────────────────────────────────────────


@app.callback(
    Output("refresh-trigger", "data", allow_duplicate=True),
    Input({"type": "del-task", "project": dash.ALL, "task": dash.ALL}, "n_clicks"),
    State("refresh-trigger", "data"),
    prevent_initial_call=True,
)
def cb_del_task(n_clicks_list, trigger):
    ctx = callback_context
    if not ctx.triggered or not any(n for n in n_clicks_list if n):
        return dash.no_update
    btn_id = _json.loads(ctx.triggered[0]["prop_id"].rsplit(".", 1)[0])
    project_name = btn_id["project"]
    task_name = btn_id["task"]

    repo = load_repo(REPO_PATH)
    project = repo.projects.get(project_name)
    if project and task_name in project.tasks:
        clear_task(project, task_name)
        save_repo(repo, REPO_PATH)
    return trigger + 1


# ── Suppression sous-tâche ────────────────────────────────────────────────────


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
    State("refresh-trigger", "data"),
    prevent_initial_call=True,
)
def cb_del_subtask(n_clicks_list, trigger):
    ctx = callback_context
    if not ctx.triggered or not any(n for n in n_clicks_list if n):
        return dash.no_update
    btn_id = _json.loads(ctx.triggered[0]["prop_id"].rsplit(".", 1)[0])
    project_name = btn_id["project"]
    task_name = btn_id["task"]
    st_index = btn_id["index"]

    repo = load_repo(REPO_PATH)
    project = repo.projects.get(project_name)
    if not project:
        return dash.no_update
    task = project.tasks.get(task_name)
    if task and 0 <= st_index < len(task.subtasks):
        clear_subtask(task, st_index)
        save_repo(repo, REPO_PATH)
    return trigger + 1


# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app.run()
