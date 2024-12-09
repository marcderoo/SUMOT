import random
import os
from typing import List, Tuple

# Import des fonctions des bots
from mode_duel import bot_proposition_difficile, bot_proposition_ultime_1

# Fonction pour charger les mots du dictionnaire
def charger_dictionnaire(fichier: str) -> List[str]:
    """Charge les mots du fichier dictionnaire_clean.txt dans une liste."""
    with open(fichier, "r", encoding="utf-8") as f:
        mots = [ligne.strip() for ligne in f.readlines() if ligne.strip()]
    return mots

# Fonction principale pour le mode Battle IA
def mode_battle_ia()-> None:
    fichier = "dictionnaire_clean.txt"
    if not os.path.exists(fichier):
        print("Le fichier dictionnaire_clean.txt est introuvable.")
        return

    # Charger le dictionnaire
    mots: List[str] = charger_dictionnaire(fichier)

    # Compteurs pour les résultats des 50 parties
    vic_ultime: int = 0
    match_nul: int = 0
    def_ultime: int = 0

    # Lancer 50 parties
    for partie in range(1, 500):
        print(f"\n=== Partie {partie} ===")
        # Choisir un mot aléatoire
        mot_a_trouver: str = random.choice(mots)
        longueur: int = len(mot_a_trouver)
        premiere_lettre: str = mot_a_trouver[0]

        print(f"Le mot à trouver contient {longueur} lettres : {premiere_lettre}{'_' * (longueur - 1)}")

        # Initialiser les historiques et les tours pour les deux IA
        historique_difficile: List[Tuple[str, List[str]]] = []
        historique_ultime: List[Tuple[str, List[str]]] = []
        tours_difficile: int = 0
        tours_ultime: int = 0

        mots_possibles = [mot for mot in mots if len(mot) == longueur and mot.startswith(premiere_lettre)]

        # Étape 1 : Le bot difficile joue jusqu'à trouver le mot
        while True:
            tours_difficile += 1

            # Bot difficile joue
            proposition_difficile: str = bot_proposition_difficile(mots_possibles, historique_difficile)
            resultat_difficile: List[str] = [
                "vert" if mot_a_trouver[i] == proposition_difficile[i]
                else "orange" if proposition_difficile[i] in mot_a_trouver
                else "rouge"
                for i in range(longueur)
            ]
            historique_difficile.append((proposition_difficile, resultat_difficile))
            print(f"Tour {tours_difficile} - Bot difficile propose : {proposition_difficile}")

            # Vérifier si le bot difficile a trouvé le mot
            if proposition_difficile == mot_a_trouver:
                print(f"🎉 Bot difficile a trouvé le mot en {tours_difficile} tours.")
                break

        # Étape 2 : Le bot ultime joue après que le bot difficile ait trouvé le mot
        while True:
            tours_ultime += 1

            # Bot ultime joue
            proposition_ultime: str = bot_proposition_ultime_1(mots_possibles, historique_ultime)
            resultat_ultime: List[str] = [
                "vert" if mot_a_trouver[i] == proposition_ultime[i]
                else "orange" if proposition_ultime[i] in mot_a_trouver
                else "rouge"
                for i in range(longueur)
            ]
            historique_ultime.append((proposition_ultime, resultat_ultime))
            print(f"Tour {tours_ultime} - Bot ultime propose : {proposition_ultime}")

            # Vérifier si le bot ultime a trouvé le mot
            if proposition_ultime == mot_a_trouver:
                print(f"🎉 Bot ultime a trouvé le mot en {tours_ultime} tours.")
                break

        # Comparer les résultats
        if tours_ultime < tours_difficile:
            vic_ultime += 1
        elif tours_ultime == tours_difficile:
            match_nul += 1
        else:
            def_ultime += 1

    # Afficher les résultats après 50 parties
    print("\n=== Résultats après 50 parties ===")
    print(f"Victoire Bot Ultime : {vic_ultime}")
    print(f"Match nul : {match_nul}")
    print(f"Défaite Bot Ultime : {def_ultime}")

# Lancer le mode Battle IA
if __name__ == "__main__":
    mode_battle_ia()