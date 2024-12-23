import unittest
import os
from collections import Counter
import unidecode
import re

class TestDictionaryProcessing(unittest.TestCase):

    def setUp(self):
        # Create a sample dictionary file for testing
        self.input_file = "test_dictionnaire.txt"
        self.output_file = "test_dictionnaire_clean.txt"
        self.frequency_file = "test_frequences_lettres.txt"
        self.sample_words = [
            "Bonjour",
            "monde",
            "Python",
            "école",
            "test"
        ]
        with open(self.input_file, "w", encoding="utf-8") as f:
            f.write("\n".join(self.sample_words))

        # Run the original processing script code here
        # The first part of the script
        with open(self.input_file, "r", encoding="utf-8") as fichier:
            mots = fichier.readlines()

        mots_corriges = set()
        for mot in mots:
            mot = mot.strip().lower()
            if mot and re.match(r"^[a-zA-Z]+$", mot):
                mot_sans_accents = unidecode.unidecode(mot)
                mots_corriges.add(mot_sans_accents)

        with open(self.output_file, "w", encoding="utf-8") as fichier_clean:
            fichier_clean.write("\n".join(sorted(mots_corriges)))

        # The second part of the script
        with open(self.output_file, "r", encoding="utf-8") as fichier:
            mots = fichier.readlines()

        texte = "".join(mots)
        compteur = Counter(texte)
        total_lettres = sum(compteur.values())
        self.frequences = {lettre: compteur[lettre] / total_lettres for lettre in compteur}

        # Sort frequencies for tests
        self.frequences_triees = dict(sorted(self.frequences.items(), key=lambda x: x[1], reverse=True))

    def tearDown(self):
        # Remove the files created during testing
        if os.path.exists(self.input_file):
            os.remove(self.input_file)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        if os.path.exists(self.frequency_file):
            os.remove(self.frequency_file)

    def test_cleaned_words(self):
        with open(self.output_file, "r", encoding="utf-8") as f:
            cleaned_words = f.read().strip().split("\n")
            self.assertIn("bonjour", cleaned_words)
            self.assertIn("monde", cleaned_words)
            self.assertIn("python", cleaned_words)

    def test_letter_frequencies(self):
        self.assertGreater(len(self.frequences_triees), 0)  # There should be some frequencies calculated
        self.assertIn('e', self.frequences_triees)  # Checking if the letter 'e' is in the frequencies
        self.assertIn('o', self.frequences_triees)  # Checking if the letter 'o' is in the frequencies
        self.assertAlmostEqual(self.frequences_triees['o'], 0.2, places=1)  # Adjust expected value as needed

if __name__ == "__main__":
    unittest.main()