import os
from tqdm import tqdm
from typing import Set

def organize_words(input_file: str, scnd_input_file: str, output_dir: str) -> None:
    """
    Organize words from a file into a folder structure.

    Args:
        input_file (str): Path to the input file where each line contains one word.
        output_dir (str): Path to the output directory to organize the words.
    """
    # Assure que le répertoire de sortie existe
    os.makedirs(output_dir, exist_ok=True)

    # Charger les mots depuis le fichier
    with open(input_file, 'r') as file:
        words: Set[str] = set([line.strip() for line in file if line.strip() and len(line) >= 7 and len(line) <= 10])  # Retirer les espaces vides
  
    # Charger les mots depuis le fichier
    with open(scnd_input_file, 'r') as file:
        words = words.union(set([line.strip() for line in file if line.strip() and len(line) >= 7 and len(line) <= 10]))  # Retirer les espaces vides

    # Progression sur les mots
    for word in tqdm(words, desc="Processing words"):
        if not word:  # Ignore les lignes vides
            continue

        # Déterminer la lettre initiale et la longueur
        first_letter: str = word[0].upper()
        word_length: int = len(word)

        # Créer le fichier pour la longueur et y ajouter le mot
        file_path: str = os.path.join(output_dir, f"{first_letter}_{word_length}.txt")
        with open(file_path, 'a') as file:
            file.write(word + "\n")

# Exemple d'utilisation
input_file: str = "dictionnaire_clean.txt"  # Remplacez par le chemin vers votre fichier d'entrée
scnd_input_file: str = "small_dico.txt"
output_dir: str = "dico"  # Répertoire de sortie
organize_words(input_file, scnd_input_file, output_dir)