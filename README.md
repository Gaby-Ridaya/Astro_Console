
🌌 Astro Console

Application astrologique en console avec affichage graphique

✨ Présentation

Astro Console est une application Python modulaire qui permet :

d’afficher les résultats astrologiques dans le terminal avec une interface colorée grâce à Rich,

de générer automatiquement une roue astrologique complète avec Matplotlib,

de calculer les positions planétaires avec pyswisseph,

et de valider toutes les fonctionnalités avec une suite complète de tests unitaires (pytest).

Le projet combine calculs astrologiques, graphique professionnel, architecture propre et bonne pratiques Python.

🧰 Fonctionnalités

Affichage clair et lisible dans le terminal

Dessin automatique du thème astral (maisons, planètes, aspects…)

Gestion des nœuds lunaires, aspects, angles, etc

Calcul astrologique précis via pyswisseph

Tests unitaires couvrant tous les modules

Architecture modulaire et extensible 

📂 Structure du projet
Astro_Console/
├── main.py
├── requirements.txt
├── module/
│   ├── affichage.py
│   ├── aspects.py
│   ├── astrologia_tradition.py
│   ├── maisons.py
│   ├── planetes.py
│   ├── rahu_ketu.py
│   ├── roue.py
│   ├── roue_v2.py
│   └── theme.py
└── tests/
    ├── test_affichage.py
    ├── test_aspects.py
    ├── test_astrologia_tradition.py
    ├── test_maisons.py
    ├── test_planetes.py
    ├── test_rahu_ketu.py
    ├── test_roue.py
    ├── test_roue_v2.py
    ├── test_theme.py
    └── test_utils.py

▶️ Lancer l’application
python main.py
Entrez la date et l'heure de naissance (YYYY-MM-DD HH:MM:SS) :
Entrez le lieu de naissance :

L’application affichera :

un rendu console stylé

une fenêtre graphique contenant le thème astral # Astro Console

![Exemple de roue astrologique](images/theme_astral_exemple.png)

🧪 Lancer les tests
pytest


Avec couverture :

pytest --cov=module

🖼️ Aperçu

Le thème astrologique généré par l’application :

📜 Licence

MIT (modifiable selon ton choix)

🤝 Contributions

Les contributions sont les bienvenues !
N’hésitez pas à proposer des idées, signaler un bug ou envoyer une PR.
>>>>>>> 626a637 (Initial commit Astro Console)
