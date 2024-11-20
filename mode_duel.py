import random
import os

from bs4 import BeautifulSoup


def obtenir_definition(mot):
    """Récupère une définition pour le mot depuis une source externe (exemple avec Wiktionary)."""
    url = f"https://fr.wiktionary.org/wiki/{mot}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            definition = soup.find("ol")
            if definition:
                return definition.find("li").text
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
    return "parc"


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


def bot_proposition(mots_possibles, longueur, historiques):
    """
    Propose un mot intelligent en filtrant les mots possibles en fonction des historiques.
    """
    for proposition, resultat in historiques:
        nouveaux_mots = []
        for mot in mots_possibles:
            valide = True
            mot_temp = list(mot)  # Copie modifiable pour vérifier les lettres

            # Vérifier chaque lettre dans la proposition précédente
            for i, lettre in enumerate(proposition):
                if resultat[i] == "vert":  # Lettre correcte et bien placée
                    if mot[i] != lettre:
                        valide = False
                        break
                elif resultat[i] == "orange":  # Lettre présente mais mal placée
                    if lettre not in mot_temp or mot[i] == lettre:
                        valide = False
                        break
                    mot_temp[mot_temp.index(lettre)] = None  # Consommer la lettre
                elif resultat[i] == "rouge":  # Lettre absente du mot
                    if lettre in mot_temp:
                        valide = False
                        break

            if valide:
                nouveaux_mots.append(mot)

        # Réduire les mots possibles
        mots_possibles = nouveaux_mots

    # Si aucun mot valide n'est trouvé
    if not mots_possibles:
        print("Aucune correspondance trouvée. Le bot réinitialise sa liste.")
        return random.choice(historiques[0][0])  # Réutiliser un mot connu pour ne pas bloquer
    return random.choice(mots_possibles)


def jouer():
    fichier = "dictionnaire_clean.txt"
    if not os.path.exists(fichier):
        print("Le fichier dictionnaire_clean.txt est introuvable.")
        return

    mots = charger_dictionnaire(fichier)
    mot_a_trouver = choisir_mot(mots)
    longueur = len(mot_a_trouver)
    mots_possibles = [mot for mot in mots if len(mot) == longueur]  # Mots de la bonne longueur
    historiques = []  # Historique des propositions et résultats

    print(f"Le mot à trouver contient {longueur} lettres : {'_' * longueur}")

    tour = 0
    while True:
        # Tour de l'utilisateur
        tour += 1
        print(f"\nTour {tour} :")
        mot_propose = input(f"Entrez un mot de {longueur} lettres : ").strip().lower()
        if len(mot_propose) != longueur:
            print("Le mot proposé n'a pas la bonne longueur.")
            continue
        if mot_propose not in mots:
            print("Le mot proposé n'existe pas dans le dictionnaire.")
            continue

        # Afficher le résultat pour l'utilisateur
        resultat_utilisateur = colorier_mot_graphique(mot_propose, mot_a_trouver)
        print("Votre proposition :", resultat_utilisateur)

        # Ajouter au historique
        historique_utilisateur = [
            ("vert" if mot_a_trouver[i] == mot_propose[i] else
             "orange" if mot_propose[i] in mot_a_trouver and mot_a_trouver[i] != mot_propose[i] else
             "rouge")
            for i in range(longueur)
        ]
        historiques.append((mot_propose, historique_utilisateur))

        if mot_propose == mot_a_trouver:
            print("🎉 Félicitations, vous avez trouvé le mot !")
            definition = obtenir_definition(mot_a_trouver)
            (f"Définition de '{mot_a_trouver}' : {definition}")
            break

        # Tour du bot
        mot_bot = bot_proposition(mots_possibles, longueur, historiques)
        if not mot_bot:
            print("Le bot n'a pas trouvé de mot valide.")
            break

        print(f"Le bot propose : {mot_bot}")
        resultat_bot = colorier_mot_graphique(mot_bot, mot_a_trouver)
        print("Réponse du bot :", resultat_bot)

        # Ajouter au historique pour le bot
        historique_bot = [
            ("vert" if mot_a_trouver[i] == mot_bot[i] else
             "orange" if mot_bot[i] in mot_a_trouver and mot_a_trouver[i] != mot_bot[i] else
             "rouge")
            for i in range(longueur)
        ]
        historiques.append((mot_bot, historique_bot))

        if mot_bot == mot_a_trouver:
            print("🤖 Le bot a trouvé le mot !")
            definition = obtenir_definition(mot_a_trouver)
            print(f"Définition de '{mot_a_trouver}' : {definition}")
            break


# Lancer le jeu
if __name__ == "__main__":
    jouer()
