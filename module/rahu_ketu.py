
import swisseph as swe
from module.astrologia_tradition import get_timezone, get_utc_time, degrees_to_sign
from datetime import datetime

def calculate_rahu_ketu(date: datetime, latitude: float, longitude: float):
    # Conversion UTC
    timezone = get_timezone(latitude, longitude)
    utc_time = get_utc_time(date, timezone)

    # Calcul Julian Day
    jd_ut = swe.julday(utc_time.year, utc_time.month, utc_time.day,
                       utc_time.hour + utc_time.minute / 60 + utc_time.second / 3600)

    # Rahu = Noeud lunaire nord (mean)
    rahu_position, _ = swe.calc_ut(jd_ut, swe.MEAN_NODE)
    rahu_lon = rahu_position[0]
    rahu_sign, rahu_deg = degrees_to_sign(rahu_lon)

    # Ketu = Rahu + 180°
    ketu_lon = (rahu_lon + 180) % 360
    ketu_sign, ketu_deg = degrees_to_sign(ketu_lon)

    return {
        "Rahu": f"{rahu_sign} {rahu_deg}°",
        "Ketu": f"{ketu_sign} {ketu_deg}°"
    }
