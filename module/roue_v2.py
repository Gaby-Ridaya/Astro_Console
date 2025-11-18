import matplotlib.pyplot as plt
import numpy as np
from rich.console import Console
from rich.table import Table

# Symboles des signes du zodiaque
signes_symbols = [
    "♈", "♉", "♊", "♋", "♌", "♍",
    "♎", "♏", "♐", "♑", "♒", "♓"
]

# Dictionnaire pour retrouver le symbole à partir du nom
planete_symbols = {
    "Soleil": "☉", "Lune": "☽", "Mercure": "☿", "Vénus": "♀", "Mars": "♂",
    "Jupiter": "♃", "Saturne": "♄", "Uranus": "♅", "Neptune": "♆", "Pluton": "♇",
    "Rahu": "☊", "Ketu": "☋"
}

def couleur_aspect(aspect_type):
    if aspect_type == "Conjonction":
        return "orange"
    elif aspect_type == "Opposition":
        return "blue"
    elif aspect_type == "Carré":
        return "red"
    elif aspect_type == "Trigone":
        return "green"
    elif aspect_type == "Sextile":
        return "purple"
    else:
        return "grey"

def plot_roue(planetes, maisons_deg, aspects, asc_deg, mc_deg):
    fig, ax = plt.subplots(figsize=(8,8), subplot_kw={'projection': 'polar'})
    fig.patch.set_facecolor('#f5ecd9')
    ax.set_facecolor('#f5ecd9')
    ax.set_theta_direction(1)
    offset = np.deg2rad(asc_deg) - np.pi  # Ascendant à gauche (9h)
    ax.set_theta_offset(offset)

    # Cercles pour les signes
    for r in [0.85, 1.2]:
        circle = plt.Circle((0,0), r, transform=ax.transData._b, fill=False, color='black', lw=2, zorder=20)
        ax.add_artist(circle)

    # Séparateurs des signes
    for i in range(12):
        angle = np.deg2rad(i*30)
        ax.plot([angle, angle], [0.98, 1.2], color='black', lw=1)

    # Signes du zodiaque
    for i, symbole in enumerate(signes_symbols):
        angle = np.deg2rad(i*30 + 15)
        ax.text(angle, 1.10, symbole, fontsize=31, ha='center', va='center', color='black', fontweight='bold', zorder=30)

    # Bande de couleur pour les maisons
    ax.bar(x=0, height=0.13, width=2*np.pi, bottom=0.85, color="#f3e9c6", alpha=0.5, align='center', edgecolor=None)

    rayon_planetes = 1.28

    # Affichage de l'ascendant et du MC
    asc_angle = np.deg2rad(asc_deg)
    mc_angle = np.deg2rad(mc_deg)
    ax.text(asc_angle, rayon_planetes, 'AS', fontsize=15, ha='center', va='center', color='black', fontweight='bold', zorder=22)
    ax.text(mc_angle, rayon_planetes, 'MC', fontsize=15, ha='center', va='center', color='black', fontweight='bold', zorder=22)

    # Couleurs pastel par élément (Feu, Terre, Air, Eau)
    element_colors = [
        "#FFD580", "#B5EAD7", "#C7CEEA", "#FFB7B2",
        "#FFD580", "#B5EAD7", "#C7CEEA", "#FFB7B2",
        "#FFD580", "#B5EAD7", "#C7CEEA", "#FFB7B2"
    ]

    # Remplir chaque case de signe
    for i in range(12):
        theta1 = i * 30
        ax.bar(
            x=np.deg2rad(theta1 + 15),
            height=0.35,
            width=np.deg2rad(30),
            bottom=0.85,
            color=element_colors[i],
            alpha=0.18,
            align='center',
            edgecolor=None
        )

    # Cases pour les maisons
    maison_colors = [
        "red", "saddlebrown", "green", "blue",
        "red", "saddlebrown", "green", "blue",
        "red", "saddlebrown", "green", "blue"
    ]
    for i in range(12):
        theta1 = maisons_deg[i]
        theta2 = maisons_deg[(i+1)%12]
        delta = (theta2 - theta1) % 360
        center_angle = (theta1 + delta/2) % 360
        ax.bar(
            x=np.deg2rad(center_angle),
            height=0.13,
            width=np.deg2rad(delta),
            bottom=0.85,
            color=maison_colors[i],
            alpha=1,
            align='center',
            edgecolor='black',
            linewidth=1
        )
        ax.text(
            np.deg2rad(center_angle), 0.92, str(i+1),
            fontsize=14, ha='center', va='center', color='black', fontweight='bold'
        )

    # Tracer les aspects
    for aspect in aspects:
        if isinstance(aspect, dict):
            noms = aspect["planetes"].split(" - ")
            if len(noms) != 2:
                continue
            p1, p2 = noms
            aspect_type = aspect["aspect"]
            color = aspect.get("color", couleur_aspect(aspect_type))
        elif len(aspect) == 4:
            p1, p2, aspect_type, color = aspect
        elif len(aspect) == 3:
            p1, p2, aspect_type = aspect
            color = couleur_aspect(aspect_type)
        else:
            continue

        if p1 not in planetes or p2 not in planetes:
            continue

        a1 = np.deg2rad(planetes[p1])
        a2 = np.deg2rad(planetes[p2])
        ax.plot([a1, a2], [0.85, 0.85], color=color, lw=2, alpha=0.7)

    # Affichage des planètes à l'extérieur du cercle (y compris Rahu/Ketu)
    conj_threshold = 5  # seuil de conjonction en degrés
    planete_positions = sorted(planetes.items(), key=lambda x: x[1])

    for i, (nom1, deg1) in enumerate(planete_positions):
        # Cherche les planètes proches (conjonction)
        proches = [
            j for j, (nom2, deg2) in enumerate(planete_positions)
            if abs((deg1 - deg2 + 180) % 360 - 180) < conj_threshold
        ]
        rang = proches.index(i)
        n = len(proches)
        if n > 1:
            espace = 10  # écart total en degrés pour le groupe
            decalage = (rang - (n-1)/2) * (espace / max(n-1,1))
            angle = np.deg2rad(deg1 + decalage)
        else:
            angle = np.deg2rad(deg1)
        rayon = rayon_planetes

        symbole = planete_symbols.get(nom1, "?")
        ax.text(angle, rayon, symbole, fontsize=26, ha='center', va='center', color='black', zorder=21)

    # Cercle d'alignement des planètes (optionnel)
    circle = plt.Circle((0,0), 1.38, transform=ax.transData._b, fill=False, color='grey', lw=1, ls='--')
    ax.add_artist(circle)

    # Décorations
    ax.set_yticklabels([])
    ax.set_xticks([])

    # Graduations intérieures tous les 10 degrés
    for deg in range(0, 360, 10):
        angle = np.deg2rad(deg)
        ax.plot([angle, angle], [1.19, 1.2], color='black', lw=1)

    # Règle graduée très fine autour de la roue
    for deg in range(0, 360):
        angle = np.deg2rad(deg)
        ax.plot([angle, angle], [1.195, 1.2], color='black', lw=0.5)
    for deg in range(0, 360, 5):
        angle = np.deg2rad(deg)
        ax.plot([angle, angle], [1.19, 1.2], color='black', lw=1)
    for deg in range(0, 360):
        angle = np.deg2rad(deg)
        ax.plot([angle, angle], [0.83, 0.85], color='black', lw=0.5)
    for deg in range(0, 360, 5):
        angle = np.deg2rad(deg)
        ax.plot([angle, angle], [0.82, 0.85], color='black', lw=1)
    for deg in range(0, 360, 10):
        angle = np.deg2rad(deg)
        ax.plot([angle, angle], [0.81, 0.85], color='black', lw=1.5)


    # Affichage joli avec Rich
    console = Console()
    table = Table(title="Résumé du Thème Astral")
    table.add_column("Objet", style="cyan", no_wrap=True)
    table.add_column("Degré", style="magenta")
    table.add_row("Ascendant", f"{asc_deg:.2f}°")
    table.add_row("Milieu du Ciel (MC)", f"{mc_deg:.2f}°")
    for nom, deg in planetes.items():
        table.add_row(nom, f"{deg:.2f}°")
    console.print(table)

