"""
callbacks.py — Tous les callbacks Dash de l'application.
Point d'entrée : register_callbacks(app) appelé depuis app.py.

Pattern : chaque callback charge le Repo depuis le JSON, effectue l'opération
via les méthodes d'instance de core.py, puis sauvegarde.
"""

import json as _json
from pathlib import Path

import dash
from dash import Input, Output, State, callback_context, html

from cards import priority_section, project_card
from components import field_group, small_btn, styled_input
from core import Repo
from dashboard import render_dashboard
from layout import file_modal, welcome_screen
from theme import COLORS, FONT_MONO

# ══════════════════════════════════════════════════════════════════════════════
# UTILITAIRES
# ══════════════════════════════════════════════════════════════════════════════


def _scan_json_files() -> list[str]:
    """Retourne les fichiers .json du répertoire courant."""
    return sorted(str(p) for p in Path(".").glob("*.json"))


def _get_state(
    ctx, type_: str, project: str, task: str | None = None, desc: str | None = None
) -> str | None:
    """Retrouve une valeur dans ctx.states par correspondance sur les clés JSON."""
    for key, val in ctx.states.items():
        try:
            sid = _json.loads(key.rsplit(".", 1)[0])
        except Exception:
            continue
        if not isinstance(sid, dict) or sid.get("type") != type_:
            continue
        if sid.get("project") != project:
            continue
        if task is not None and sid.get("task") != task:
            continue
        if desc is not None and sid.get("desc") != desc:
            continue
        return val
    return None


def _btn_id(ctx) -> dict:
    """Parse l'ID JSON du composant déclencheur."""
    return _json.loads(ctx.triggered[0]["prop_id"].rsplit(".", 1)[0])


# ══════════════════════════════════════════════════════════════════════════════
# REGISTRATION
# ══════════════════════════════════════════════════════════════════════════════


