from module.theme import construire_theme
from module.rahu_ketu import calculate_rahu_ketu
from module.astrologia_tradition import get_coordinates_from_place
from datetime import datetime
from module.affichage import afficher_ascendant_mc, afficher_maisons, afficher_planetes, afficher_rahu_ketu, afficher_aspects


def main():
    print("=== Calcul du Thème Astral ===")
    date_str = input("Entrez la date et l'heure de naissance (YYYY-MM-DD HH:MM:SS) : ")
    lieu = input("Entrez le lieu de naissance : ")

    try:
        birth_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        print("Format de date non reconnu. Utilisez : YYYY-MM-DD HH:MM:SS")
        return

    # Construction du thème
    theme = construire_theme(birth_time, lieu)

    # Calcul de Rahu et Ketu
    from geopy.exc import GeocoderTimedOut
    for tentative in range(2):
        try:
            latitude, longitude = get_coordinates_from_place(lieu)
            break
        except GeocoderTimedOut:
            print("Service de géolocalisation indisponible ou trop lent. Veuillez réessayer ou entrer un autre lieu.")
            lieu = input("Entrez un autre lieu de naissance (ou laissez vide pour quitter) : ")
            if not lieu:
                print("Abandon.")
                return
        except Exception as e:
            print(f"Erreur lors de la recherche du lieu : {e}")
            latitude = float(input("Entrez la latitude : "))
            longitude = float(input("Entrez la longitude : "))
            break
    noeuds = calculate_rahu_ketu(birth_time, latitude, longitude)

    # Affichage avec Rich
    afficher_ascendant_mc(theme)
    afficher_maisons(theme['maisons'])
    afficher_planetes(theme['planetes'])
    afficher_rahu_ketu(noeuds)
    afficher_aspects(theme['aspects'])

    # Affichage de la roue astrologique avec roue.py
    from module.roue import ThemeAstral
    # Conversion signe + degré en degré absolu
    signes_fr = ["Bélier", "Taureau", "Gémeaux", "Cancer", "Lion", "Vierge",
                 "Balance", "Scorpion", "Sagittaire", "Capricorne", "Verseau", "Poissons"]
    def signe_degre_to_abs(val):
        try:
            signe, deg = val.split()
            deg = float(deg.replace('°',''))
            idx = signes_fr.index(signe)
            return idx * 30 + deg
        except Exception:
            return 0.0

    asc_deg = signe_degre_to_abs(theme['ascendant'])
    mc_deg = signe_degre_to_abs(theme['mc'])
    maisons_deg = [signe_degre_to_abs(pos) for nom, pos in theme['maisons']]
    planetes_deg = {nom: signe_degre_to_abs(pos) for nom, pos in theme['planetes']}
    # Ajout Rahu et Ketu
    planetes_deg["Rahu"] = signe_degre_to_abs(noeuds["Rahu"])
    planetes_deg["Ketu"] = signe_degre_to_abs(noeuds["Ketu"])
    # Ajout Lilith et Chiron si présents
    for nom in ["Lilith", "Chiron"]:
        if nom not in planetes_deg:
            for n, pos in theme['planetes']:
                if n == nom:
                    planetes_deg[nom] = signe_degre_to_abs(pos)
    # Transformation des aspects pour la roue
    def couleur_aspect(aspect_type):
        if aspect_type == "Conjonction":
            return "purple"
        elif aspect_type == "Opposition":
            return "blue"
        elif aspect_type == "Carré":
            return "red"
        elif aspect_type == "Trigone":
            return "green"
        elif aspect_type == "Sextile":
            return "orange"
        else:
            return "grey"

    aspects_roue = []
    for aspect in theme['aspects']:
        noms = aspect['planetes'].split(' - ')
        if len(noms) == 2:
            p1, p2 = noms
            aspects_roue.append((p1, p2, aspect['aspect'].lower(), couleur_aspect(aspect['aspect'])))

    roue = ThemeAstral(ascendant=asc_deg, mc=mc_deg, maisons=maisons_deg, planetes=planetes_deg, aspects=aspects_roue)
    roue.tracer()


if __name__ == "__main__":
    main()
