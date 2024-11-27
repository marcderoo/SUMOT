import random
import os

from bs4 import BeautifulSoup
import requests


def obtenir_definition(mot):
    """Récupère uniquement la définition principale pour le mot depuis le Wiktionnaire."""
    url = f"https://fr.wiktionary.org/wiki/{mot}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            definition = soup.find("ol")  # Trouve la liste ordonnée
            if definition:
                premier_element = definition.find("li")  # Trouve la première entrée de la liste
                if premier_element:
                    # Ne garde que le texte avant les points ou les puces inutiles
                    texte_principal = premier_element.text.split("\n")[0]  # Sépare sur les sauts de ligne et prend le premier élément
                    return texte_principal.strip()  # Nettoie les espaces autour du texte
        return "Définition introuvable."
    except Exception as e:
        return f"Erreur lors de la récupération de la définition : {e}"




def charger_dictionnaire(fichier):
    """Charge les mots du fichier dictionnaire_clean.txt dans une liste."""
    with open(fichier, "r", encoding="utf-8") as f:
        mots = [ligne.strip() for ligne in f.readlines() if ligne.strip()]
    return mots


def choisir_mot(mots):
    """Choisit un mot aléatoire depuis la liste des mots."""
    return random.choice(mots)



def colorier_mot_graphique(mot_propose, mot_a_trouver):
    """Retourne un mot coloré graphiquement avec des lettres :
    - Vert pour correcte et bien placée
    - Orange pour présente mais mal placée
    - Rouge pour absente.
    """
    resultat = []
    mot_a_trouver_temp = list(mot_a_trouver)  # Copie modifiable du mot à trouver

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




def bot_proposition_facile(mots_possibles, historiques):
    """Le bot se base uniquement sur les lettres bien placées (vertes) pour faire ses propositions."""
    for proposition, resultat in historiques:
        nouveaux_mots = []
        for mot in mots_possibles:
            valide = True
            for i, lettre in enumerate(proposition):
                # Vérifie uniquement les lettres "vertes"
                if resultat[i] == "vert" and mot[i] != lettre:
                    valide = False
                    break
            if valide:
                nouveaux_mots.append(mot)
        mots_possibles = nouveaux_mots if nouveaux_mots else mots_possibles
    return random.choice(mots_possibles) if mots_possibles else None




def bot_proposition_moyen(mots_possibles, historiques):
    """Le bot se base sur les lettres bien placées (vertes) et les lettres correctes mais mal placées (oranges)."""
    for proposition, resultat in historiques:
        nouveaux_mots = []
        for mot in mots_possibles:
            valide = True
            mot_temp = list(mot)  # Copie modifiable pour traquer les lettres oranges
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



def bot_proposition_difficile(mots_possibles, historiques):
    """Le bot utilise toutes les couleurs pour filtrer les mots possibles, sans gestion de lettres consommées."""
    mots_filtrés = mots_possibles.copy()  # Travail sur une copie pour préserver l'original

    for proposition, resultat in historiques:
        nouveaux_mots = []
        for mot in mots_filtrés:
            valide = True

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
                    indices_orange_vert = [
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
    print(f"Mots possibles après filtrage (difficile) : {mots_filtrés}")

    return random.choice(mots_filtrés) if mots_filtrés else None



def jouer():
    fichier = "dictionnaire_clean.txt"
    if not os.path.exists(fichier):
        print("Le fichier dictionnaire_clean.txt est introuvable.")
        return

    # Choisir la difficulté
    while True:
        print("Choisissez une difficulté :")
        print("1. Facile")
        print("2. Moyen")
        print("3. Difficile")
        choix = input("Entrez 1, 2 ou 3 : ").strip()
        if choix in ["1", "2", "3"]:
            break
        print("Choix invalide. Réessayez.")

    niveaux_bot = {
        "1": bot_proposition_facile,
        "2": bot_proposition_moyen,
        "3": bot_proposition_difficile,
    }
    bot_propose = niveaux_bot[choix]

    mots = charger_dictionnaire(fichier)
    mot_a_trouver = choisir_mot(mots)
    longueur = len(mot_a_trouver)
    mots_possibles = [mot for mot in mots if len(mot) == longueur]
    historiques = []

    print(f"Le mot à trouver contient {longueur} lettres : {'_' * longueur}")
    print(mot_a_trouver)

    tour = 0
    while True:
        tour += 1
        print(f"\nTour {tour} :")
        mot_propose = input(f"Entrez un mot de {longueur} lettres : ").strip().lower()
        if len(mot_propose) != longueur:
            print("Le mot proposé n'a pas la bonne longueur.")
            continue
        if mot_propose not in mots:
            print("Le mot proposé n'existe pas dans le dictionnaire.")
            continue

        resultat_utilisateur = [
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

        mot_bot = bot_propose(mots_possibles, historiques)
        if not mot_bot:
            print("Le bot n'a pas trouvé de mot valide.")
            break

        print(f"Le bot propose : {mot_bot}")
        resultat_bot = [
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

