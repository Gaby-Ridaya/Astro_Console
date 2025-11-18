import pytest
from module.roue_v2 import plot_roue, get_planet_house

def test_plot_roue_runs_without_error():
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
        {"planetes": "Soleil - Lune", "aspect": "Conjonction", "angle": 0.5},
        {"planetes": "Mars - Saturne", "aspect": "Carré", "angle": 90},
    ]
    asc_deg = 345.2
    mc_deg = 262.6
    plot_roue(planetes, maisons_deg, aspects, asc_deg, mc_deg)

    maisons_deg = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]
    assert get_planet_house(15, maisons_deg) == 2
    assert get_planet_house(75, maisons_deg) == 4
    assert get_planet_house(350, maisons_deg) == 1
