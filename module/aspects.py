
from math import fabs

# Définition des aspects et orbes tolérés
ASPECTS = {
    "Conjonction": (0, 8),
    "Opposition": (180, 8),
    "Carré": (90, 6),
    "Trigone": (120, 6),
    "Sextile": (60, 5)
}

def find_aspects(planets: list[tuple[str, float]]):
    resultats = []
    n = len(planets)

    for i in range(n):
        nom1, pos1 = planets[i]
        for j in range(i+1, n):
            nom2, pos2 = planets[j]
            angle = fabs(pos1 - pos2)
            angle = angle if angle <= 180 else 360 - angle

            for aspect_name, (aspect_angle, orbe) in ASPECTS.items():
                if fabs(angle - aspect_angle) <= orbe:
                    resultats.append({
                        "planetes": f"{nom1} - {nom2}",
                        "aspect": aspect_name,
                        "angle": round(angle, 2)
                    })

    return resultats
