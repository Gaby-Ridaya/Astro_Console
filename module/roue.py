import matplotlib.pyplot as plt
import numpy as np

class ThemeAstral:
    def __init__(self, ascendant, mc, maisons, planetes, aspects=None):
        self.asc = ascendant
        self.mc = mc
        self.maisons = maisons
        self.planetes = planetes
        self.aspects = aspects if aspects else []
        
        # Configuration des symboles
        self.signes_symboles = ["♈","♉","♊","♋","♌","♍","♎","♏","♐","♑","♒","♓"]
        self.planete_symboles = {
            "Soleil": "☉", "Lune": "☽", "Mercure": "☿", "Vénus": "♀", "Mars": "♂",
            "Jupiter": "♃", "Saturne": "♄", "Uranus": "♅", "Neptune": "♆", "Pluton": "♇",
            "Rahu": "☊", "Ketu": "☋",  # Nœuds lunaires ajoutés
            "Lilith": "⚸", "Chiron": "⚷"
        }
        # Couleurs des éléments (Feu, Terre, Air, Eau)
        self.element_colors = ["#ffdddd", "#e6f2e6", "#e6f7ff", "#e6e6ff"] * 3

    def _deg_to_rad(self, deg):
        return np.deg2rad(deg)

    def _get_element_color(self, sign_index):
        return self.element_colors[sign_index % 4]

    def optimiser_positions_planetes(self, planetes_triees, seuil=5):
        """Évite la superposition des textes des planètes."""
        positions = {}
        n = len(planetes_triees)
        if n == 0: return positions

        levels = [0] * n
        
        for i in range(n):
            nom, deg = planetes_triees[i]
            angle = self._deg_to_rad(deg)
            
            for prev in range(max(0, i-3), i):
                prev_nom, prev_deg = planetes_triees[prev]
                diff = min(abs(deg - prev_deg), 360 - abs(deg - prev_deg))
                
                if diff < seuil:
                    if levels[i] == levels[prev]:
                         levels[i] += 1

            positions[nom] = (angle, levels[i])
        return positions

    def tracer(self):
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='polar')
        
        bg_color = '#ffffff'
        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)
        
        # Rayons (Layers)
        r_houses_inner = 0.45
        r_houses_outer = 0.75
        r_zodiac_inner = 0.75
        r_zodiac_outer = 0.90
        r_ticks = 0.92
        
        # Orientation (ASC à gauche)
        rotation_offset = np.pi - self._deg_to_rad(self.asc)
        ax.set_theta_offset(rotation_offset)
        ax.set_theta_direction(1) 

        # --- 1. ZODIAQUE ---
        for i in range(12):
            theta1 = i * np.pi / 6
            width = np.pi / 6
            ax.bar(theta1 + width/2, r_zodiac_outer - r_zodiac_inner, width=width, bottom=r_zodiac_inner, 
                   color=self._get_element_color(i), edgecolor='white', linewidth=1)
            ax.text(theta1 + width/2, (r_zodiac_inner + r_zodiac_outer)/2, self.signes_symboles[i], 
                    ha='center', va='center', fontsize=14, fontweight='bold', color='#444')

        # --- 2. MAISONS ---
        house_colors = ['#fcfcfc', '#f0f0f0'] 
        for i in range(12):
            deg_start = self.maisons[i]
            deg_end = self.maisons[(i+1)%12]
            
            if deg_end < deg_start: width_deg = (360 - deg_start) + deg_end
            else: width_deg = deg_end - deg_start
                
            rad_mid = self._deg_to_rad(deg_start + width_deg/2)
            
            # Secteur maison
            ax.bar(rad_mid, r_houses_outer - r_houses_inner, width=self._deg_to_rad(width_deg), bottom=r_houses_inner,
                   color=house_colors[i%2], edgecolor='none', alpha=1)
            
            # Cuspide (ligne de séparation)
            ax.plot([self._deg_to_rad(deg_start), self._deg_to_rad(deg_start)], 
                    [r_houses_inner, r_houses_outer], color='#666666', lw=1, linestyle='-')
            
            # Numéro maison
            ax.text(rad_mid, (r_houses_inner + r_houses_outer)/2, str(i+1), 
                    fontsize=9, color='#888888', ha='center', va='center')

        # Cercles de délimitation
        for r in [r_houses_inner, r_houses_outer, r_zodiac_outer]:
            ax.plot(np.linspace(0, 2*np.pi, 100), [r]*100, color='#444', lw=0.6)

        # --- 3. GRADES ---
        angles_rad = np.deg2rad(np.arange(0, 360, 1))
        for rad in angles_rad:
            deg = np.rad2deg(rad)
            if deg % 10 == 0:
                ax.plot([rad, rad], [r_zodiac_outer, r_ticks], color='black', lw=1)
            elif deg % 5 == 0:
                ax.plot([rad, rad], [r_zodiac_outer, r_zodiac_outer + 0.01], color='black', lw=0.5)

        # --- 4. ANGLES (ASC/MC) ---
        ax.text(self._deg_to_rad(self.asc), r_houses_outer - 0.05, "ASC", color='red', fontsize=8, fontweight='bold', ha='center')
        ax.text(self._deg_to_rad(self.mc), r_houses_outer - 0.05, "MC", color='red', fontsize=8, fontweight='bold', ha='center')
        ax.plot([self._deg_to_rad(self.asc), self._deg_to_rad(self.asc)], [r_houses_inner, r_zodiac_outer], color='red', lw=1.5, alpha=0.5)
        ax.plot([self._deg_to_rad(self.mc), self._deg_to_rad(self.mc)], [r_houses_inner, r_zodiac_outer], color='red', lw=1.5, alpha=0.5)

        # --- 5. PLANÈTES (Rahu/Ketu inclus) ---
        sorted_planets = sorted(self.planetes.items(), key=lambda x: x[1])
        positions_optimisees = self.optimiser_positions_planetes(sorted_planets)
        
        r_base_planete = r_ticks + 0.15
        step_level = 0.08
        
        for nom, (angle, level) in positions_optimisees.items():
            rayon = r_base_planete + (level * step_level)
            symbole = self.planete_symboles.get(nom, nom[0])
            
            # Couleur spécifique pour Rahu/Ketu
            color = 'darkblue' if nom in ["Rahu", "Ketu"] else 'black'
            
            if level > 0:
                ax.plot([angle, angle], [r_zodiac_outer, rayon-0.02], color='grey', lw=0.5, alpha=0.3)
            else:
                ax.plot([angle, angle], [r_zodiac_outer, r_ticks + 0.02], color='grey', lw=0.5)
            
            ax.text(angle, rayon, symbole, fontsize=16, ha='center', va='center', color=color)
            deg_display = int(self.planetes[nom] % 30)
            ax.text(angle, rayon - 0.035, f"{deg_display}°", fontsize=7, ha='center', va='top', color='#555')

        # --- 6. ASPECTS ---
        for p1_nom, p2_nom, aspect_nom, color in self.aspects:
            d1 = self._get_degree_from_input(p1_nom)
            d2 = self._get_degree_from_input(p2_nom)
            if d1 is not None and d2 is not None:
                ax.plot([self._deg_to_rad(d1), self._deg_to_rad(d2)], 
                        [r_houses_inner, r_houses_inner], color=color, lw=0.8, alpha=0.6)

        # Finitions
        ax.set_yticklabels([])
        ax.set_xticks([])
        ax.grid(False)
        ax.spines['polar'].set_visible(False)
        plt.title(f"Thème Astral avec Nœuds Lunaires\nASC: {self.asc}° | MC: {self.mc}°", pad=20)
        plt.tight_layout()
        plt.show()

    def _get_degree_from_input(self, identifiant):
        if identifiant in self.planetes: return self.planetes[identifiant]
        for nom, symb in self.planete_symboles.items():
            if symb == identifiant:
                if nom in self.planetes: return self.planetes[nom]
        return None

