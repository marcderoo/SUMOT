"""
Script for generating or manipulating dictionaries
"""

import os
from typing import Set
from tqdm import tqdm

def get_path(full_path: str) -> str:
    """
    Get the full path of a file in the project.
    """
    root = os.path.dirname(os.path.abspath(__file__))

    # Go up until we find the LICENSE file
    while not os.path.exists(os.path.join(root, "LICENSE")):
        new_root = os.path.dirname(root)
        if new_root == root:  # Évite une boucle infinie
            raise FileNotFoundError("LICENSE file not found")
        root = new_root
    if "\\" in root :
        full_path = full_path.replace("/", "\\")
    else:
        full_path = full_path.replace("\\", "/")
    return str(os.path.join(root, full_path))

def organize_words(input_file_local: str, scnd_input_file_local: \
                    str, output_dir_local: str) -> None:
    """
    Organize words from a file into a folder structure.

    Args:
        input_file_local (str): Path to the input file where each line contains one word.
        output_dir_local (str): Path to the output directory to organize the words.
    """
    # Assure que le répertoire de sortie existe
    os.makedirs(output_dir_local, exist_ok=True)

    # Charger les mots depuis le fichier
    with open(input_file_local, 'r', encoding='utf-8') as file:
        words: Set[str] = set([line.strip() for line in file \
            if line.strip() and len(line) >= 7 and len(line) <= 10])  # Retirer les espaces vides

    # Charger les mots depuis le fichier
    with open(scnd_input_file_local, 'r', encoding='utf-8') as file:
        words = words.union(set([line.strip() for line in file \
            if line.strip() and len(line) >= 7 and len(line) <= 10]))  # Retirer les espaces vides

    # Progression sur les mots
    for word in tqdm(words, desc="Processing words"):
        if not word:  # Ignore les lignes vides
            continue

        # Déterminer la lettre initiale et la longueur
        first_letter: str = word[0].upper()
        word_length: int = len(word)

        # Créer le fichier pour la longueur et y ajouter le mot
        file_path: str = os.path.join(output_dir_local, f"{first_letter}_{word_length}.txt")
        with open(file_path, 'a', encoding="utf-8") as file:
            file.write(word + "\n")

# Exemple d'utilisation
input_file_local: str = get_path("app/dictionnaire_clean.txt")  #chemin vers votre fichier d'entrée
scnd_input_file_local: str = get_path("app/small_dico.txt")
output_dir_local: str = get_path("app/dico")  # Répertoire de sortie
organize_words(input_file_local, scnd_input_file_local, output_dir_local)
