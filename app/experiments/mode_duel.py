from typing import List, Tuple, Dict, Optional
import random
import os
import requests
from bs4 import BeautifulSoup

def get_path(full_path: str) -> str:
    """
    Get the full path of a file in the project.
    """
    root = os.path.dirname(os.path.abspath(__file__))

    # Go up until we find the LICENSE file
    while not os.path.exists(os.path.join(root, "LICENSE")):
        root = os.path.dirname(root)
    return os.path.join(root, full_path)

def obtenir_definition(mot: str) -> str:
    """
    Récupère la définition principale d'un mot, en cherchant d'abord sur le site du Larousse,
    puis sur le Wiktionnaire si nécessaire. Retourne un message si aucune définition n'est trouvée.
    
    :param mot: Mot pour lequel chercher la définition
    :return: Définition principale ou message d'erreur
    """
    # Fonction pour récupérer la définition depuis le Larousse
    def definition_larousse(mot: str) -> str:
        url = f"https://www.larousse.fr/dictionnaires/francais/{mot}"
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                # Recherche de la définition, même si l'URL contient un identifiant supplémentaire
                definition = soup.find("ul", class_="Definitions")  # Classe spécifique au Larousse
                if definition:
                    premier_element = definition.find("li")  # Trouve la première définition
                    if premier_element:
                        return premier_element.text.strip()
            return None
        except Exception as e:
            return None

    # Fonction pour récupérer la définition depuis le Wiktionnaire
    def definition_wiktionnaire(mot: str) -> str:
        url = f"https://fr.wiktionary.org/wiki/{mot}"
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                definition = soup.find("ol")  # Trouve la liste ordonnée
                if definition:
                    premier_element = definition.find("li")  # Trouve la première entrée de la liste
                    if premier_element:
                        texte_principal = premier_element.text.split("\n")[0]  # Sépare sur les sauts de ligne
                        return texte_principal.strip()
            return None
        except Exception as e:
            return None

    # Tentative de récupération depuis le Larousse
    definition = definition_larousse(mot)
    if definition:
        return f"(Source: Larousse) {definition}"

    # Si non trouvé, tentative depuis le Wiktionnaire
    definition = definition_wiktionnaire(mot)
    if definition:
        return f"(Source: Wiktionnaire) {definition}"

    # Si aucune définition n'est trouvée
    return "Aucune définition trouvée pour ce mot."




def charger_dictionnaire(fichier: str) -> List[str]:
    """Charge les mots du fichier dictionnaire_clean.txt dans une liste."""
    with open(fichier, "r", encoding="utf-8") as f:
        mots = [ligne.strip() for ligne in f.readlines() if ligne.strip()]
    return mots


def choisir_mot(mots: List[str]) -> str:
    """Choisit un mot aléatoire depuis la liste des mots."""
    return "lapin"



def colorier_mot_graphique(mot_propose: str, mot_a_trouver: str) -> str:
    """Retourne un mot coloré graphiquement avec des lettres :
    - Vert pour correcte et bien placée
    - Orange pour présente mais mal placée
    - Rouge pour absente.
    """
    resultat: List[Optional[str]] = []
    mot_a_trouver_temp: List[Optional[str]] = list(mot_a_trouver)  # Copie modifiable du mot à trouver

    # Étape 1 : Identifier les lettres correctes (vertes)
    for i, lettre in enumerate(mot_propose):
        if lettre == mot_a_trouver[i]:
            resultat.append(f"\033[92m{lettre}\033[0m")  # Vert
            mot_a_trouver_temp[i] = None  # Marquer comme utilisée
        else:
            resultat.append(None)  # Placeholder temporaire

    # Étape 2 : Identifier les lettres présentes mais mal placées (oranges) et absentes (rouges)
    for i, lettre in enumerate(mot_propose):
        if resultat[i] is None:  # Ne traiter que les lettres non marquées comme vertes
            if lettre in mot_a_trouver_temp:
                resultat[i] = f"\033[93m{lettre}\033[0m"  # Orange
                mot_a_trouver_temp[mot_a_trouver_temp.index(lettre)] = None  # Consommer la lettre
            else:
                resultat[i] = f"\033[91m{lettre}\033[0m"  # Rouge

    # Combiner les lettres colorées en une chaîne
    return "".join(resultat)




def bot_proposition_facile(mots_possibles: List[str], historiques: List[Tuple[str, List[str]]])-> Optional[str]:
    """Le bot se base uniquement sur les lettres bien placées (vertes) pour faire ses propositions."""
    for proposition, resultat in historiques:
        nouveaux_mots: List[str] = []
        for mot in mots_possibles:
            valide: bool = True
            for i, lettre in enumerate(proposition):
                # Vérifie uniquement les lettres "vertes"
                if resultat[i] == "vert" and mot[i] != lettre:
                    valide = False
                    break
            if valide:
                nouveaux_mots.append(mot)
        mots_possibles = nouveaux_mots if nouveaux_mots else mots_possibles
    return random.choice(mots_possibles) if mots_possibles else None




