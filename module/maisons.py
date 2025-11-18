
import swisseph as swe
from module.astrologia_tradition import get_timezone, get_utc_time, degrees_to_sign
from datetime import datetime

def calculate_houses(date: datetime, latitude: float, longitude: float):
    # Conversion UTC
    timezone = get_timezone(latitude, longitude)
    utc_time = get_utc_time(date, timezone)

    # Calcul Julian Day
    jd_ut = swe.julday(utc_time.year, utc_time.month, utc_time.day,
                       utc_time.hour + utc_time.minute / 60 + utc_time.second / 3600)

    # Calcul des maisons (système Placidus)
    houses, _ = swe.houses_ex(jd_ut, latitude, longitude, b'P')

    maisons = []
    for i in range(12):
        deg = houses[i]
        sign, deg_in_sign = degrees_to_sign(deg)
        maisons.append((f"Maison {i+1}", f"{sign} {deg_in_sign}°"))

    return maisons