def get_planet_house(deg, maisons_deg):
    """Retourne le numéro de la maison dans laquelle se trouve la planète."""
    for i, maison_deg in enumerate(maisons_deg):
        if deg < maison_deg:
            return i + 1
    return 1  # Si au-delà de la dernière maison, retourne la première maison

# Exemple d'utilisation en script (pas d'interface web)
if __name__ == "__main__":
    # Exemple de données fictives pour test
    planetes = {
        "Soleil": 232.81, "Lune": 251.49, "Mercure": 214.84, "Vénus": 235.07, "Mars": 222.41,
        "Jupiter": 338.23, "Saturne": 108.7, "Uranus": 209.66, "Neptune": 248.73, "Pluton": 188.35,
        "Rahu": 251.05, "Ketu": 71.05,
    }
    maisons_deg = [
        15.2, 32.05, 61.0, 82.62, 102.97, 127.19,
        195.2, 212.05, 241.0, 262.62, 282.97, 307.19
    ]
    aspects = [
        {"planetes": "Soleil - Lune", "aspect": "Conjonction", "angle": 0.5, "color": couleur_aspect("Conjonction")},
        {"planetes": "Mars - Saturne", "aspect": "Carré", "angle": 90, "color": couleur_aspect("Carré")},
        # Ajoute d'autres aspects si tu veux
    ]
    asc_deg = 345.2
    mc_deg = 262.6

    fig = plot_roue(planetes, maisons_deg, aspects, asc_deg, mc_deg)
    plt.show()  # Affiche la roue dans une fenêtre
    # fig.savefig("ma_roue.png")  # Ou sauvegarde en image si tu veux