def bot_proposition_moyen(mots_possibles: List[str], historiques: List[Tuple[str, List[str]]]) -> Optional[str]:
    """Le bot se base sur les lettres bien placées (vertes) et les lettres correctes mais mal placées (oranges)."""
    for proposition, resultat in historiques:
        nouveaux_mots: List[str] = []
        for mot in mots_possibles:
            valide: bool = True
            mot_temp: List[Optional[str]] = list(mot)  # Copie modifiable pour traquer les lettres oranges
            for i, lettre in enumerate(proposition):
                if resultat[i] == "vert":
                    if mot[i] != lettre:
                        valide = False
                        break
                elif resultat[i] == "orange":
                    # Vérifie la présence ailleurs mais pas à la même position
                    if lettre not in mot_temp or mot[i] == lettre:
                        valide = False
                        break
                    mot_temp[mot_temp.index(lettre)] = None  # Consomme la lettre
                elif resultat[i] == "rouge":
                    # Vérifie que la lettre n'est pas du tout présente
                    if lettre in mot_temp:
                        valide = False
                        break
            if valide:
                nouveaux_mots.append(mot)
        mots_possibles = nouveaux_mots if nouveaux_mots else mots_possibles

    return random.choice(mots_possibles) if mots_possibles else None



def bot_proposition_difficile(mots_possibles: List[str], historiques: List[Tuple[str, List[str]]]) -> Optional[str]:
    """Le bot utilise toutes les couleurs pour filtrer les mots possibles, sans gestion de lettres consommées."""
    mots_filtrés = mots_possibles.copy()  # Travail sur une copie pour préserver l'original

    for proposition, resultat in historiques:
        nouveaux_mots: List[str] = []
        for mot in mots_filtrés:
            valide: bool = True

            for i, lettre in enumerate(proposition):
                if resultat[i] == "vert":
                    # Lettre doit être exactement à cette position
                    if mot[i] != lettre:
                        valide = False
                        break
                elif resultat[i] == "orange":
                    # Lettre doit être présente ailleurs, mais pas à cette position
                    if lettre not in mot or mot[i] == lettre:
                        valide = False
                        break
                elif resultat[i] == "rouge":
                    # Lettre ne doit pas être à cette position
                    if mot[i] == lettre:
                        valide = False
                        break
                    # Vérifie si la lettre rouge est présente ailleurs
                    indices_orange_vert: List[int] = [
                        j for j, res in enumerate(resultat) if res in ["vert", "orange"] and proposition[j] == lettre
                    ]
                    if lettre in mot and not indices_orange_vert:
                        valide = False
                        break

            if valide:
                nouveaux_mots.append(mot)

        # Met à jour la liste des mots possibles après ce tour
        mots_filtrés = nouveaux_mots if nouveaux_mots else mots_filtrés

    # Débogage : Affiche les mots possibles après filtrage
    #print(f"Mots possibles après filtrage (difficile) : {mots_filtrés}")

    return random.choice(mots_filtrés) if mots_filtrés else None






def bot_proposition_ultime_1(mots_possibles: List[str], historiques: List[Tuple[str, List[str]]]) -> Optional[str]:
    """Le bot utilise toutes les couleurs pour filtrer les mots possibles, sans gestion de lettres consommées."""
    mots_filtrés: List[str] = mots_possibles.copy()  # Travail sur une copie pour préserver l'original

    for proposition, resultat in historiques:
        nouveaux_mots: List[str] = []
        for mot in mots_filtrés:
            valide: bool = True

            for i, lettre in enumerate(proposition):
                if resultat[i] == "vert":
                    # Lettre doit être exactement à cette position
                    if mot[i] != lettre:
                        valide = False
                        break
                elif resultat[i] == "orange":
                    # Lettre doit être présente ailleurs, mais pas à cette position
                    if lettre not in mot or mot[i] == lettre:
                        valide = False
                        break
                elif resultat[i] == "rouge":
                    # Lettre ne doit pas être à cette position
                    if mot[i] == lettre:
                        valide = False
                        break
                    # Vérifie si la lettre rouge est présente ailleurs
                    indices_orange_vert: List[int] = [
                        j for j, res in enumerate(resultat) if res in ["vert", "orange"] and proposition[j] == lettre
                    ]
                    if lettre in mot and not indices_orange_vert:
                        valide = False
                        break

            if valide:
                nouveaux_mots.append(mot)

        # Met à jour la liste des mots possibles après ce tour
        mots_filtrés = nouveaux_mots if nouveaux_mots else mots_filtrés

    # Charger les fréquences des lettres depuis le fichier texte
    frequences_lettres: Dict[str, float] = {}
    with open(get_path("app/frequences_lettres.txt"), "r") as fichier:
        for ligne in fichier:
            ligne = ligne.strip()
            if " : " in ligne:  # Vérifie que la ligne contient " : "
                lettre, freq = ligne.split(" : ")
                frequences_lettres[lettre.strip()] = float(freq.strip())  # Nettoie aussi les espaces autour

    # Calculer la somme des fréquences pour chaque mot
    def somme_frequences(mot: str)-> float:
        return sum(frequences_lettres.get(lettre, 0) for lettre in mot)

    # Filtrer les mots avec des lettres toutes différentes
    mots_uniques: List[str] = [mot for mot in mots_filtrés if len(set(mot)) == len(mot)]

    # Afficher la somme des fréquences pour chaque mot unique
    print("Somme des fréquences pour chaque mot filtré (lettres uniques uniquement) :")
    for mot in mots_uniques:
        print(f"{mot} : {somme_frequences(mot)}")

    # Trouver le mot avec la somme maximale des fréquences parmi les mots uniques
    mot_max: Optional[str] = max(mots_uniques, key=somme_frequences, default=None)

    # Débogage : Affiche les mots possibles après filtrage
    print(f"Mots possibles après filtrage (ultime, lettres uniques) : {mots_uniques}")
    print(f"Mot proposé avec la somme maximale des fréquences (lettres uniques) : {mot_max}")

    # Retourner le mot avec la somme maximale des fréquences
    return mot_max if mot_max else (mots_filtrés[0] if mots_filtrés else None)












