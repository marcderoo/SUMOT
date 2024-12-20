import unittest
from unittest.mock import mock_open, patch, MagicMock
import random
from typing import List, Tuple, Optional
from mode_battleIA import charger_dictionnaire



class TestChargerDictionnaire(unittest.TestCase):
    def test_charger_dictionnaire(self):
        # Mock file content
        mock_file_content = "mot1\nmot2\n\nmot3\n"
        
        # Patch the open function
        with patch("builtins.open", mock_open(read_data=mock_file_content)) as mocked_file:
            fichier = "dictionnaire_clean.txt"
            expected_output = ["mot1", "mot2", "mot3"]

            # Call the function
            result = charger_dictionnaire(fichier)

            # Assertions
            mocked_file.assert_called_once_with(fichier, "r", encoding="utf-8")
            self.assertEqual(result, expected_output)
    
    
    

    

if __name__ == "__main__":
    unittest.main()