# --- DONNÉES ---

ASC_DEG = 345.2
MC_DEG = 262.62
MAISONS_DEG = [
    15.2, 32.05, 61.0, 82.62, 102.97, 127.19,
    195.2, 212.05, 241.0, 262.62, 282.97, 307.19
]
PLANETES = {
    "Soleil": 232.81, "Lune": 251.49, "Mercure": 214.84, "Vénus": 235.07, "Mars": 222.41,
    "Jupiter": 338.23, "Saturne": 108.7, "Uranus": 209.66, "Neptune": 248.73, "Pluton": 188.35,
    # Ajout manuel de Rahu (Noeud Nord)
    "Rahu": 15.5  # Exemple en Bélier
}

# Calcul automatique de Ketu (toujours opposé à Rahu)
if "Rahu" in PLANETES and "Ketu" not in PLANETES:
    PLANETES["Ketu"] = (PLANETES["Rahu"] + 180) % 360

# Aspects
ASPECTS = [
    ("☉", "♀", "conjonction", "purple"),
    ("☉", "♄", "trigone", "blue"),
    ("☽", "♃", "carré", "red"),
    # On peut ajouter des aspects aux noeuds si on veut
    ("Rahu", "♄", "carré", "red"), 
]

if __name__ == "__main__":
    theme = ThemeAstral(ASC_DEG, MC_DEG, MAISONS_DEG, PLANETES, ASPECTS)
    theme.tracer()