def jouer()-> None:
    fichier: str = get_path("app/dictionnaire_clean.txt")
    if not os.path.exists(fichier):
        print("Le fichier dictionnaire_clean.txt est introuvable.")
        return

    # Choisir la difficulté
    while True:
        print("Choisissez une difficulté :")
        print("1. Facile")
        print("2. Moyen")
        print("3. Difficile")
        print("4. Ultime")

        choix = input("Entrez 1, 2 ou 3 ou 4 si tu l'oses : ").strip()
        if choix in ["1", "2", "3","4"]:
            break
        print("Choix invalide. Réessayez.")

    niveaux_bot: Dict[str, callable] = {
        "1": bot_proposition_facile,
        "2": bot_proposition_moyen,
        "3": bot_proposition_difficile,
        "4": bot_proposition_ultime_1,

    }
    bot_propose = niveaux_bot[choix]

    mots: List[str] = charger_dictionnaire(fichier)
    mot_a_trouver: str = choisir_mot(mots)
    longueur: int = len(mot_a_trouver)
    mots_possibles: List[str] = [mot for mot in mots if len(mot) == longueur]
    historiques: List[Tuple[str, List[str]]] = []

    print(f"Le mot à trouver contient {longueur} lettres : {'_' * longueur}")
    print(mot_a_trouver)

    tour: int = 0
    while True:
        tour += 1
        print(f"\nTour {tour} :")
        mot_propose: str = input(f"Entrez un mot de {longueur} lettres : ").strip().lower()
        if len(mot_propose) != longueur:
            print("Le mot proposé n'a pas la bonne longueur.")
            continue
        if mot_propose not in mots:
            print("Le mot proposé n'existe pas dans le dictionnaire.")
            continue

        resultat_utilisateur: List[str] = [
            "vert" if mot_a_trouver[i] == mot_propose[i]
            else "orange" if mot_propose[i] in mot_a_trouver and mot_a_trouver[i] != mot_propose[i]
            else "rouge"
            for i in range(longueur)
        ]
        historiques.append((mot_propose, resultat_utilisateur))
        print("Votre proposition :", colorier_mot_graphique(mot_propose, mot_a_trouver))

        if mot_propose == mot_a_trouver:
            print("🎉 Félicitations, vous avez trouvé le mot !")
            print(f"Définition de '{mot_a_trouver}' :", obtenir_definition(mot_a_trouver))
            break

        mot_bot: Optional[str] = bot_propose(mots_possibles, historiques)
        if not mot_bot:
            print("Le bot n'a pas trouvé de mot valide.")
            break

        print(f"Le bot propose : {mot_bot}")
        resultat_bot: List[str] = [
            "vert" if mot_a_trouver[i] == mot_bot[i]
            else "orange" if mot_bot[i] in mot_a_trouver and mot_a_trouver[i] != mot_bot[i]
            else "rouge"
            for i in range(longueur)
        ]
        historiques.append((mot_bot, resultat_bot))
        print("Réponse du bot :", colorier_mot_graphique(mot_bot, mot_a_trouver))

        if mot_bot == mot_a_trouver:
            print("🤖 Le bot a trouvé le mot !")
            print(f"Définition de '{mot_a_trouver}' :", obtenir_definition(mot_a_trouver))
            break


# Lancer le jeu
if __name__ == "__main__":
    jouer()








