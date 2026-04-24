"""
cards.py — Composants Dash représentant les entités métier (Projet, Tâche, Sous-tâche).
Dépend de components.py et theme.py. Aucune logique callback ici.
"""

from dash import html

from components import (
    delete_btn,
    dur_badge,
    field_group,
    prio_badge,
    save_btn,
    small_btn,
    spacer,
    styled_input,
    summary_link,
    tag_badge,
)
from theme import COLORS, prio_color

# ── Sous-tâche ────────────────────────────────────────────────────────────────


def subtask_card(subtask, st_desc: str, task_name: str, project_name: str) -> html.Div:
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
                                "desc": st_desc,
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
                                "desc": st_desc,
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
                                "desc": st_desc,
                            },
                            str(subtask.duration),
                            "80px",
                        ),
                    ),
                    html.Div(
                        [
                            spacer(),
                            save_btn(
                                {
                                    "type": "save-subtask",
                                    "project": project_name,
                                    "task": task_name,
                                    "desc": st_desc,
                                }
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
            # Ligne principale : prio + description | durée + suppr
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
                                    "desc": st_desc,
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
            # Formulaire d'édition dépliable
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


# ── Tâche ─────────────────────────────────────────────────────────────────────


def task_card(task, project_name: str) -> html.Div:
    subtasks_sorted = sorted(
        task.subtasks.items(),
        key=lambda x: (x[1].priority, x[1].description),
    )
    subtask_items = [
        subtask_card(st, desc, task.name, project_name) for desc, st in subtasks_sorted
    ]

    add_form = html.Details(
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
                            spacer(),
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
                            spacer(),
                            save_btn(
                                {
                                    "type": "save-task",
                                    "project": project_name,
                                    "task": task.name,
                                }
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
            add_form,
        ],
        style={
            "background": COLORS["card"],
            "border": f"1px solid {COLORS['border']}",
            "borderRadius": "10px",
            "padding": "14px 16px",
            "marginBottom": "10px",
            "boxShadow": COLORS["shadow_card_task"],
        },
    )


# ── Projet ────────────────────────────────────────────────────────────────────


def project_card(project) -> html.Div:
    task_items = [task_card(t, project.name) for t in project.tasks.values()]

    add_form = html.Details(
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
                            spacer(),
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
                            spacer(),
                            save_btn({"type": "save-project", "project": project.name}),
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
            add_form,
        ],
        style={
            "background": COLORS["surface"],
            "border": f"1px solid {COLORS['border']}",
            "borderTop": f"3px solid {COLORS['accent2']}",
            "borderRadius": "14px",
            "padding": "22px 26px",
            "marginBottom": "22px",
            "boxShadow": COLORS["shadow_card_project"],
        },
    )


# ── Vue par priorité ──────────────────────────────────────────────────────────


def priority_section(priority: int, subtasks_tuples: list) -> html.Div:
    """
    subtasks_tuples : liste de tuples (Project, Task, SubTask)
    telle que retournée par repo.subtasks(priority=p).
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
                        tag_badge(project.name),
                        tag_badge(task.name),
                        dur_badge(st.duration),
                        delete_btn(
                            {
                                "type": "del-subtask",
                                "project": project.name,
                                "task": task.name,
                                "desc": st.description,
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
                "boxShadow": COLORS["shadow_prio_item"],
            },
        )
        for project, task, st in subtasks_tuples
    ]

    n = len(subtasks_tuples)
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
                        f"{n} sous-tâche{'s' if n > 1 else ''}",
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
            "boxShadow": COLORS["shadow_card_project"],
        },
    )
