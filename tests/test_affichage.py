import unittest
from module.affichage import afficher_ascendant_mc

class TestAffichage(unittest.TestCase):
    def test_afficher_ascendant_mc(self):
        # Test d'appel de la fonction (vérifie qu'il n'y a pas d'erreur)
        theme = {'ascendant': 'Poissons 15.2°', 'mc': 'Sagittaire 22.62°'}
        try:
            afficher_ascendant_mc(theme)
        except Exception as e:
            self.fail(f"afficher_ascendant_mc a échoué : {e}")

if __name__ == "__main__":
    unittest.main()
