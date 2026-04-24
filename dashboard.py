"""
dashboard.py — Vue Dashboard : KPIs quantitatifs et graphes Plotly.
Dépend de theme.py. Reçoit un objet Repo et retourne du HTML Dash.
"""

from collections import Counter

import plotly.graph_objects as go
from dash import dcc, html

from theme import CHART_COLORS, COLORS, FONT_SANS, PRIO_COLORS

# ── Atomes dashboard ──────────────────────────────────────────────────────────

def kpi_card(label: str, value: str) -> html.Div:
    """Petite card affichant un chiffre clé."""
    return html.Div([
        html.Div(value, style={
            "fontSize":     "32px",
            "fontWeight":   "700",
            "color":        COLORS["accent"],
            "lineHeight":   "1",
            "marginBottom": "6px",
        }),
        html.Div(label, style={
            "fontSize":   "12px",
            "color":      COLORS["muted"],
            "fontWeight": "500",
        }),
    ], style={
        "background":   COLORS["card"],
        "border":       f"1px solid {COLORS['border']}",
        "borderRadius": "12px",
        "padding":      "20px 24px",
        "flex":         "1",
        "minWidth":     "160px",
        "boxShadow":    f"0 1px 4px {COLORS['shadow_sm']}",
    })


def _graph_card(fig: go.Figure, title: str) -> html.Div:
    """Card contenant un graphe Plotly stylé selon le thème."""
    fig.update_layout(
        paper_bgcolor=COLORS["transparent"],
        plot_bgcolor=COLORS["transparent"],
        font=dict(family=FONT_SANS, color=COLORS["text"], size=12),
        margin=dict(l=16, r=16, t=40, b=16),
        title=dict(text=title, font=dict(size=14, color=COLORS["text"]), x=0),
        legend=dict(bgcolor=COLORS["transparent"], borderwidth=0),
        xaxis=dict(
            gridcolor=COLORS["border"], linecolor=COLORS["border"],
            tickfont=dict(color=COLORS["muted"]),
        ),
        yaxis=dict(
            gridcolor=COLORS["border"], linecolor=COLORS["border"],
            tickfont=dict(color=COLORS["muted"]),
        ),
    )
    return html.Div(
        dcc.Graph(figure=fig, config={"displayModeBar": False},
                  style={"height": "320px"}),
        style={
            "background":   COLORS["card"],
            "border":       f"1px solid {COLORS['border']}",
            "borderRadius": "12px",
            "padding":      "16px",
            "flex":         "1",
            "minWidth":     "340px",
            "boxShadow":    f"0 1px 4px {COLORS['shadow_sm']}",
        },
    )


# ── Graphes ───────────────────────────────────────────────────────────────────

def _bar_subtasks_by_priority(all_subtasks: list) -> go.Figure:
    """Histogramme : nombre de sous-tâches par niveau de priorité."""
    prio_counts = Counter(st.priority for _, _, st in all_subtasks)
    priorities  = sorted(prio_counts)
    colors      = [PRIO_COLORS.get(p, COLORS["accent"]) for p in priorities]

    fig = go.Figure(go.Bar(
        x=[f"P{p}" for p in priorities],
        y=[prio_counts[p] for p in priorities],
        marker_color=colors,
        marker_line_width=0,
        text=[prio_counts[p] for p in priorities],
        textposition="outside",
        textfont=dict(color=COLORS["text"], size=12),
    ))
    fig.update_layout(showlegend=False, yaxis=dict(showgrid=True, zeroline=False))
    return fig


def _pie_days_by_project(repo) -> go.Figure:
    """Donut chart : répartition des jours planifiés par projet."""
    project_durations = {
        name: round(p.duration, 2)
        for name, p in repo.projects.items()
        if p.duration > 0
    }
    fig = go.Figure(go.Pie(
        labels=list(project_durations.keys()),
        values=list(project_durations.values()),
        marker=dict(
            colors=CHART_COLORS[:len(project_durations)],
            line=dict(color=COLORS["card"], width=2),
        ),
        textinfo="label+percent",
        hovertemplate="%{label}: %{value}j<extra></extra>",
        hole=0.35,
    ))
    return fig


# ── Vue principale ────────────────────────────────────────────────────────────

def render_dashboard(repo) -> html.Div:
    """Construit la vue dashboard complète à partir d'un objet Repo."""
    all_subtasks = repo.subtasks()

    # KPIs
    kpis = html.Div([
        kpi_card("Projets",         str(len(repo.projects))),
        kpi_card("Tâches",          str(sum(len(p.tasks) for p in repo.projects.values()))),
        kpi_card("Sous-tâches",     str(len(all_subtasks))),
        kpi_card("Jours planifiés", str(round(repo.duration, 1))),
    ], style={"display": "flex", "gap": "16px", "flexWrap": "wrap", "marginBottom": "24px"})

    if not all_subtasks:
        empty = html.Div(
            "Aucune donnée à afficher — ajoutez des projets et des sous-tâches.",
            style={"color": COLORS["muted"], "fontSize": "13px",
                   "textAlign": "center", "marginTop": "40px"},
        )
        return html.Div([kpis, empty])

    graphs = html.Div([
        _graph_card(_bar_subtasks_by_priority(all_subtasks), "Sous-tâches par priorité"),
        _graph_card(_pie_days_by_project(repo),              "Jours planifiés par projet"),
    ], style={"display": "flex", "gap": "16px", "flexWrap": "wrap"})

    return html.Div([kpis, graphs])
