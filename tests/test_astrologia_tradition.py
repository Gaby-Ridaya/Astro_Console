import pytest
from module.astrologia_tradition import get_coordinates_from_place, get_timezone, get_utc_time, degrees_to_sign

def test_get_coordinates_from_place_valide():
    lat, lon = get_coordinates_from_place("Paris")
    assert isinstance(lat, float)
    assert isinstance(lon, float)

def test_get_coordinates_from_place_invalide():
    with pytest.raises(Exception):
        get_coordinates_from_place("LieuInconnu")

def test_get_timezone_valide():
    from geopy.exc import GeocoderTimedOut
    try:
        lat, lon = get_coordinates_from_place("Paris")
        tz = get_timezone(lat, lon)
        assert tz is not None
    except GeocoderTimedOut:
        pytest.skip("Service de géolocalisation indisponible (timeout)")

def test_get_timezone_invalide():
    with pytest.raises(Exception):
        get_timezone("LieuInconnu")

def test_get_utc_time():
    # Test avec une date et un fuseau horaire connus
    from datetime import datetime
    dt = datetime(2020, 1, 1, 12, 0, 0)
    tz = "Europe/Paris"
    utc_dt = get_utc_time(dt, tz)
    assert utc_dt.tzinfo is not None

def test_degrees_to_sign():
    sign, deg = degrees_to_sign(30)
    assert isinstance(sign, str)
