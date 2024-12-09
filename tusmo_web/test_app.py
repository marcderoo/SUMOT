import unittest
from flask import Flask
from app import app  

import random

# Mock data for testing
with open("small_dico.txt", 'r') as file:
    dico = [line.strip() for line in file]

class TestMenuRoute(unittest.TestCase):
    def setUp(self):
        # Set up a test client for the Flask app
        self.app = app.test_client()
        self.app.testing = True  # Enable testing mode for better error reporting

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

        

if __name__ == '_main_':
    unittest.main()