def register_callbacks(app: dash.Dash) -> None:

    # ── Gestion des fichiers ──────────────────────────────────────────────────

    @app.callback(
        Output("welcome-screen", "children"),
        Input("repo-path", "data"),
    )
    def render_welcome(repo_path):
        if repo_path is not None:
            return []
        return welcome_screen(_scan_json_files())

    @app.callback(
        Output("main-content", "style"),
        Output("header-filename", "children"),
        Input("repo-path", "data"),
    )
    def toggle_main_content(repo_path):
        if repo_path is None:
            return {"display": "none"}, ""
        return {"display": "block"}, Path(repo_path).name

    @app.callback(
        Output("file-modal-container", "children"),
        Input("btn-open-file-modal", "n_clicks"),
        Input("repo-path", "data"),
        prevent_initial_call=True,
    )
    def toggle_file_modal(open_clicks, repo_path):
        trigger = callback_context.triggered[0]["prop_id"].split(".")[0]
        if trigger == "btn-open-file-modal":
            return file_modal(_scan_json_files())
        return []

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
        path = _btn_id(ctx)["path"]
        try:
            Repo.load(Path(path))
        except Exception:
            return (
                dash.no_update,
                dash.no_update,
                file_modal(_scan_json_files(), f"Impossible de lire {path}"),
                dash.no_update,
            )
        return path, trigger + 1, [], []

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
        name = name.strip().removesuffix(".json")
        if not name:
            err = "Nom invalide."
            return (
                dash.no_update,
                dash.no_update,
                file_modal(_scan_json_files(), err) if current_path else dash.no_update,
                welcome_screen(_scan_json_files())
                if not current_path
                else dash.no_update,
            )
        path = Path(f"{name}.json")
        if path.exists():
            err = f"{path.name} existe déjà — utilisez « Charger »."
            return (
                dash.no_update,
                dash.no_update,
                file_modal(_scan_json_files(), err) if current_path else dash.no_update,
                welcome_screen(_scan_json_files())
                if not current_path
                else dash.no_update,
            )
        Repo().save(path)
        return str(path), trigger + 1, [], []

    # ── Rendu des onglets ─────────────────────────────────────────────────────

    @app.callback(
        Output("tab-content", "children"),
        Input("main-tabs", "value"),
        Input("refresh-trigger", "data"),
        State("repo-path", "data"),
    )
    def render_tab(tab, _, repo_path):
        if not repo_path:
            return []
        repo = Repo.load(Path(repo_path))

        if tab == "tab-projects":
            cards = [project_card(p) for p in repo.projects.values()]
            add_form = html.Div(
                [
                    html.Hr(
                        style={
                            "borderColor": COLORS["border"],
                            "margin": "4px 0 16px 0",
                        }
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
            return html.Div([*cards, add_form])

        elif tab == "tab-priority":
            all_st = repo.subtasks()
            priorities = sorted({st.priority for _, _, st in all_st})
            sections = [
                priority_section(p, repo.subtasks(priority=p)) for p in priorities
            ]
            return (
                html.Div(sections)
                if sections
                else html.Div(
                    "Aucune sous-tâche.",
                    style={"color": COLORS["muted"], "fontFamily": FONT_MONO},
                )
            )

        else:  # tab-dashboard
            return render_dashboard(repo)

    # ── CRUD — Projets ────────────────────────────────────────────────────────

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
        repo = Repo.load(Path(repo_path))
        if name not in repo.projects:
            repo.add_project(name)
            repo.save(Path(repo_path))
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
        pname = _btn_id(ctx)["project"]
        repo = Repo.load(Path(repo_path))
        if pname in repo.projects:
            repo.clear_project(pname)
            repo.save(Path(repo_path))
        return trigger + 1

    @app.callback(
        Output("refresh-trigger", "data", allow_duplicate=True),
        Input({"type": "save-project", "project": dash.ALL}, "n_clicks"),
        State({"type": "edit-project-name", "project": dash.ALL}, "value"),
        State("repo-path", "data"),
        State("refresh-trigger", "data"),
        prevent_initial_call=True,
    )
    def cb_rename_project(n_clicks_list, values, repo_path, trigger):
        ctx = callback_context
        if not ctx.triggered or not repo_path or not any(n for n in n_clicks_list if n):
            return dash.no_update
        old_name = _btn_id(ctx)["project"]
        new_name = _get_state(ctx, "edit-project-name", old_name)
        if not new_name or new_name == old_name:
            return dash.no_update
        repo = Repo.load(Path(repo_path))
        if old_name not in repo.projects:
            return dash.no_update
        repo.rename_project(old_name, new_name)
        repo.save(Path(repo_path))
        return trigger + 1

    # ── CRUD — Tâches ─────────────────────────────────────────────────────────

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
        project_name = _btn_id(ctx)["project"]
        task_name = _get_state(ctx, "task-name", project_name)
        if not task_name:
            return dash.no_update
        repo = Repo.load(Path(repo_path))
        project = repo.get_project(project_name)
        if project and task_name not in project.tasks:
            project.add_task(task_name)
            repo.save(Path(repo_path))
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
        btn = _btn_id(ctx)
        repo = Repo.load(Path(repo_path))
        project = repo.get_project(btn["project"])
        if project and btn["task"] in project.tasks:
            project.clear_task(btn["task"])
            repo.save(Path(repo_path))
        return trigger + 1

    @app.callback(
        Output("refresh-trigger", "data", allow_duplicate=True),
        Input({"type": "save-task", "project": dash.ALL, "task": dash.ALL}, "n_clicks"),
        State(
            {"type": "edit-task-name", "project": dash.ALL, "task": dash.ALL}, "value"
        ),
        State("repo-path", "data"),
        State("refresh-trigger", "data"),
        prevent_initial_call=True,
    )
    def cb_rename_task(n_clicks_list, values, repo_path, trigger):
        ctx = callback_context
        if not ctx.triggered or not repo_path or not any(n for n in n_clicks_list if n):
            return dash.no_update
        btn = _btn_id(ctx)
        pname = btn["project"]
        old_name = btn["task"]
        new_name = _get_state(ctx, "edit-task-name", pname, old_name)
        if not new_name or new_name == old_name:
            return dash.no_update
        repo = Repo.load(Path(repo_path))
        project = repo.get_project(pname)
        if not project or old_name not in project.tasks:
            return dash.no_update
        project.rename_task(old_name, new_name)
        repo.save(Path(repo_path))
        return trigger + 1

    # ── CRUD — Sous-tâches ────────────────────────────────────────────────────

    @app.callback(
        Output("refresh-trigger", "data", allow_duplicate=True),
        Input(
            {"type": "add-subtask", "project": dash.ALL, "task": dash.ALL}, "n_clicks"
        ),
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
        btn = _btn_id(ctx)
        pname = btn["project"]
        tname = btn["task"]
        desc = _get_state(ctx, "st-desc", pname, tname)
        prio = _get_state(ctx, "st-prio", pname, tname)
        dur = _get_state(ctx, "st-dur", pname, tname)
        if not desc or not prio:
            return dash.no_update
        try:
            prio = int(prio)
            dur = float(dur) if dur else 0.0
        except ValueError:
            return dash.no_update
        repo = Repo.load(Path(repo_path))
        project = repo.get_project(pname)
        if not project:
            return dash.no_update
        task = project.get_task(tname)
        if not task:
            return dash.no_update
        task.add_subtask(desc, prio, dur)
        repo.save(Path(repo_path))
        return trigger + 1

    @app.callback(
        Output("refresh-trigger", "data", allow_duplicate=True),
        Input(
            {
                "type": "del-subtask",
                "project": dash.ALL,
                "task": dash.ALL,
                "desc": dash.ALL,
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
        btn = _btn_id(ctx)
        repo = Repo.load(Path(repo_path))
        project = repo.get_project(btn["project"])
        if not project:
            return dash.no_update
        task = project.get_task(btn["task"])
        if task and btn["desc"] in task.subtasks:
            task.clear_subtask(btn["desc"])
            repo.save(Path(repo_path))
        return trigger + 1

    @app.callback(
        Output("refresh-trigger", "data", allow_duplicate=True),
        Input(
            {
                "type": "save-subtask",
                "project": dash.ALL,
                "task": dash.ALL,
                "desc": dash.ALL,
            },
            "n_clicks",
        ),
        State(
            {
                "type": "edit-st-desc",
                "project": dash.ALL,
                "task": dash.ALL,
                "desc": dash.ALL,
            },
            "value",
        ),
        State(
            {
                "type": "edit-st-prio",
                "project": dash.ALL,
                "task": dash.ALL,
                "desc": dash.ALL,
            },
            "value",
        ),
        State(
            {
                "type": "edit-st-dur",
                "project": dash.ALL,
                "task": dash.ALL,
                "desc": dash.ALL,
            },
            "value",
        ),
        State("repo-path", "data"),
        State("refresh-trigger", "data"),
        prevent_initial_call=True,
    )
    def cb_edit_subtask(n_clicks_list, descs, prios, durs, repo_path, trigger):
        ctx = callback_context
        if not ctx.triggered or not repo_path or not any(n for n in n_clicks_list if n):
            return dash.no_update
        btn = _btn_id(ctx)
        pname = btn["project"]
        tname = btn["task"]
        old_desc = btn["desc"]
        new_desc = _get_state(ctx, "edit-st-desc", pname, tname, old_desc)
        prio_str = _get_state(ctx, "edit-st-prio", pname, tname, old_desc)
        dur_str = _get_state(ctx, "edit-st-dur", pname, tname, old_desc)
        try:
            prio_val = int(prio_str) if prio_str else None
            dur_val = float(dur_str) if dur_str else None
        except ValueError:
            return dash.no_update
        repo = Repo.load(Path(repo_path))
        project = repo.get_project(pname)
        if not project:
            return dash.no_update
        task = project.get_task(tname)
        if not task or old_desc not in task.subtasks:
            return dash.no_update
        task.modify_subtask(
            old_desc, description=new_desc, priority=prio_val, duration=dur_val
        )
        repo.save(Path(repo_path))
        return trigger + 1
