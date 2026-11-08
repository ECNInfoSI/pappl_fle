#!/usr/bin/env python3
"""Génère les maquettes SVG de Centrale App FLE (charte Centrale Pékin)."""
import base64, os, sys
from xml.sax.saxutils import escape

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
LOGO = base64.b64encode(open(os.path.join(os.path.dirname(__file__), "logo.png"), "rb").read()).decode()

W, H = 1440, 900
NAVY, NAVY_D, NAVY_L = "#1B1F8A", "#12155E", "#EEF0FB"
RED, RED_L = "#C0191F", "#FBECEC"
TEXT, MUTED, BORDER, BG, WHITE = "#1C1E2E", "#6B6F80", "#E3E5EC", "#F6F7FA", "#FFFFFF"
GREEN, GREEN_L, AMBER, AMBER_L = "#1E7B4F", "#E7F4EE", "#9A6400", "#FFF4DC"
FONT = "Inter"


def tw(s, size=14, weight=400):
    return len(s) * size * (0.58 if weight >= 600 else 0.55)


class S:
    def __init__(self):
        self.p = []

    def add(self, x):
        self.p.append(x)

    def g(self, name):
        self.p.append(f'<g id="{escape(name)}">')

    def end(self):
        self.p.append("</g>")

    def rect(self, x, y, w, h, fill=WHITE, stroke=None, r=0, sw=1, name=None, dash=None):
        a = f'x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"'
        if r: a += f' rx="{r}"'
        if stroke: a += f' stroke="{stroke}" stroke-width="{sw}"'
        if dash: a += f' stroke-dasharray="{dash}"'
        if name: a = f'id="{escape(name)}" ' + a
        self.add(f"<rect {a}/>")

    def circle(self, cx, cy, r, fill=WHITE, stroke=None, sw=1):
        a = f'cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"'
        if stroke: a += f' stroke="{stroke}" stroke-width="{sw}"'
        self.add(f"<circle {a}/>")

    def line(self, x1, y1, x2, y2, c=BORDER, sw=1):
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{sw}"/>')

    def path(self, d, stroke=TEXT, fill="none", sw=1.6):
        self.add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')

    def text(self, x, y, s, size=14, weight=400, fill=TEXT, anchor="start"):
        self.add(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
                 f'fill="{fill}" text-anchor="{anchor}">{escape(s)}</text>')

    # ---------- composants ----------
    def button(self, x, y, label, kind="primary", w=None, h=40, size=14):
        w = w or int(tw(label, size, 600) + 36)
        fill, stroke, col = {
            "primary": (NAVY, None, WHITE),
            "secondary": (WHITE, BORDER, TEXT),
            "danger": (RED, None, WHITE),
            "ghost": (WHITE, None, NAVY),
            "danger-ghost": (WHITE, "#F0C9CB", RED),
        }[kind]
        self.g(f"Bouton / {label}")
        self.rect(x, y, w, h, fill, stroke, r=8)
        self.text(x + w / 2, y + h / 2 + size * 0.36, label, size, 600, col, "middle")
        self.end()
        return w

    def field(self, x, y, w, label, value="", placeholder="", h=40, select=False):
        self.g(f"Champ / {label or placeholder}")
        if label:
            self.text(x, y - 8, label, 13, 500, TEXT)
        self.rect(x, y, w, h, WHITE, BORDER, r=8)
        if value:
            self.text(x + 12, y + h / 2 + 5, value, 14, 400, TEXT)
        elif placeholder:
            self.text(x + 12, y + h / 2 + 5, placeholder, 14, 400, "#9A9DAB")
        if select:
            cx, cy = x + w - 18, y + h / 2
            self.path(f"M{cx-4} {cy-2} L{cx} {cy+2} L{cx+4} {cy-2}", MUTED)
        self.end()

    def search(self, x, y, w, placeholder):
        self.field(x, y, w, "")
        self.text(x + 38, y + 25, placeholder, 14, 400, "#9A9DAB")
        self.circle(x + 20, y + 18, 6, "none", MUTED, 1.6)
        self.line(x + 24.5, y + 22.5, x + 28, y + 26, MUTED, 1.6)

    def badge(self, x, y, label, fg=NAVY, bg=NAVY_L):
        w = tw(label, 12, 600) + 16
        self.g(f"Badge / {label}")
        self.rect(x, y, w, 22, bg, r=11)
        self.text(x + w / 2, y + 15, label, 12, 600, fg, "middle")
        self.end()
        return w

    def checkbox(self, x, y, checked=False, radio=False):
        if radio:
            self.circle(x + 9, y + 9, 9, WHITE, NAVY if checked else "#B9BCC8", 1.5)
            if checked: self.circle(x + 9, y + 9, 4.5, NAVY)
        else:
            self.rect(x, y, 18, 18, NAVY if checked else WHITE, None if checked else "#B9BCC8", r=4, sw=1.5)
            if checked: self.path(f"M{x+4} {y+9.5} L{x+7.5} {y+13} L{x+14} {y+5.5}", WHITE, sw=2)

    def toggle(self, x, y, on=True):
        self.rect(x, y, 36, 20, NAVY if on else "#C9CCD6", r=10)
        self.circle(x + (26 if on else 10), y + 10, 7, WHITE)

    def card(self, x, y, w, h, name="Carte"):
        self.rect(x, y, w, h, WHITE, BORDER, r=12, name=name)

    def handle(self, x, y):
        for dx in (0, 6):
            for dy in (0, 6, 12):
                self.circle(x + dx, y + dy, 1.6, "#A4A7B5")

    def kebab(self, x, y):
        for dy in (0, 6, 12):
            self.circle(x, y + dy, 1.8, MUTED)

    def table(self, x, y, cols, rows, row_h=52, name="Tableau", sort_col=None):
        """cols: [(titre, largeur)] ; rows: listes de cellules (str ou callable(x,y))."""
        w = sum(c[1] for c in cols)
        self.g(name)
        self.rect(x, y, w, 44 + row_h * len(rows), WHITE, BORDER, r=12)
        self.rect(x + 1, y + 1, w - 2, 43, BG, r=11)
        self.rect(x + 1, y + 20, w - 2, 24, BG)
        cx = x
        for i, (t, cw) in enumerate(cols):
            self.text(cx + 16, y + 27, t.upper(), 11, 600, MUTED)
            if sort_col == i:
                ax = cx + 16 + tw(t.upper(), 11, 600) + 8
                self.path(f"M{ax} {y+21} L{ax+4} {y+25} L{ax+8} {y+21}", NAVY, sw=1.6)
            cx += cw
        for r, row in enumerate(rows):
            ry = y + 44 + r * row_h
            self.line(x, ry, x + w, ry)
            cx = x
            for c, cell in enumerate(row):
                if callable(cell):
                    cell(cx + 16, ry + row_h / 2)
                elif cell:
                    self.text(cx + 16, ry + row_h / 2 + 5, cell, 14, 600 if c == 0 else 400,
                              TEXT if c == 0 else MUTED)
                cx += cols[c][1]
        self.end()

    def modal_backdrop(self):
        self.rect(0, 0, W, H, "#12155E", name="Voile").__class__  # noqa
        self.p[-1] = self.p[-1].replace("/>", ' fill-opacity="0.45"/>')

    def svg(self, name):
        body = "\n".join(self.p)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
                f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n<g id="{escape(name)}">\n'
                f'<rect width="{W}" height="{H}" fill="{BG}"/>\n{body}\n</g>\n</svg>\n')


