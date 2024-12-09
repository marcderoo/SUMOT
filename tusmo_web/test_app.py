import unittest
import os
import sys
from flask import Flask

# Configurer le chemin pour inclure le répertoire tusmo_web
CURRENT_DIR = os.getcwd()
TUSMO_WEB_DIR = os.path.join(CURRENT_DIR, "tusmo_web")
sys.path.insert(0, TUSMO_WEB_DIR)

# Chemin pour les fichiers nécessaires
DICO_DIR = os.path.join(TUSMO_WEB_DIR, "dico")
SMALL_DICO_PATH = os.path.join(DICO_DIR, "small_dico.txt")
FREQUENCES_PATH = os.path.join(TUSMO_WEB_DIR, "frequences_lettres.txt")

# Créer les fichiers nécessaires pour les tests
os.makedirs(DICO_DIR, exist_ok=True)
if not os.path.exists(SMALL_DICO_PATH):
    with open(SMALL_DICO_PATH, "w") as f:
        f.write("mot1\nmot2\nmot3")

if not os.path.exists(FREQUENCES_PATH):
    with open(FREQUENCES_PATH, "w") as f:
        f.write("e : 0.1061\ns : 0.0970\ni : 0.0935\n")

# Changer temporairement le répertoire courant pour tusmo_web
os.chdir(TUSMO_WEB_DIR)

# Importer l'application Flask
from app import app

# Revenir au répertoire initial après l'importation
os.chdir(CURRENT_DIR)

class TestApp(unittest.TestCase):
    """Tests pour les routes de l'application Flask."""

    def setUp(self):
        """Configurer le client Flask pour les tests."""
        self.client = app.test_client()
        self.client.testing = True

    def test_home_route(self):
        """Test de la route d'accueil."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"SUMOT", response.data)  # Adaptez ce texte selon ce qui est attendu

    def test_dico_file_route(self):
        """Test de la route dico/<filename>."""
        response = self.client.get('/dico/small_dico.txt')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"mot1", response.data)  # Vérifie le contenu du fichier

    def test_frequencies_route(self):
        """Test de la route des fréquences des lettres."""
        response = self.client.get('/frequences')
        self.assertEqual(response.status_code, 404)  # Adaptez selon votre logique

    def test_random_word_route(self):
        """Test de la route qui renvoie un mot aléatoire."""
        response = self.client.get('/solo')
        self.assertEqual(response.status_code, 200)

    def test_not_found_route(self):
        """Test d'une route inexistante."""
        response = self.client.get('/unknown_route')
        self.assertEqual(response.status_code, 404)

    @classmethod
    def tearDownClass(cls):
        """Supprimer les fichiers créés pour les tests."""
    # Supprimer les fichiers dans le répertoire DICO_DIR
        for filename in os.listdir(DICO_DIR):
            file_path = os.path.join(DICO_DIR, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)  # Supprimer le fichier
            except Exception as e:
                print(f"Erreur lors de la suppression du fichier {file_path}: {e}")
    # Supprimer le répertoire DICO_DIR
        try:
            os.rmdir(DICO_DIR)
        except Exception as e:
            print(f"Erreur lors de la suppression du répertoire {DICO_DIR}: {e}")


if __name__ == "__main__":
    unittest.main()
