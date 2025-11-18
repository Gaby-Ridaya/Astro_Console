import unittest
from module.rahu_ketu import calculate_rahu_ketu
from datetime import datetime

class TestRahuKetu(unittest.TestCase):
    def test_calculate_rahu_ketu(self):
        date = datetime(1974, 11, 15, 14, 45, 0)
        latitude, longitude = 43.6045, 1.4442
        noeuds = calculate_rahu_ketu(date, latitude, longitude)
        self.assertIn('Rahu', noeuds)
        self.assertIn('Ketu', noeuds)

if __name__ == "__main__":
    unittest.main()
