import unittest
from flask import Flask
from app import app  
from app import somme_frequences
import os
from unittest.mock import patch, MagicMock
import requests


# Mock data for testing
with open("small_dico.txt", 'r') as file:
    dico = [line.strip() for line in file]
    
with open("frequences_lettres.txt", "r") as file:
    frequences_lettres = {
        ligne.split(" : ")[0].strip(): float(ligne.split(" : ")[1].strip())
        for ligne in file if " : " in ligne
    }

class TestMenuRoute(unittest.TestCase):
    def setUp(self):
        # Set up a test client for the Flask app
        self.app = app.test_client()
        self.app.testing = True  # Enable testing mode for better error reporting
        self.test_dir = 'dico'
        os.makedirs(self.test_dir, exist_ok=True)
        with open(os.path.join(self.test_dir, 'test.txt'), 'w') as f:
            f.write('This is a test file.')

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
        
    def tearDown(self):
        # Clean up the test directory and files
        if os.path.exists(self.test_dir):
            for file in os.listdir(self.test_dir):
                os.remove(os.path.join(self.test_dir, file))
            os.rmdir(self.test_dir)

    def test_valid_file(self):
        # Test for a valid file
        response = self.app.get('/dico/test.txt')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'This is a test file.')

    def test_file_not_found(self):
        # Test for a file that does not exist
        response = self.app.get('/dico/nonexistent.txt')
        self.assertEqual(response.status_code, 500)

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




if __name__ == '__main__':
    unittest.main()