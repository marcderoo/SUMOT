import unittest
from unittest.mock import mock_open, patch, MagicMock
import random
from typing import List, Tuple, Optional
from mode_battleIA import charger_dictionnaire, mode_battle_ia
import os

def get_path(full_path: str) -> str:
    """
    Get the full path of a file in the project.
    """
    root = os.path.dirname(os.path.abspath(__file__))

    # Go up until we find the LICENSE file
    while not os.path.exists(os.path.join(root, "LICENSE")):
        root = os.path.dirname(root)
    return os.path.join(root, full_path)

class TestChargerDictionnaire(unittest.TestCase):
    def test_charger_dictionnaire(self):
        # Mock file content
        mock_file_content = "mot1\nmot2\n\nmot3\n"
        
        # Patch the open function
        with patch("builtins.open", mock_open(read_data=mock_file_content)) as mocked_file:
            fichier = get_path("app/dictionnaire_clean.txt")
            expected_output = ["mot1", "mot2", "mot3"]

            # Call the function
            result = charger_dictionnaire(fichier)

            # Assertions
            mocked_file.assert_called_once_with(fichier, "r", encoding="utf-8")
            self.assertEqual(result, expected_output)
    

    @patch("mode_battleIA.random.choice")
    @patch("mode_battleIA.charger_dictionnaire")
    def test_mode_battle_ia(self, mock_charger_dictionnaire, mock_random_choice):
        # Simulate a dictionary of words
        mock_charger_dictionnaire.return_value = ["mot1", "mot2", "mot3"]

        # Use a generator to produce infinite "mot1"
        mock_random_choice.side_effect = (x for x in ["mot1"] * 10000)  # Infinite generator

        # Mock os.path.exists to ensure the dictionary file is "found"
        with patch("mode_battleIA.os.path.exists", return_value=True):
            # Run the function
            mode_battle_ia()

            # Check that the dictionary was loaded
            mock_charger_dictionnaire.assert_called_once_with(get_path("app/dictionnaire_clean.txt"))

            # Log the call count to verify behavior
            print(f"random.choice called {mock_random_choice.call_count} times")
    

    

if __name__ == "__main__":
    unittest.main()