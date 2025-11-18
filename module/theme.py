
from module.astrologia_tradition import calculate_ascendant_and_mc, get_coordinates_from_place
from module.maisons import calculate_houses
from module.planetes import calculate_planets
from module.aspects import find_aspects
from datetime import datetime
import swisseph as swe
from module.astrologia_tradition import get_timezone, get_utc_time

def construire_theme(date: datetime, lieu: str):
    # La date est déjà un objet datetime

    # Obtenir les coordonnées
    latitude, longitude = get_coordinates_from_place(lieu)

    # Calcul des points principaux
    asc, asc_deg, mc, mc_deg = calculate_ascendant_and_mc(date, latitude, longitude)

    # Maisons
    maisons = calculate_houses(date, latitude, longitude)

    # Planètes dans les signes
    planetes_signes = calculate_planets(date, latitude, longitude)

    # Pour les aspects, calculer les positions en degrés absolus
    codes = {
        "Soleil": swe.SUN,
        "Lune": swe.MOON,
        "Mercure": swe.MERCURY,
        "Vénus": swe.VENUS,
        "Mars": swe.MARS,
        "Jupiter": swe.JUPITER,
        "Saturne": swe.SATURN,
        "Uranus": swe.URANUS,
        "Neptune": swe.NEPTUNE,
        "Pluton": swe.PLUTO
    }

    timezone = get_timezone(latitude, longitude)
    utc_time = get_utc_time(date, timezone)
    jd_ut = swe.julday(utc_time.year, utc_time.month, utc_time.day,
                       utc_time.hour + utc_time.minute / 60 + utc_time.second / 3600)

    planetes_degres = [(nom, swe.calc_ut(jd_ut, code)[0][0]) for nom, code in codes.items()]

    aspects = find_aspects(planetes_degres)

    # Compilation du thème
    theme = {
        "ascendant": f"{asc} {asc_deg}°",
        "mc": f"{mc} {mc_deg}°",
        "maisons": maisons,
        "planetes": planetes_signes,
        "aspects": aspects
    }

    return theme
