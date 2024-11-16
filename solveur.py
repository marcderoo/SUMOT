# Contient le code Python pour le solveur (
# les algorithmes d’analyse des mots, les suggestions, les mises à jour des listes rouges/jaunes/noires).

# Liste de 336531 mots du français 
# (source (Pythoud, C. (1998) Français-GUTenberg : un nouveau dictionnaire français pour ISPELL. problèmes résolus et intégration de contributions extérieures Cahiers GUTenberg, n° 28-29, p. 252-275 (pdf) )) 
# https://github.com/chrplr/openlexicon/tree/master/datasets-info/Liste-de-mots-francais-Gutenberg

import unidecode
import re

# Lire le fichier dictionnaire.txt (dictionnaire original)
with open("dictionnaire.txt", "r", encoding="utf-8") as fichier:
    mots = fichier.readlines()

# Transformer les mots en minuscules, enlever les accents et supprimer les espaces et les traits d'union
mots_corriges = set()  # Utiliser un set pour éliminer les doublons
for mot in mots:
    mot = mot.strip().lower()  # Nettoyer le mot (enlever les espaces autour et le mettre en minuscule)
    
    # Vérifier si le mot n'est pas vide et contient des caractères valides avant de le traiter
    if mot and re.match(r"^[a-zA-Z]+$", mot):  # Vérifier si le mot contient uniquement des lettres
        mot_sans_accents = unidecode.unidecode(mot)  # Enlever les accents
        mots_corriges.add(mot_sans_accents)  # Ajouter au set

# Sauvegarder les mots corrigés dans un fichier dictionnaire_clean.txt
with open("dictionnaire_clean.txt", "w", encoding="utf-8") as fichier_clean:
    fichier_clean.write("\n".join(sorted(mots_corriges)))  # Trier avant d'écrire

# Afficher un message de confirmation
print(f"{len(mots_corriges)} mots valides ont été conservés après nettoyage.")







# Problème : il compte l'espace comme une lettre je crois

from collections import Counter

# Lire le fichier nettoyé
with open("dictionnaire_clean.txt", "r", encoding="utf-8") as fichier:
    mots = fichier.readlines()

# Joindre tous les mots en une seule chaîne
texte = "".join(mots)

# Compter la fréquence des lettres
compteur = Counter(texte)

# Total des lettres pour calculer les fréquences relatives
total_lettres = sum(compteur.values())

# Calcul des fréquences relatives
frequences = {lettre: compteur[lettre] / total_lettres for lettre in compteur}

# Trier les lettres par fréquence décroissante
frequences_triees = dict(sorted(frequences.items(), key=lambda x: x[1], reverse=True))

# Afficher les fréquences triées
print("Fréquence des lettres (par ordre décroissant) :")
for lettre, freq in frequences_triees.items():
    print(f"{lettre} : {freq:.4f}")

# Optionnel : Sauvegarder dans un fichier
with open("frequences_lettres.txt", "w", encoding="utf-8") as fichier_freq:
    for lettre, freq in frequences_triees.items():
        fichier_freq.write(f"{lettre} : {freq:.4f}\n")
