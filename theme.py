"""
theme.py — Source unique de vérité pour TOUTES les couleurs, polices et styles.
Aucune valeur de couleur hexadécimale ou rgba ne doit apparaître dans les autres modules.
"""

# ── Polices ───────────────────────────────────────────────────────────────────

FONT_SANS = "'Inter', 'Google Sans', 'Segoe UI', sans-serif"
FONT_MONO = "'Roboto Mono', 'Fira Code', monospace"

GOOGLE_FONTS = (
    "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700"
    "&family=Roboto+Mono:wght@400;500&display=swap"
)

# ── Palette principale ────────────────────────────────────────────────────────

COLORS = {
    # Fonds
    "bg":          "#f8f9fa",   # gris perle très clair (fond page)
    "surface":     "#ffffff",   # blanc pur (header, surfaces élevées)
    "card":        "#ffffff",   # blanc pur (cards)
    "border":      "#e0e4ea",   # gris doux

    # Accents
    "accent":      "#1a73e8",   # bleu Google vif
    "accent2":     "#8430ce",   # violet Google

    # Texte
    "text":        "#1f2937",   # gris foncé quasi-noir
    "muted":       "#6b7280",   # gris moyen
    "white":       "#ffffff",   # blanc pur (texte sur fond coloré, boutons)

    # Sémantique
    "danger":      "#d93025",   # rouge Google

    # Badge durée
    "dur_bg":      "#e8f0fe",   # bleu très pâle
    "dur_fg":      "#1a73e8",   # bleu Google

    # Badge tag (projet/tâche dans vue priorité)
    "tag_bg":      "#f1f3f4",   # gris Google très clair
    "tag_fg":      "#5f6368",   # gris Google moyen

    # Transparences nommées
    "transparent":         "rgba(0,0,0,0)",     # fond transparent (graphes)
    "overlay":             "rgba(0,0,0,0.6)",   # fond modal
    "shadow_sm":           "rgba(0,0,0,0.07)",  # ombre légère cards
    "shadow_md":           "rgba(0,0,0,0.08)",  # ombre moyenne project cards
    "shadow_outline":      "rgba(0,0,0,0.04)",  # contour subtil
    "shadow_btn":          "rgba(26,115,232,0.25)",  # ombre bouton accent
    "shadow_input_inset":  "rgba(0,0,0,0.06)",  # ombre inset inputs

    # Ombres composées (cards)
    "shadow_card_task":    "0 1px 4px rgba(0,0,0,0.07)",
    "shadow_card_project": "0 1px 6px rgba(0,0,0,0.08), 0 0 0 1px rgba(0,0,0,0.04)",
    "shadow_prio_item":    "0 1px 3px rgba(0,0,0,0.06)",
}

# ── Couleurs de priorité (1 = urgent) ────────────────────────────────────────

PRIO_COLORS = {
    1: "#d93025",   # rouge Google
    2: "#e8710a",   # orange
    3: "#f9ab00",   # ambre
    4: "#1e8e3e",   # vert Google
    5: "#1a73e8",   # bleu Google
}

PRIO_BG = {
    1: "#fce8e6",   # rose pâle
    2: "#fde9d3",   # pêche pâle
    3: "#fef7e0",   # jaune crème
    4: "#e6f4ea",   # vert pâle
    5: "#e8f0fe",   # bleu pâle
}

# ── Palette graphes ───────────────────────────────────────────────────────────

CHART_COLORS = [
    "#1a73e8",   # bleu Google
    "#8430ce",   # violet
    "#e8710a",   # orange
    "#1e8e3e",   # vert
    "#f9ab00",   # ambre
    "#d93025",   # rouge
    "#00897b",   # teal
    "#e91e8c",   # rose
]

# ── Styles globaux ────────────────────────────────────────────────────────────

GLOBAL_STYLE = {
    "backgroundColor": COLORS["bg"],
    "color":           COLORS["text"],
    "fontFamily":      FONT_SANS,
    "minHeight":       "100vh",
    "padding":         "0 0 80px 0",
    "letterSpacing":   "0.01em",
}

TAB_STYLE = {
    "fontSize":     "13px",
    "background":   "transparent",
    "color":        COLORS["muted"],
    "border":       "none",
    "borderBottom": f"2px solid {COLORS['transparent']}",
    "padding":      "8px 20px",
    "fontWeight":   "500",
}

TAB_SELECTED_STYLE = {
    "fontSize":     "13px",
    "background":   "transparent",
    "color":        COLORS["accent"],
    "border":       "none",
    "borderBottom": f"2px solid {COLORS['accent']}",
    "padding":      "8px 20px",
    "fontWeight":   "600",
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def prio_color(p: int) -> str:
    return PRIO_COLORS.get(int(p), COLORS["muted"])
