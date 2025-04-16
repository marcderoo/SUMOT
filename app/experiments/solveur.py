"""Script de nettoyage et d'analyse de fréquence des mots pour le projet SUMOT."""

import os
import re
from typing import List, Set, Dict
from collections import Counter
import unidecode

def get_path(full_path: str) -> str:
    """
    Obtenir le chemin absolu vers un fichier à partir de la racine du projet.
    """
    root = os.path.dirname(os.path.abspath(__file__))

    # Monter jusqu'à trouver le fichier LICENSE
    while not os.path.exists(os.path.join(root, "LICENSE")):
        new_root = os.path.dirname(root)
        if new_root == root:
            raise FileNotFoundError("LICENSE file not found")
        root = new_root

    if "\\" in root:
        full_path = full_path.replace("/", "\\")
    else:
        full_path = full_path.replace("\\", "/")
    return os.path.join(root, full_path)

# Lecture du dictionnaire original
with open(get_path("app/experiments/dictionnaire.txt"), "r", encoding="utf-8") as fichier:
    mots: List[str] = fichier.readlines()

# Nettoyage des mots
mots_corriges: Set[str] = set()
for mot in mots:
    mot = mot.strip().lower()
    if mot and re.match(r"^[a-zA-Z]+$", mot):
        mot_sans_accents = unidecode.unidecode(mot)
        mots_corriges.add(mot_sans_accents)

# Écriture dans un nouveau fichier nettoyé
with open(get_path("app/dictionnaire_clean.txt"), "w", encoding="utf-8") as fichier_clean:
    fichier_clean.write("\n".join(sorted(mots_corriges)))

print(f"{len(mots_corriges)} mots valides ont été conservés après nettoyage.")

# Analyse des fréquences de lettres
with open(get_path("app/dictionnaire_clean.txt"), "r", encoding="utf-8") as fichier:
    mots: List[str] = fichier.readlines()

texte: str = "".join(mots)
compteur: Counter = Counter(texte)
total_lettres: int = sum(compteur.values())

frequences: Dict[str, float] = {
    lettre: compteur[lettre] / total_lettres for lettre in compteur
}

frequences_triees: Dict[str, float] = dict(
    sorted(frequences.items(), key=lambda x: x[1], reverse=True)
)

print("Fréquence des lettres (par ordre décroissant) :")
for lettre, freq in frequences_triees.items():
    print(f"{lettre} : {freq:.4f}")

with open(get_path("app/frequences_lettres.txt"), "w", encoding="utf-8") as fichier_freq:
    for lettre, freq in frequences_triees.items():
        fichier_freq.write(f"{lettre} : {freq:.4f}\n")