def logo(s, x, y, h=40):
    w = h * 328 / 72
    s.add(f'<image id="Logo Centrale Pékin" x="{x}" y="{y}" width="{w:.0f}" height="{h}" '
          f'href="data:image/png;base64,{LOGO}"/>')
    return w


NAV = [("Accueil", "home"), ("Mes exercices", "ex"), ("Mes sujets", "suj"),
       ("Import / Export", "io"), ("Paramètres", "set"), ("Administration", "adm")]


def shell(name, active, crumbs, title, subtitle=None, actions=()):
    s = S()
    # En-tête
    s.g("En-tête")
    s.rect(0, 0, W, 64, WHITE)
    s.line(0, 64, W, 64)
    logo(s, 24, 14, 36)
    s.line(200, 18, 200, 46)
    s.text(216, 38, "App FLE", 16, 600, NAVY)
    # langue + utilisateur
    s.rect(1092, 16, 64, 32, WHITE, BORDER, r=8)
    s.text(1108, 37, "FR", 13, 600, TEXT)
    s.path("M1138 30 L1142 34 L1146 30", MUTED)
    s.circle(1188, 32, 16, NAVY_L)
    s.text(1188, 37, "CG", 12, 600, NAVY, "middle")
    s.text(1212, 30, "Corentin Godard", 13, 600, TEXT)
    s.text(1212, 46, "Enseignant · Admin", 12, 400, MUTED)
    s.text(1416, 37, "Déconnexion", 13, 500, RED, "end")
    s.end()
    # Barre latérale
    s.g("Navigation latérale")
    s.rect(0, 65, 240, H - 65, WHITE)
    s.line(240, 65, 240, H)
    y = 92
    for label, key in NAV:
        if key == "adm":
            s.line(24, y + 2, 216, y + 2)
            y += 16
        if key == active:
            s.rect(12, y, 216, 40, NAVY_L, r=8)
            s.rect(12, y + 8, 3, 24, RED, r=1.5)
        s.text(32, y + 25, label, 14, 600 if key == active else 500, NAVY if key == active else TEXT)
        if key == "adm":
            s.badge(158, y + 9, "admin", RED, RED_L)
        y += 44
    s.text(24, H - 24, "v1.0 · Centrale Pékin", 12, 400, "#9A9DAB")
    s.end()
    # Titre de page
    s.g("Titre de page")
    x = 280
    for i, c in enumerate(crumbs):
        last = i == len(crumbs) - 1
        s.text(x, 104, c, 13, 500 if last else 400, TEXT if last else MUTED)
        x += tw(c, 13) + 6
        if not last:
            s.text(x, 104, "/", 13, 400, "#B9BCC8")
            x += 14
    s.text(280, 140, title, 26, 700, TEXT)
    if subtitle:
        s.text(280, 164, subtitle, 14, 400, MUTED)
    ax = 1400
    for label, kind in reversed(actions):
        bw = int(tw(label, 14, 600) + 36)
        ax -= bw
        s.button(ax, 116, label, kind, bw)
        ax -= 12
    s.end()
    return s


def type_badge(t):
    m = {"QCM": (NAVY, NAVY_L), "Texte à trous": (GREEN, GREEN_L),
         "Vrai / Faux": (AMBER, AMBER_L), "Association": (RED, RED_L)}
    fg, bg = m[t]
    return lambda s, x, y: s.badge(x, y - 11, t, fg, bg)


def mk(s, fn):
    return lambda x, y: fn(s, x, y)


EXOS = [
    ("Les articles définis", "QCM", "A1", "Grammaire", "05/11/2026"),
    ("Passé composé ou imparfait ?", "Texte à trous", "B1", "Conjugaison", "03/11/2026"),
    ("La vie à Paris", "Vrai / Faux", "A2", "Compréhension écrite", "28/10/2026"),
    ("Vocabulaire de la cuisine", "Association", "A2", "Lexique", "24/10/2026"),
    ("Les pronoms COD / COI", "QCM", "B1", "Grammaire", "20/10/2026"),
    ("Le subjonctif présent", "Texte à trous", "B2", "Conjugaison", "15/10/2026"),
    ("Expressions de la météo", "Association", "A1", "Lexique", "12/10/2026"),
    ("Un week-end à Lyon", "Vrai / Faux", "A2", "Compréhension écrite", "08/10/2026"),
]

screens = {}

# ============ 01 Connexion ============
s = S()
s.g("Panneau identité")
s.rect(0, 0, 640, H, NAVY)
s.rect(0, 0, 8, H, RED)
s.text(80, 380, "Centrale App FLE", 40, 700, WHITE)
s.text(80, 424, "Créez, réutilisez et partagez vos exercices", 18, 400, "#C9CCF2")
s.text(80, 450, "de français langue étrangère.", 18, 400, "#C9CCF2")
s.text(80, H - 48, "École Centrale de Pékin · 北航中法工程师学院", 13, 400, "#9EA2DC")
s.end()
s.g("Formulaire de connexion")
logo(s, 840, 200, 56)
s.text(840, 330, "Connexion", 28, 700, TEXT)
s.text(840, 358, "Accédez à votre bibliothèque d’exercices.", 15, 400, MUTED)
s.field(840, 410, 400, "Identifiant", "cgodard2026")
s.field(840, 490, 400, "Mot de passe", "••••••••••")
s.text(1240, 474, "Mot de passe oublié ?", 13, 500, NAVY, "end")
s.g("Message d’erreur")
s.rect(840, 550, 400, 48, RED_L, "#F0C9CB", r=8)
s.circle(862, 574, 9, RED)
s.text(862, 579, "!", 13, 700, WHITE, "middle")
s.text(882, 579, "Identifiant ou mot de passe incorrect. Réessayez.", 13, 500, RED)
s.end()
s.button(840, 622, "Se connecter", "primary", 400, 44)
s.rect(1352, 24, 64, 32, WHITE, BORDER, r=8)
s.text(1368, 45, "FR", 13, 600, TEXT)
s.path("M1398 38 L1402 42 L1406 38", MUTED)
s.end()
screens["01 Connexion"] = s

