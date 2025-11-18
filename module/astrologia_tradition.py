
import swisseph as swe
from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim



# Fonction pour obtenir les coordonnées à partir du nom du lieu en utilisant Geopy
def get_coordinates_from_place(place_name):
    from geopy.exc import GeocoderTimedOut
    geolocator = Nominatim(user_agent="astro_calculator")
    try:
        location = geolocator.geocode(place_name, timeout=10)
        if location:
            return location.latitude, location.longitude
        else:
            raise ValueError(f"Lieu '{place_name}' non trouvé.")
    except GeocoderTimedOut:
        print("\n[ERREUR] Le service de géolocalisation a expiré. Veuillez vérifier votre connexion ou réessayer plus tard.")
        print("Vous pouvez aussi entrer les coordonnées manuellement.")
        lat = input("Latitude : ")
        lon = input("Longitude : ")
        try:
            return float(lat), float(lon)
        except Exception:
            raise ValueError("Coordonnées invalides.")

def get_timezone(lat, lon):
    tf = TimezoneFinder()
    return tf.timezone_at(lat=lat, lng=lon)

def get_utc_time(local_time, timezone):
    local_tz = pytz.timezone(timezone)
    local_time = local_tz.localize(local_time)
    return local_time.astimezone(pytz.utc)

def degrees_to_sign(degrees):
    signes_francais = ["Bélier", "Taureau", "Gémeaux", "Cancer", "Lion", "Vierge",
                       "Balance", "Scorpion", "Sagittaire", "Capricorne", "Verseau", "Poissons"]
    sign_index = int(degrees // 30)
    return signes_francais[sign_index], round(degrees % 30, 2)

def calculate_ascendant_and_mc(date, latitude, longitude):
    timezone = get_timezone(latitude, longitude)
    utc_time = get_utc_time(date, timezone)
    print(f"Heure UTC utilisée pour le calcul : {utc_time}")

    jd_ut = swe.julday(utc_time.year, utc_time.month, utc_time.day,
                       utc_time.hour + utc_time.minute / 60 + utc_time.second / 3600)

    houses, ascmc = swe.houses_ex(jd_ut, latitude, longitude, b'P')  # Appel sans flag
    ascendant = ascmc[0]  # Ascendant
    mc = ascmc[1]         # Milieu du Ciel (MC)

    ascendant_sign, ascendant_degree = degrees_to_sign(ascendant)
    mc_sign, mc_degree = degrees_to_sign(mc)

    return ascendant_sign, ascendant_degree, mc_sign, mc_degree

def main():
    pass  # La saisie se fait désormais dans main.py
