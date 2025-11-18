
from module.theme import construire_theme
from module.rahu_ketu import calculate_rahu_ketu
from module.astrologia_tradition import get_coordinates_from_place
from datetime import datetime

print("=== Calcul du Thème Astral ===")
date_str = input("Entrez la date et l'heure de naissance (YYYY-MM-DD HH:MM:SS) : ")
lieu = input("Entrez le lieu de naissance : ")

# Construction du thème
theme = construire_theme(date_str, lieu)

# Calcul de Rahu et Ketu
date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
latitude, longitude = get_coordinates_from_place(lieu)
noeuds = calculate_rahu_ketu(date, latitude, longitude)

# Affichage du thème complet dans la console
print("\n--- ASCENDANT & MC ---")
print(f"Ascendant : {theme['ascendant']}")
print(f"Milieu du Ciel (MC) : {theme['mc']}")

print("\n--- MAISONS ---")
for nom, position in theme['maisons']:
    print(f"{nom} : {position}")

print("\n--- PLANÈTES ---")
for nom, position in theme['planetes']:
    print(f"{nom} : {position}")

print("\n--- RAHU & KETU ---")
print(f"Rahu : {noeuds['Rahu']}")
print(f"Ketu : {noeuds['Ketu']}")

print("\n--- ASPECTS ---")
for aspect in theme['aspects']:
    print(f"{aspect['planetes']} : {aspect['aspect']} ({aspect['angle']}°)")