# ============ 02 Menu principal ============
s = shell("02", "home", ["Accueil"], "Bonjour Corentin", "Que souhaitez-vous faire aujourd’hui ?")
tiles = [("Mes exercices", "128 exercices dans votre base", "Créer, rechercher, modifier"),
         ("Mes sujets", "14 sujets composés", "Composer, exporter, variantes"),
         ("Import / Export", "Échanger avec vos collègues", "Paquets d’échange .fle"),
         ("Paramètres", "Dernière sauvegarde : hier", "Sauvegarde, restauration, compte")]
for i, (t, a, b) in enumerate(tiles):
    x = 280 + i * 284
    s.g(f"Tuile / {t}")
    s.card(x, 196, 268, 168, t)
    s.rect(x + 24, 220, 40, 40, NAVY_L if i else RED_L, r=10)
    s.rect(x + 36, 232, 16, 16, NAVY if i else RED, r=3)
    s.text(x + 24, 296, t, 18, 700, TEXT)
    s.text(x + 24, 320, a, 14, 400, MUTED)
    s.text(x + 24, 344, b + "  →", 13, 600, NAVY)
    s.end()
s.text(280, 418, "Actions rapides", 16, 700, TEXT)
s.button(280, 436, "+ Nouvel exercice", "primary")
s.button(450, 436, "+ Nouveau sujet", "secondary")
s.button(612, 436, "Importer un paquet", "secondary")
s.text(280, 524, "Récemment modifiés", 16, 700, TEXT)
s.table(280, 540, [("Titre", 420), ("Type", 200), ("Niveau", 120), ("Thème", 200), ("Modifié le", 180)],
        [[e[0], mk(s, type_badge(e[1])), e[2], e[3], e[4]] for e in EXOS[:5]], row_h=52, name="Récents")
screens["02 Menu principal"] = s

# ============ 03 Mes exercices ============
s = shell("03", "ex", ["Accueil", "Mes exercices"], "Mes exercices", "128 exercices",
          [("Importer", "secondary"), ("+ Nouvel exercice", "primary")])
s.g("Barre de recherche et filtres")
s.search(280, 192, 440, "Rechercher par mot-clé…")
s.field(736, 192, 160, "", "Type : Tous", select=True)
s.field(908, 192, 150, "", "Niveau : A2, B1", select=True)
s.field(1070, 192, 170, "", "Thème : Tous", select=True)
s.field(1252, 192, 148, "", "Trier : Date ↓", select=True)
s.end()
s.g("Filtres actifs")
s.text(280, 266, "Filtres :", 13, 500, MUTED)
s.badge(340, 252, "Niveau A2  ×")
s.badge(432, 252, "Niveau B1  ×")
s.text(524, 266, "Tout effacer", 13, 500, NAVY)
s.end()
def sel(on):
    return lambda x, y: s.checkbox(x, y - 9, on)
def acts(x, y):
    s.text(x, y + 5, "Ouvrir", 13, 600, NAVY); s.kebab(x + 80, y - 6)
rows = [[sel(False), e[0], mk(s, type_badge(e[1])), e[2], e[3], e[4], acts] for e in EXOS]
s.table(280, 288, [("", 48), ("Titre", 360), ("Type", 170), ("Niveau", 100), ("Thème", 190), ("Créé le", 132), ("", 120)],
        rows, row_h=56, name="Liste des exercices", sort_col=5)
s.g("Pagination")
s.text(280, 856, "1–8 sur 128", 13, 400, MUTED)
for i, p in enumerate(["‹", "1", "2", "3", "…", "16", "›"]):
    x = 1148 + i * 36
    s.rect(x, 836, 32, 32, NAVY if p == "1" else WHITE, None if p == "1" else BORDER, r=8)
    s.text(x + 16, 857, p, 13, 600, WHITE if p == "1" else TEXT, "middle")
s.end()
screens["03 Mes exercices — liste"] = s

# ============ 04 Détail exercice ============
def detail_exo(s):
    s.g("Aperçu de l’exercice")
    s.card(280, 196, 760, 660, "Aperçu")
    s.text(312, 236, "APERÇU", 11, 600, MUTED)
    s.rect(820, 218, 196, 32, BG, r=8)
    s.rect(822, 220, 96, 28, WHITE, BORDER, r=7)
    s.text(870, 239, "Élève", 13, 600, TEXT, "middle")
    s.text(966, 239, "Enseignant", 13, 500, MUTED, "middle")
    s.text(312, 284, "Consigne : choisissez l’article défini qui convient.", 15, 600, TEXT)
    qs = [("1. ___ maison est grande.", ["le", "la", "les"], 1),
          ("2. ___ enfants jouent dans le jardin.", ["le", "la", "les"], 2),
          ("3. ___ soleil brille aujourd’hui.", ["le", "la", "l’"], 0),
          ("4. ___ école ferme à 17 h.", ["le", "la", "l’"], 2)]
    y = 330
    for q, opts, _ in qs:
        s.text(312, y, q, 15, 500, TEXT)
        for j, o in enumerate(opts):
            s.checkbox(332 + j * 120, y + 18, False, radio=True)
            s.text(360 + j * 120, y + 32, o, 14, 400, TEXT)
        y += 84
    s.line(312, 680, 1008, 680)
    s.text(312, 712, "Aperçu tel qu’il apparaîtra dans le document exporté (version élève, sans corrigé).", 13, 400, MUTED)
    s.end()
    s.g("Métadonnées")
    s.card(1064, 196, 336, 380, "Informations")
    s.text(1088, 232, "Informations", 16, 700, TEXT)
    meta = [("Type", None), ("Niveau", "A1"), ("Thème", "Grammaire"), ("Mots-clés", "article, déterminant"),
            ("Auteur", "C. Godard"), ("Créé le", "05/11/2026"), ("Modifié le", "06/11/2026"), ("Version", "3")]
    y = 272
    for k, v in meta:
        s.text(1088, y, k, 13, 400, MUTED)
        if v: s.text(1376, y, v, 13, 600, TEXT, "end")
        else: s.badge(1376 - tw("QCM", 12, 600) - 16, y - 15, "QCM")
        y += 36
    s.end()
    s.g("Utilisé dans")
    s.card(1064, 592, 336, 132, "Utilisé dans")
    s.text(1088, 626, "Utilisé dans 2 sujets", 14, 700, TEXT)
    s.text(1088, 656, "• Évaluation A1 — novembre", 13, 400, NAVY)
    s.text(1088, 682, "• Révisions grammaire S1", 13, 400, NAVY)
    s.end()

