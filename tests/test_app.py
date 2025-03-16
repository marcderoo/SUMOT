import unittest
import os
from unittest.mock import patch, MagicMock
import requests
import json
import importlib.util

def get_path(full_path):
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

# Charger dynamiquement le module
module_name = "app"  # Nom du module sans l'extension
spec = importlib.util.spec_from_file_location(module_name, get_path("app/app.py"))
app_ = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_)

# Accès aux objets du module via app_
app, somme_frequences, get_daily_word = getattr(app_, "app", None), getattr(app_, "somme_frequences", None), getattr(app_, "get_daily_word", None)

# Mock data for testing
with open(get_path("app/small_dico.txt"), 'r') as file:
    dico = [line.strip() for line in file]
    
with open(get_path("app/frequences_lettres.txt"), "r") as file:
    frequences_lettres = {
        ligne.split(" : ")[0].strip(): float(ligne.split(" : ")[1].strip())
        for ligne in file if " : " in ligne
    }

class TestMenuRoute(unittest.TestCase):
    def setUp(self):
        # Set up a test client for the Flask app
        app.template_folder = get_path("app/templates")
        self.app = app.test_client()
        self.app.testing = True  # Enable testing mode for better error reporting

        get_daily_word()

    def test_menu_route(self):
        # Send a GET request to the '/' route
        response = self.app.get('/')
        
       
        self.assertEqual(response.status_code, 200)
    
    def test_solo_get_request(self):
        # Simulate a GET request to '/solo'
        response = self.app.get('/solo')
        
        # Assert the response status code is 200
        self.assertEqual(response.status_code, 200)
        
        
        # Assert that a random word from 'dico' is in the rendered content
        self.assertTrue(any(word.upper() in response.data.decode() for word in dico))

    def test_solo_post_request_with_valid_data(self):
        # Simulate a POST request with valid score and count
        response = self.app.post('/solo', data={'score': 10, 'count': 5})
        
        # Assert the response status code is 200
        self.assertEqual(response.status_code, 200)
        
        # Assert that the score and count are in the rendered content
        self.assertIn('10', response.data.decode())
        self.assertIn('5', response.data.decode())
        
        # Assert that a random word from 'dico' is in the rendered content
        self.assertTrue(any(word.upper() in response.data.decode() for word in dico))

    def test_solo_post_request_with_missing_data(self):
        # Simulate a POST request with missing form data
        response = self.app.post('/solo', data={})
        
        # Assert the response status code is 200
        self.assertEqual(response.status_code, 200)
        
        # Default values should be used for score and count
        self.assertIn('0', response.data.decode())  # Default score
        self.assertIn('1', response.data.decode())  # Default count
        
        # Assert that a random word from 'dico' is in the rendered content
        self.assertTrue(any(word.upper() in response.data.decode() for word in dico))
    
    def test_regles_endpoint(self):
        # Send a GET request to the /regles endpoint
        response = self.app.get('/regles')

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

    def test_daily_endpoint(self):
        res_decoded = []
        
        for i in range(2):
            # Send a GET request to the /daily endpoint
            response = self.app.get('/daily')

            # Add response content in the list
            res_decoded.append(response.data.decode())

            # Default values should be used for score and count
            self.assertIn('let score = parseInt("0");', res_decoded[-1])  # Default score
            self.assertIn('let count = parseInt("1");', res_decoded[-1])  # Default count

            real_word = [line for line in res_decoded[-1].split("\n") if line.strip().startswith('const real_word = "')][0].split('"')[1]
            
            # Assert that a random word from 'dico' is in the rendered content and that it's not the DEFAUT value
            self.assertTrue(any(word.upper() == real_word for word in dico) and real_word != "DEFAUT")

        # Check if daily send always the same content
        self.assertTrue(all(x == res_decoded[0] for x in res_decoded))

    def test_invalid_file_name(self):
        # Test for an invalid file name
        response = self.app.get('/dico/../../etc/passwd')
        self.assertEqual(response.status_code, 404)  

    def test_empty_file_name(self):
        # Test for an empty file name
        response = self.app.get('/dico/')
        self.assertEqual(response.status_code, 404)  # Flask typically handles this as 404
    
    @patch('requests.get')
    def test_valid_word(self, mock_get):
        """Test with a valid word where a definition exists."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
        <body>
            <ol>
                <li>Définition principale pour le mot.</li>
            </ol>
        </body>
        </html>
        """
        mock_get.return_value = mock_response

        with app.test_client() as client:
            response = client.get('/def/validword')
            self.assertEqual(response.data.decode(), "Définition principale pour le mot.")

    @patch('requests.get')
    def test_word_without_definition(self, mock_get):
        """Test with a word that exists but has no definitions."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
        <body>
        </body>
        </html>
        """
        mock_get.return_value = mock_response

        with app.test_client() as client:
            response = client.get('/def/nodictionaryentry')
            self.assertEqual(response.data.decode(), "err")

    @patch('requests.get')
    def test_invalid_word(self, mock_get):
        """Test with an invalid word or non-existent Wiktionary page."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with app.test_client() as client:
            response = client.get('/def/invalidword')
            self.assertEqual(response.data.decode(), "err")

    @patch('requests.get')
    def test_timeout_error(self, mock_get):
        """Test for timeout error during the request."""
        mock_get.side_effect = requests.exceptions.Timeout

        with app.test_client() as client:
            response = client.get('/def/timeoutword')
            self.assertEqual(response.data.decode(), "err")

    @patch('requests.get')
    def test_network_error(self, mock_get):
        """Test for network-related error during the request."""
        mock_get.side_effect = requests.exceptions.ConnectionError

        with app.test_client() as client:
            response = client.get('/def/networkerror')
            self.assertEqual(response.data.decode(), "err")
        
    def test_valid_word(self):
        # Test with a valid word
        self.assertAlmostEqual(somme_frequences("esi"), 0.1337 + 0.0931 + 0.0866, places=4)


    def test_empty_word(self):
        # Test with an empty string
        self.assertAlmostEqual(somme_frequences(""), 0.0, places=4)


    def test_cache_functionality(self):
        # Ensure the function uses caching by calling the same word multiple times
        result1 = somme_frequences("esi")
        result2 = somme_frequences("esi")  # Should be fetched from cache
        self.assertEqual(result1, result2)
        
        
    @patch('app.dico', ["ABRICOT", "AMBRE", "AMARRE", "AMULET", "ANANAS"]) 
    @patch('app.frequences_lettres', {"A": 0.0817, "P": 0.0193, "L": 0.0278, "E": 0.1270, "R": 0.0599, "O": 0.0751, "M": 0.0241, "B": 0.0149, "I": 0.0697, "H": 0.0609})
    def test_easy_difficulty(self):
        data = {
            "len": 5,
            "firstLetter": "A",
            "stateLetters": {},
            "validLetters": ["A", "", "", "", ""],
            "history":[]
        }

        response = self.app.post('/ia/0', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(response.get_data(as_text=True), ["ABRICOT", "AMBRE", "AMARRE", "AMULET", "ANANAS"])

    @patch('app.dico', ["MOTIVANT", "MALICIEUX", "MARTINET", "MILLIONS"])  
    @patch('app.frequences_lettres', {"A": 0.0817, "P": 0.0193, "L": 0.0278, "E": 0.1270, "R": 0.0599, "O": 0.0751, "M": 0.0241, "B": 0.0149, "I": 0.0697, "H": 0.0609})
    def test_hard_difficulty(self):
        # Define the data for the POST request
        data = {
            "len": 8,
            "firstLetter": "M",
            "stateLetters": {
                "M": {"count": 1, "posValid": [0], "posGood": [], "notMore": False},
                "A": {"count": 1, "posValid": [1], "posGood": [], "notMore": False}
            },
            "validLetters": ["M", "A", False, False, False, False, False, False],
            "history":[]
        }

        # Send the POST request
        response = self.app.post('/ia/3', data=json.dumps(data), content_type='application/json')

        # Assert the status code of the response
        self.assertEqual(response.status_code, 200)

        # Define the expected valid words for this test case
        expected_words = [ "MALICIEUX", "MARTINET"]  # Update this to reflect valid words
        response_word = response.get_data(as_text=True)

        # Assert that the response word is among the expected words
        self.assertIn(response_word, expected_words)
        
    
    @patch('app.dico', ["MOTIVANT", "MALICIEUX", "MARTINET", "MILLIONS"])  
    @patch('app.frequences_lettres', {"A": 0.0817, "P": 0.0193, "L": 0.0278, "E": 0.1270, "R": 0.0599, "O": 0.0751, "M": 0.0241, "B": 0.0149, "I": 0.0697, "H": 0.0609})
    def test_hard_difficulty2(self):
        # Define the data for the POST request
        data = {
            "len": 8,
            "firstLetter": "M",
            "stateLetters": {
                "M": {"count": 1, "posValid": [0], "posGood": [], "notMore": False}
            },
            "validLetters": ["M", False, False, False, False, False, False, False],
            "history":[]
        }

        # Send the POST request
        response = self.app.post('/ia/3', data=json.dumps(data), content_type='application/json')

        # Assert the status code of the response
        self.assertEqual(response.status_code, 200)

        # Define the expected valid words for this test case
        expected_words = ["MOTIVANT", "MALICIEUX", "MARTINET", "MILLIONS"]  # Updated expected words
        response_word = response.get_data(as_text=True)

        # Assert that the response word is among the expected words
        self.assertIn(response_word, expected_words)
    



if __name__ == '__main__':
    unittest.main()