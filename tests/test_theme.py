import unittest
from module.theme import construire_theme

class TestTheme(unittest.TestCase):
    def test_construire_theme(self):
        # Exemple de test basique
        from datetime import datetime
        date = datetime.strptime("1974-11-15 14:45:00", "%Y-%m-%d %H:%M:%S")
        theme = construire_theme(date, "Toulouse")
        self.assertIn('ascendant', theme)
        self.assertIn('mc', theme)

if __name__ == "__main__":
    unittest.main()