s = shell("04", "ex", ["Accueil", "Mes exercices", "Les articles définis"], "Les articles définis", None,
          [("Supprimer", "danger-ghost"), ("Dupliquer", "secondary"), ("Modifier", "primary")])
detail_exo(s)
screens["04 Détail d’un exercice"] = s

# ============ 04b Confirmation suppression ============
s = shell("04b", "ex", ["Accueil", "Mes exercices", "Les articles définis"], "Les articles définis", None,
          [("Supprimer", "danger-ghost"), ("Dupliquer", "secondary"), ("Modifier", "primary")])
detail_exo(s)
s.modal_backdrop()
s.g("Modale de confirmation")
s.rect(520, 300, 480, 280, WHITE, r=16)
s.circle(564, 352, 20, RED_L)
s.text(564, 359, "!", 18, 700, RED, "middle")
s.text(600, 359, "Supprimer cet exercice ?", 20, 700, TEXT)
s.text(552, 408, "« Les articles définis » sera retiré de votre bibliothèque", 14, 400, TEXT)
s.text(552, 430, "et des résultats de recherche.", 14, 400, TEXT)
s.rect(552, 450, 416, 54, AMBER_L, r=8)
s.text(568, 472, "Cet exercice est utilisé dans 2 sujets. Les documents", 13, 500, AMBER)
s.text(568, 492, "déjà exportés ne seront pas modifiés.", 13, 500, AMBER)
s.button(744, 520, "Annuler", "secondary", 100)
s.button(856, 520, "Supprimer", "danger", 112)
s.end()
screens["04b Confirmation de suppression"] = s

# ============ 05 Choix du type ============
s = shell("05", "ex", ["Accueil", "Mes exercices", "Nouvel exercice"], "Nouvel exercice",
          "Étape 1 sur 2 — choisissez le type d’exercice", [("Annuler", "secondary")])
types = [("QCM", "Une question, plusieurs réponses proposées, une ou plusieurs bonnes réponses.", NAVY, NAVY_L),
         ("Texte à trous", "Un texte dont certains mots sont masqués et doivent être complétés.", GREEN, GREEN_L),
         ("Vrai / Faux", "Une série d’affirmations à juger vraies ou fausses.", AMBER, AMBER_L),
         ("Association", "Des paires d’éléments à relier (mot ↔ définition, image ↔ mot…).", RED, RED_L)]
