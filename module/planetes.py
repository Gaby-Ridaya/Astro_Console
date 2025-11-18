
import swisseph as swe
from module.astrologia_tradition import get_timezone, get_utc_time, degrees_to_sign
from datetime import datetime

# Liste des corps célestes principaux à calculer
PLANETES = {
    "Soleil": swe.SUN,
    "Lune": swe.MOON,
    "Mercure": swe.MERCURY,
    "Vénus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturne": swe.SATURN,
    "Uranus": swe.URANUS,
    "Neptune": swe.NEPTUNE,
    "Pluton": swe.PLUTO,
    "Lilith": swe.MEAN_APOG,
    "Chiron": swe.CHIRON
}

def calculate_planets(date: datetime, latitude: float, longitude: float):
    timezone = get_timezone(latitude, longitude)
    utc_time = get_utc_time(date, timezone)

    jd_ut = swe.julday(utc_time.year, utc_time.month, utc_time.day,
                       utc_time.hour + utc_time.minute / 60 + utc_time.second / 3600)

    positions = []
    for nom, code in PLANETES.items():
        try:
            position, _ = swe.calc_ut(jd_ut, code)
            lon = position[0]
            sign, deg_in_sign = degrees_to_sign(lon)
            positions.append((nom, f"{sign} {deg_in_sign}°"))
        except Exception:
            continue
    return positions