for i, (t, d, fg, bg) in enumerate(types):
    x = 280 + (i % 2) * 568
    y = 200 + (i // 2) * 236
    s.g(f"Type / {t}")
    selected = i == 0
    s.rect(x, y, 552, 212, WHITE, NAVY if selected else BORDER, r=12, sw=2 if selected else 1)
    s.rect(x + 28, y + 28, 56, 56, bg, r=12)
    # pictogrammes simples
    if t == "QCM":
        for k in range(3):
            s.checkbox(x + 40, y + 37 + k * 13 - 4, k == 1, radio=True) if False else None
            s.circle(x + 44, y + 42 + k * 14, 4, fg if k == 1 else WHITE, fg, 1.5)
            s.rect(x + 54, y + 40 + k * 14, 18, 4, fg, r=2)
    elif t == "Texte à trous":
        s.rect(x + 40, y + 46, 12, 4, fg, r=2); s.rect(x + 56, y + 44, 16, 8, WHITE, fg, r=2, dash="2 2")
        s.rect(x + 40, y + 60, 32, 4, fg, r=2)
    elif t == "Vrai / Faux":
        s.path(f"M{x+40} {y+56} L{x+46} {y+62} L{x+56} {y+48}", fg, sw=2.5)
        s.path(f"M{x+62} {y+48} L{x+72} {y+60} M{x+72} {y+48} L{x+62} {y+60}", fg, sw=2.5)
    else:
        s.circle(x + 44, y + 46, 4, fg); s.circle(x + 68, y + 66, 4, fg)
        s.circle(x + 44, y + 66, 4, fg); s.circle(x + 68, y + 46, 4, fg)
        s.path(f"M{x+44} {y+46} L{x+68} {y+66} M{x+44} {y+66} L{x+68} {y+46}", fg, sw=1.5)
    s.text(x + 28, y + 124, t, 20, 700, TEXT)
    words = d.split(" ")
    line, ly = "", y + 154
    for w_ in words:
        if tw(line + " " + w_, 14) > 480:
            s.text(x + 28, ly, line.strip(), 14, 400, MUTED); line, ly = "", ly + 22
        line += " " + w_
    s.text(x + 28, ly, line.strip(), 14, 400, MUTED)
    if selected:
        s.circle(x + 516, y + 36, 12, NAVY)
        s.path(f"M{x+510} {y+36} L{x+514} {y+40} L{x+522} {y+32}", WHITE, sw=2)
    s.end()
s.button(1260, 692, "Continuer  →", "primary", 140)
screens["05 Choix du type d’exercice"] = s


# ============ 06 Éditeurs ============
def editor(type_name, title_value, consigne, body_fn, crumb_title):
    s = shell("06", "ex", ["Accueil", "Mes exercices", crumb_title], crumb_title,
              f"Étape 2 sur 2 — {type_name}", [("Annuler", "secondary"), ("Aperçu", "secondary"), ("Enregistrer", "primary")])
    s.g("Informations générales")
    s.card(280, 196, 1120, 168, "Informations générales")
    s.field(304, 236, 520, "Titre", title_value)
    s.field(840, 236, 120, "Niveau", "A1", select=True)
    s.field(976, 236, 200, "Thème", "Grammaire", select=True)
    s.field(1192, 236, 184, "Type", type_name, select=True)
    s.field(304, 308, 1072, "Mots-clés", "article, déterminant, genre")
    s.end()
    s.g("Consigne")
    s.card(280, 380, 1120, 96, "Consigne")
    s.field(304, 420, 1072, "Consigne *", consigne)
    s.end()
    s.g("Contenu de l’exercice")
    s.card(280, 492, 1120, 384, "Contenu")
    body_fn(s)
    s.end()
    return s


def qcm_body(s):
    s.text(304, 528, "Questions", 16, 700, TEXT)
    s.text(1376, 528, "Cochez la ou les bonnes réponses", 13, 400, MUTED, "end")
    qs = [("___ maison est grande.", ["le", "la", "les"], 1),
          ("___ enfants jouent dans le jardin.", ["le", "la", "les"], 2)]
    y = 548
    for i, (q, opts, ok) in enumerate(qs):
        s.g(f"Question {i+1}")
        s.rect(304, y, 1072, 132, BG, r=10)
        s.handle(318, y + 22)
        s.text(340, y + 34, f"{i+1}.", 14, 700, MUTED)
        s.rect(364, y + 14, 940, 36, WHITE, BORDER, r=8)
        s.text(376, y + 37, q, 14, 400, TEXT)
        s.kebab(1352, y + 24)
        for j, o in enumerate(opts):
            x = 364 + j * 236
            s.checkbox(x, y + 66, j == ok)
            s.rect(x + 28, y + 60, 190, 32, WHITE, NAVY if j == ok else BORDER, r=8)
            s.text(x + 40, y + 81, o, 14, 500 if j == ok else 400, TEXT)
        s.text(1080, y + 81, "+ Ajouter une réponse", 13, 600, NAVY)
        s.text(364, y + 118, "Explication (facultatif) : « maison » est un nom féminin.", 12, 400, MUTED)
        s.end()
        y += 148
    s.button(304, 844 - 8, "+ Ajouter une question", "ghost", 200, 36)


def trous_body(s):
    s.text(304, 528, "Texte", 16, 700, TEXT)
    s.text(1376, 528, "Sélectionnez un mot puis « Créer un trou »", 13, 400, MUTED, "end")
    s.rect(304, 548, 1072, 44, BG, r=8)
    s.button(312, 554, "Créer un trou", "secondary", 130, 32, 13)
    s.button(450, 554, "Retirer le trou", "secondary", 136, 32, 13)
    s.rect(304, 592, 1072, 132, WHITE, BORDER, r=8)
    parts = [("Hier, je ", 0), ("suis allé", 1), (" au marché. Il ", 0), ("faisait", 1), (" beau et", 0)]
    x, y = 320, 628
    for t_, hole in parts:
        if hole:
            w_ = tw(t_, 15) + 20
            s.rect(x, y - 19, w_, 26, GREEN_L, GREEN, r=6)
            s.text(x + 10, y, t_, 15, 600, GREEN)
            x += w_ + 4
        else:
            s.text(x, y, t_, 15, 400, TEXT); x += tw(t_, 15)
    x, y = 320, 664
    for t_, hole in [("les gens ", 0), ("se promenaient", 1), (" tranquillement.", 0)]:
        if hole:
            w_ = tw(t_, 15) + 20
            s.rect(x, y - 19, w_, 26, GREEN_L, GREEN, r=6); s.text(x + 10, y, t_, 15, 600, GREEN); x += w_ + 4
        else:
            s.text(x, y, t_, 15, 400, TEXT); x += tw(t_, 15)
    s.text(304, 760, "Trous et réponses acceptées", 14, 700, TEXT)
    for i, (a, alt) in enumerate([("suis allé", "suis allée"), ("faisait", "—"), ("se promenaient", "—")]):
        x = 304 + i * 360
        s.rect(x, 776, 344, 64, BG, r=8)
        s.text(x + 14, 800, f"Trou {i+1} : {a}", 13, 600, TEXT)
        s.text(x + 14, 824, f"Variante acceptée : {alt}", 12, 400, MUTED)


def vf_body(s):
    s.text(304, 528, "Affirmations", 16, 700, TEXT)
    s.text(1376, 528, "Indiquez la valeur attendue", 13, 400, MUTED, "end")
    items = [("Le narrateur habite à Paris depuis 3 ans.", True),
             ("Il prend le métro tous les matins.", False),
             ("Son quartier préféré est le Marais.", True),
             ("Il trouve les loyers peu élevés.", False)]
    y = 548
    for i, (t_, v) in enumerate(items):
        s.g(f"Affirmation {i+1}")
        s.rect(304, y, 1072, 60, BG, r=10)
        s.handle(318, y + 24)
        s.text(340, y + 35, f"{i+1}.", 14, 700, MUTED)
        s.rect(364, y + 12, 760, 36, WHITE, BORDER, r=8)
        s.text(376, y + 35, t_, 14, 400, TEXT)
        s.rect(1140, y + 12, 200, 36, WHITE, BORDER, r=8)
        s.rect(1142 if v else 1240, y + 14, 98, 32, GREEN_L if v else RED_L, r=7)
        s.text(1190, y + 35, "Vrai", 13, 600 if v else 400, GREEN if v else MUTED, "middle")
        s.text(1290, y + 35, "Faux", 13, 400 if v else 600, MUTED if v else RED, "middle")
        s.kebab(1360, y + 24)
        s.end()
        y += 70
    s.button(304, 836, "+ Ajouter une affirmation", "ghost", 220, 36)


def asso_body(s):
    s.text(304, 528, "Paires à associer", 16, 700, TEXT)
    s.text(1376, 528, "L’ordre de la colonne B sera mélangé à l’export", 13, 400, MUTED, "end")
    s.text(364, 566, "COLONNE A", 11, 600, MUTED)
    s.text(872, 566, "COLONNE B", 11, 600, MUTED)
    pairs = [("une casserole", "ustensile pour faire bouillir"), ("éplucher", "retirer la peau d’un légume"),
             ("une poêle", "ustensile pour faire frire"), ("mijoter", "cuire lentement à feu doux")]
    y = 580
    for i, (a, b) in enumerate(pairs):
        s.g(f"Paire {i+1}")
        s.handle(318, y + 12)
        s.rect(340, y, 480, 40, WHITE, BORDER, r=8)
        s.text(354, y + 25, a, 14, 500, TEXT)
        s.line(824, y + 20, 864, y + 20, RED, 1.5)
        s.circle(824, y + 20, 3.5, RED); s.circle(864, y + 20, 3.5, RED)
        s.rect(868, y, 480, 40, WHITE, BORDER, r=8)
        s.text(882, y + 25, b, 14, 400, TEXT)
        s.kebab(1362, y + 14)
        s.end()
        y += 54
    s.button(304, 836, "+ Ajouter une paire", "ghost", 180, 36)


screens["06a Édition — QCM"] = editor("QCM", "Les articles définis",
                                      "Choisissez l’article défini qui convient.", qcm_body, "Modifier l’exercice")
screens["06b Édition — Texte à trous"] = editor("Texte à trous", "Passé composé ou imparfait ?",
                                                "Complétez le texte avec les verbes conjugués.", trous_body, "Nouvel exercice")
screens["06c Édition — Vrai / Faux"] = editor("Vrai / Faux", "La vie à Paris",
                                              "Lisez le texte puis indiquez si les affirmations sont vraies ou fausses.", vf_body, "Nouvel exercice")
screens["06d Édition — Association"] = editor("Association", "Vocabulaire de la cuisine",
                                              "Associez chaque mot à sa définition.", asso_body, "Nouvel exercice")

# ============ 07 Mes sujets ============
SUJETS = [("Évaluation A1 — novembre", 6, "A1", "06/11/2026", "Exporté"),
          ("Révisions grammaire S1", 8, "A2", "02/11/2026", "Brouillon"),
          ("Contrôle B1 — temps du passé", 5, "B1", "29/10/2026", "Exporté"),
          ("Lexique : la maison", 4, "A2", "22/10/2026", "Exporté"),
          ("Compréhension écrite — semaine 6", 3, "B1", "15/10/2026", "Brouillon"),
          ("Évaluation diagnostique", 10, "A1–B1", "02/10/2026", "Exporté")]
s = shell("07", "suj", ["Accueil", "Mes sujets"], "Mes sujets", "14 sujets", [("+ Nouveau sujet", "primary")])
s.search(280, 192, 520, "Rechercher un sujet…")
s.field(816, 192, 180, "", "Trier : Date ↓", select=True)
def status(st):
    return lambda x, y: s.badge(x, y - 11, st, GREEN if st == "Exporté" else MUTED, GREEN_L if st == "Exporté" else BG)
def acts2(x, y):
    s.text(x, y + 5, "Ouvrir", 13, 600, NAVY); s.kebab(x + 80, y - 6)
s.table(280, 256, [("Titre", 440), ("Exercices", 140), ("Niveau", 120), ("Modifié le", 160), ("Statut", 140), ("", 120)],
        [[t, str(n), lv, d, status(st), acts2] for t, n, lv, d, st in SUJETS], row_h=60, name="Liste des sujets", sort_col=3)
screens["07 Mes sujets — liste"] = s

# ============ 08 Détail sujet ============
s = shell("08", "suj", ["Accueil", "Mes sujets", "Évaluation A1 — novembre"], "Évaluation A1 — novembre",
          "6 exercices · niveau A1 · modifié le 06/11/2026",
          [("Générer une variante", "secondary"), ("Modifier", "primary")])
s.g("Contenu du sujet")
s.card(280, 196, 740, 660, "Exercices du sujet")
s.text(304, 232, "Exercices (dans l’ordre)", 16, 700, TEXT)
s.text(304, 258, "Consigne générale : répondez sur la feuille, durée 45 minutes.", 13, 400, MUTED)
for i, (t, ty, lv, th, _) in enumerate(EXOS[:6]):
    y = 280 + i * 92
    s.rect(304, y, 692, 80, BG, r=10)
    s.circle(336, y + 40, 16, WHITE, BORDER)
    s.text(336, y + 45, str(i + 1), 14, 700, NAVY, "middle")
    s.text(368, y + 34, t, 15, 600, TEXT)
    s.text(368, y + 58, f"{lv} · {th}", 13, 400, MUTED)
    type_badge(ty)(s, 996 - tw(ty, 12, 600) - 32, y + 40)
s.end()
s.g("Export")
s.card(1044, 196, 356, 368, "Exporter")
s.text(1068, 232, "Exporter le sujet", 16, 700, TEXT)
s.text(1068, 270, "Format", 13, 500, TEXT)
s.rect(1068, 282, 308, 40, BG, r=8)
s.rect(1070, 284, 152, 36, WHITE, BORDER, r=7)
s.text(1146, 307, "PDF", 13, 600, TEXT, "middle")
s.text(1300, 307, "HTML", 13, 500, MUTED, "middle")
s.text(1068, 356, "Version", 13, 500, TEXT)
s.checkbox(1068, 370, True); s.text(1096, 384, "Élève (sans corrigé)", 14, 400, TEXT)
s.checkbox(1068, 402, True); s.text(1096, 416, "Enseignant (avec corrigé)", 14, 400, TEXT)
s.text(1068, 456, "Variantes", 13, 500, TEXT)
s.field(1068, 468, 120, "", "1", select=True)
s.text(1200, 493, "version(s) à générer", 13, 400, MUTED)
s.button(1068, 512, "Exporter", "primary", 308)
s.end()
s.g("Variantes")
s.card(1044, 580, 356, 180, "Variantes")
s.text(1068, 614, "Variantes générées", 16, 700, TEXT)
for i, (v, d) in enumerate([("Variante A", "06/11/2026"), ("Variante B", "06/11/2026")]):
    y = 640 + i * 52
    s.rect(1068, y, 308, 44, BG, r=8)
    s.text(1084, y + 27, v, 14, 600, TEXT)
    s.text(1360, y + 27, "Exporter", 13, 600, NAVY, "end")
    s.text(1260, y + 27, d, 12, 400, MUTED, "end")
s.end()
screens["08 Détail d’un sujet"] = s

# ============ 09 Composition ============
s = shell("09", "suj", ["Accueil", "Mes sujets", "Composition"], "Composer un sujet", None,
          [("Annuler", "secondary"), ("Enregistrer", "primary")])
s.g("Banque d’exercices")
s.card(280, 196, 540, 680, "Banque d’exercices")
s.text(304, 232, "Banque d’exercices", 16, 700, TEXT)
s.search(304, 248, 492, "Rechercher…")
s.field(304, 300, 156, "", "Type", select=True)
s.field(472, 300, 156, "", "Niveau", select=True)
s.field(640, 300, 156, "", "Thème", select=True)
chosen = {0, 1, 3}
for i, (t, ty, lv, th, _) in enumerate(EXOS[:7]):
    y = 356 + i * 72
    s.rect(304, y, 492, 62, BG if i in chosen else WHITE, None if i in chosen else BORDER, r=10)
    s.text(320, y + 26, t, 14, 600, MUTED if i in chosen else TEXT)
    s.text(320, y + 47, f"{ty} · {lv} · {th}", 12, 400, MUTED)
    if i in chosen:
        s.text(780, y + 36, "Ajouté ✓", 12, 600, GREEN, "end")
    else:
        s.rect(740, y + 15, 40, 32, WHITE, BORDER, r=8)
        s.text(760, y + 37, "+", 18, 600, NAVY, "middle")
s.end()
s.g("Sujet en cours")
s.card(844, 196, 556, 680, "Sujet")
s.field(868, 236, 508, "Titre du sujet", "Évaluation A1 — novembre")
s.field(868, 312, 508, "Consigne générale", "Répondez sur la feuille, durée 45 minutes.")
s.text(868, 386, "Exercices sélectionnés (3)", 14, 700, TEXT)
s.text(1376, 386, "Glissez pour réordonner", 12, 400, MUTED, "end")
for i, k in enumerate([0, 1, 3]):
    t, ty, lv, th, _ = EXOS[k]
    y = 400 + i * 72
    drag = i == 1
    s.rect(868 + (8 if drag else 0), y, 508, 62, WHITE, NAVY if drag else BORDER, r=10, sw=2 if drag else 1)
    s.handle(884 + (8 if drag else 0), y + 25)
    s.text(906 + (8 if drag else 0), y + 37, f"{i+1}.", 14, 700, NAVY)
    s.text(932 + (8 if drag else 0), y + 30, t, 14, 600, TEXT)
    s.text(932 + (8 if drag else 0), y + 50, f"{ty} · {lv}", 12, 400, MUTED)
    s.text(1360, y + 37, "Retirer", 12, 600, RED, "end")
s.rect(868, 620, 508, 62, WHITE, "#B9BCC8", r=10, dash="5 4")
s.text(1122, 656, "Ajoutez des exercices depuis la banque", 13, 400, MUTED, "middle")
s.end()
screens["09 Composition d’un sujet"] = s

# ============ 10 Import / Export ============
s = shell("10", "io", ["Accueil", "Import / Export"], "Import / Export",
          "Échangez des exercices avec d’autres enseignants via des paquets .fle")
s.g("Exporter un paquet")
s.card(280, 196, 548, 640, "Exporter")
s.text(304, 236, "Exporter un paquet", 18, 700, TEXT)
s.text(304, 262, "Sélectionnez les exercices à partager.", 14, 400, MUTED)
s.search(304, 284, 500, "Filtrer…")
s.checkbox(304, 344, True); s.text(332, 358, "Tout sélectionner (6)", 13, 600, TEXT)
for i, (t, ty, lv, *_r) in enumerate(EXOS[:6]):
    y = 380 + i * 52
    s.line(304, y, 804, y)
    s.checkbox(304, y + 17, i != 4)
    s.text(332, y + 31, t, 14, 500, TEXT)
    s.text(804, y + 31, f"{ty} · {lv}", 12, 400, MUTED, "end")
s.field(304, 718, 500, "Nom du fichier", "exercices_godard_2026-11-08.fle")
s.button(304, 776, "Exporter 5 exercices", "primary", 500)
s.end()
s.g("Importer un paquet")
s.card(852, 196, 548, 640, "Importer")
s.text(876, 236, "Importer un paquet", 18, 700, TEXT)
s.text(876, 262, "Vos exercices existants ne seront jamais remplacés sans accord.", 14, 400, MUTED)
s.rect(876, 288, 500, 200, BG, "#B9BCC8", r=12, dash="6 5")
s.path("M1126 352 L1126 384 M1114 364 L1126 352 L1138 364", NAVY, sw=2)
s.line(1110, 392, 1142, 392, NAVY, 2)
s.text(1126, 428, "Déposez un fichier .fle ici", 15, 600, TEXT, "middle")
s.text(1126, 452, "ou cliquez pour parcourir", 13, 400, NAVY, "middle")
s.text(876, 528, "Fichier sélectionné", 13, 500, TEXT)
s.rect(876, 540, 500, 60, WHITE, BORDER, r=10)
s.rect(890, 552, 36, 36, NAVY_L, r=8)
s.text(908, 575, ".fle", 10, 700, NAVY, "middle")
s.text(940, 566, "paquet_lefebvre_A2.fle", 14, 600, TEXT)
s.text(940, 586, "20 exercices · format v1 · 48 Ko", 12, 400, MUTED)
s.rect(876, 616, 500, 78, AMBER_L, r=10)
s.text(892, 644, "Analyse terminée : 16 nouveaux exercices,", 13, 600, AMBER)
s.text(892, 666, "3 doublons et 1 conflit détectés.", 13, 600, AMBER)
s.button(876, 776, "Analyser et importer", "primary", 500)
s.end()
s.g("Confirmation (toast)")
s.rect(1040, 40, 0, 0, WHITE)
s.end()
screens["10 Import / Export"] = s

# ============ 11 Conflits ============
s = shell("11", "io", ["Accueil", "Import / Export", "Résolution des conflits"], "Résolution des doublons et conflits",
          "paquet_lefebvre_A2.fle · 4 cas à traiter", [("Annuler l’import", "secondary"), ("Valider l’import", "primary")])
s.g("Résumé")
for i, (n, l, fg, bg) in enumerate([("16", "Nouveaux", GREEN, GREEN_L), ("3", "Doublons", AMBER, AMBER_L),
                                     ("1", "Conflit", RED, RED_L), ("0", "Erreurs", MUTED, BG)]):
    x = 280 + i * 284
    s.rect(x, 196, 268, 76, WHITE, BORDER, r=12)
    s.rect(x + 16, 214, 40, 40, bg, r=10)
    s.text(x + 36, 240, n, 16, 700, fg, "middle")
    s.text(x + 72, 240, l, 15, 600, TEXT)
s.end()
cases = [("Les articles définis", "Conflit", "Même identifiant, contenu différent", 2),
         ("Vocabulaire de la cuisine", "Doublon", "Contenu identique", 0),
         ("Les pronoms COD / COI", "Doublon", "Même identifiant", 0),
         ("Expressions de la météo", "Doublon", "Contenu identique", 1)]
def kind(k):
    return lambda x, y: s.badge(x, y - 11, k, RED if k == "Conflit" else AMBER, RED_L if k == "Conflit" else AMBER_L)
def choice(c):
    def f(x, y):
        opts = ["Ignorer", "Importer comme copie", "Remplacer"]
        xx = x
        for j, o in enumerate(opts):
            s.checkbox(xx, y - 9, j == c, radio=True)
            s.text(xx + 26, y + 5, o, 13, 600 if j == c else 400, TEXT)
            xx += tw(o, 13) + 56
    return f
def compare(x, y):
    s.text(x, y + 5, "Comparer", 13, 600, NAVY)
s.table(280, 296, [("Exercice", 300), ("Cas", 120), ("Détail", 260), ("Action", 420), ("", 20)],
        [[t, kind(k), d, choice(c), None] for t, k, d, c in cases], row_h=64, name="Cas détectés")
s.g("Comparaison du conflit")
s.card(280, 620, 1120, 236, "Comparaison")
s.text(304, 656, "Comparaison — Les articles définis", 16, 700, TEXT)
for i, (lab, v, lines) in enumerate([("Votre version", "v3 · 06/11/2026", ["4 questions", "Niveau A1", "Consigne : choisissez l’article défini…"]),
                                      ("Version importée", "v2 · 01/11/2026", ["5 questions (+1)", "Niveau A1", "Consigne : complétez avec le bon article…"])]):
    x = 304 + i * 548
    s.rect(x, 676, 524, 156, BG, r=10)
    s.text(x + 16, 704, lab, 14, 700, TEXT)
    s.text(x + 508, 704, v, 12, 400, MUTED, "end")
    for j, l in enumerate(lines):
        s.text(x + 16, 736 + j * 26, l, 13, 400, RED if (i == 1 and j != 1) else TEXT)
s.end()
s.g("Avertissement remplacement")
s.rect(1040, 26, 0, 0, WHITE)
s.end()
screens["11 Résolution des conflits"] = s

# ============ 12 Paramètres ============
s = shell("12", "set", ["Accueil", "Paramètres"], "Paramètres et sauvegarde")
s.g("Compte")
s.card(280, 176, 548, 352, "Mon compte")
s.text(304, 214, "Mon compte", 18, 700, TEXT)
s.field(304, 258, 242, "Prénom", "Corentin")
s.field(562, 258, 242, "Nom", "Godard")
s.field(304, 334, 500, "Adresse e-mail", "corentin.godard@exemple.edu")
s.field(304, 410, 242, "Langue de l’interface", "Français", select=True)
s.button(562, 410, "Changer le mot de passe", "secondary", 242)
s.button(304, 472, "Enregistrer", "primary", 120)
s.end()
s.g("Sauvegarde")
s.card(852, 176, 548, 352, "Sauvegarde")
s.text(876, 214, "Sauvegarde de la base", 18, 700, TEXT)
s.text(876, 240, "Un fichier unique contenant tous vos exercices et sujets.", 14, 400, MUTED)
s.rect(876, 262, 500, 64, GREEN_L, r=10)
s.circle(900, 294, 10, GREEN)
s.path("M895 294 L899 298 L905 290", WHITE, sw=2)
s.text(920, 290, "Dernière sauvegarde : 07/11/2026 à 18:42", 13, 600, GREEN)
s.text(920, 310, "sauvegarde_app_fle_2026-11-07.zip · 2,4 Mo", 12, 400, GREEN)
s.text(876, 362, "Sauvegarde automatique hebdomadaire", 14, 500, TEXT)
s.toggle(1340, 348, True)
s.button(876, 400, "Sauvegarder maintenant", "primary", 500)
s.end()
s.g("Restauration")
s.card(280, 552, 1120, 220, "Restauration")
s.text(304, 590, "Restaurer une sauvegarde", 18, 700, TEXT)
s.text(304, 616, "La base actuelle sera remplacée par l’état de la sauvegarde choisie.", 14, 400, MUTED)
s.table(304, 636, [("Sauvegarde", 520), ("Date", 260), ("Taille", 160), ("", 132)],
        [["sauvegarde_app_fle_2026-11-07.zip", "07/11/2026 18:42", "2,4 Mo",
          lambda x, y: s.text(x, y + 5, "Restaurer", 13, 600, RED)]], row_h=48, name="Sauvegardes")
s.button(304, 740 - 0, "Restaurer depuis un fichier…", "secondary", 240, 36) if False else None
s.end()
screens["12 Paramètres et sauvegarde"] = s

# ============ 13 Gestion des comptes ============
s = shell("13", "adm", ["Accueil", "Administration"], "Gestion des comptes",
          "Réservé aux administrateurs", [("+ Nouveau compte", "primary")])
s.search(280, 192, 440, "Rechercher un utilisateur…")
s.field(736, 192, 180, "", "Rôle : Tous", select=True)
USERS = [("Grégory Lefebvre", "gregory.lefebvre@exemple.edu", "Admin", "Actif", "08/11/2026"),
         ("Corentin Godard", "corentin.godard@exemple.edu", "Admin", "Actif", "08/11/2026"),
         ("Maxence Schwerer", "maxence.schwerer@exemple.edu", "Enseignant", "Actif", "07/11/2026"),
         ("Li Wei", "li.wei@exemple.edu", "Enseignant", "Actif", "04/11/2026"),
         ("Claire Martin", "claire.martin@exemple.edu", "Enseignant", "Désactivé", "12/09/2026")]
def role(r):
    return lambda x, y: s.badge(x, y - 11, r, RED if r == "Admin" else NAVY, RED_L if r == "Admin" else NAVY_L)
def st(v):
    return lambda x, y: s.badge(x, y - 11, v, GREEN if v == "Actif" else MUTED, GREEN_L if v == "Actif" else BG)
def ua(x, y):
    s.text(x, y + 5, "Modifier", 13, 600, NAVY); s.kebab(x + 86, y - 6)
s.table(280, 256, [("Nom", 260), ("E-mail", 320), ("Rôle", 120), ("Statut", 120), ("Dernière connexion", 180), ("", 120)],
        [[n, m, role(r), st(v), d, ua] for n, m, r, v, d in USERS], row_h=60, name="Comptes")
screens["13 Gestion des comptes (admin)"] = s

for name, sc in screens.items():
    fn = name.split(" ")[0] + ".svg"
    open(os.path.join(OUT, fn), "w", encoding="utf-8").write(sc.svg(name))
print("\n".join(screens))
