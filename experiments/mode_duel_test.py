import unittest
from unittest.mock import patch, MagicMock,mock_open
import experiments.mode_duel as mode_duel
from experiments.mode_duel import jouer


class TestObtenirDefinition(unittest.TestCase):

    @patch('mode_duel.requests.get')
    def test_definition_larousse_success(self, mock_get):
        # Mocking a successful response from Larousse
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<ul class="Definitions"><li>Test Larousse Definition</li></ul>'
        mock_get.return_value = mock_response

        result = mode_duel.obtenir_definition("test")
        self.assertIn("(Source: Larousse)", result)
        self.assertIn("Test Larousse Definition", result)

    @patch('mode_duel.requests.get')
    def test_definition_wiktionnaire_success(self, mock_get):
        # Mocking a successful response from Wiktionary when Larousse fails
        def side_effect(url, headers):
            if "larousse.fr" in url:
                mock_larousse_response = MagicMock()
                mock_larousse_response.status_code = 404  # Simulate Larousse failure
                return mock_larousse_response
            elif "wiktionary.org" in url:
                mock_wiktionary_response = MagicMock()
                mock_wiktionary_response.status_code = 200
                mock_wiktionary_response.text = '<ol><li>Test Wiktionnaire Definition</li></ol>'
                return mock_wiktionary_response

        mock_get.side_effect = side_effect

        result = mode_duel.obtenir_definition("test")
        self.assertIn("(Source: Wiktionnaire)", result)
        self.assertIn("Test Wiktionnaire Definition", result)

    @patch('mode_duel.requests.get')
    def test_definition_not_found(self, mock_get):
        # Mocking a case where both Larousse and Wiktionary fail
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = mode_duel.obtenir_definition("test")
        self.assertEqual(result, "Aucune définition trouvée pour ce mot.")

    @patch('mode_duel.requests.get')
    def test_definition_larousse_malformed_response(self, mock_get):
        # Mocking a malformed response from Larousse
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<ul class="Definitions"></ul>'  # No definition available
        mock_get.return_value = mock_response

        result = mode_duel.obtenir_definition("test")
        self.assertNotIn("(Source: Larousse)", result)
    
    def test_charger_dictionnaire(self):
        # Mock content of the dictionary file
        mock_file_content = "lapin\nchien\nchat\n\n"
        with patch("builtins.open", mock_open(read_data=mock_file_content)) as mock_file:
            mots = mode_duel.charger_dictionnaire("dictionnaire_clean.txt")
            # Verify the content of the loaded list
            self.assertEqual(mots, ["lapin", "chien", "chat"])
            # Ensure the file was opened correctly
            mock_file.assert_called_once_with("dictionnaire_clean.txt", "r", encoding="utf-8")
    
    def test_choisir_mot(self):
        # Mock list of words
        mots = ["lapin", "chien", "chat"]
        # Force the function to always return "lapin"
        with patch("random.choice", return_value="lapin"):
            mot = mode_duel.choisir_mot(mots)
            # Verify that the chosen word is "lapin"
            self.assertEqual(mot, "lapin")
    
    def test_no_historic_guesses(self):
        mots_possibles = ["chat", "chien", "lapin"]
        historiques = []
        result = mode_duel.bot_proposition_facile(mots_possibles, historiques)
        self.assertIn(result, mots_possibles)

    
    def test_single_valid_word(self):
        mots_possibles = ["lapin", "lapis", "chien"]
        historiques = [("lapin", ["vert", "vert", "vert", "vert", "vert"])]
        result = mode_duel.bot_proposition_facile(mots_possibles, historiques)
        self.assertEqual(result, "lapin")

    def test_multiple_valid_words(self):
        mots_possibles = ["lapin", "lapis", "lapel"]
        historiques = [("lap__", ["vert", "vert", "vert", "absent", "absent"])]
        result = mode_duel.bot_proposition_facile(mots_possibles, historiques)
        self.assertIn(result, ["lapin", "lapis", "lapel"])

    def test_empty_word_list(self):
        mots_possibles = []
        historiques = [("chat", ["vert", "vert", "absent", "absent"])]
        result = mode_duel.bot_proposition_facile(mots_possibles, historiques)
        self.assertIsNone(result)
    
    def test_no_historic_guesses(self):
        mots_possibles = ["chat", "chien", "lapin"]
        historiques = []
        result = mode_duel.bot_proposition_moyen(mots_possibles, historiques)
        self.assertIn(result, mots_possibles)

    def test_vert_only(self):
        mots_possibles = ["lapin", "lapis", "lapel"]
        historiques = [("lap__", ["vert", "vert", "vert", "absent", "absent"])]
        result = mode_duel.bot_proposition_moyen(mots_possibles, historiques)
        self.assertIn(result, ["lapin", "lapis", "lapel"])


    def test_empty_word_list(self):
        mots_possibles = []
        historiques = [("lapin", ["vert", "vert", "absent", "absent"])]
        result = mode_duel.bot_proposition_moyen(mots_possibles, historiques)
        self.assertIsNone(result)
    
    def test_no_historic_guesses(self):
        mots_possibles = ["chat", "chien", "lapin"]
        historiques = []
        result = mode_duel.bot_proposition_difficile(mots_possibles, historiques)
        self.assertIn(result, mots_possibles)

    def test_vert_only(self):
        mots_possibles = [ "chien", "lapin"]
        historiques = [("ch__n", ["vert", "vert", "absent", "absent", "vert"])]
        result = mode_duel.bot_proposition_difficile(mots_possibles, historiques)
        self.assertIn(result, ["chien"])    

    def test_orange_letter_condition(self):
        mots_possibles = ["lapin", "lesar", "palin"]
        historiques = [("lapin", ["vert", "orange", "absent", "absent", "absent"])]
        result = mode_duel.bot_proposition_difficile(mots_possibles, historiques)
        self.assertIn(result, ["lesar"])

    

    
    def test_all_correct(self):
        mot_propose = "chat"
        mot_a_trouver = "chat"
        result = mode_duel.colorier_mot_graphique(mot_propose, mot_a_trouver)
        expected = "\033[92mc\033[0m\033[92mh\033[0m\033[92ma\033[0m\033[92mt\033[0m"  
        self.assertEqual(result, expected)

    

    def test_some_incorrect_some_wrong(self):
        mot_propose = "cahr"
        mot_a_trouver = "chat"
        result = mode_duel.colorier_mot_graphique(mot_propose, mot_a_trouver)
        expected = "\x1b[92mc\x1b[0m\x1b[93ma\x1b[0m\x1b[93mh\x1b[0m\x1b[91mr\x1b[0m"  
        self.assertEqual(result, expected)

    def test_letters_present_but_misplaced(self):
        mot_propose = "atch"
        mot_a_trouver = "chat"
        result = mode_duel.colorier_mot_graphique(mot_propose, mot_a_trouver)
        expected = "\x1b[93ma\x1b[0m\x1b[93mt\x1b[0m\x1b[93mc\x1b[0m\x1b[93mh\x1b[0m"  
        self.assertEqual(result, expected)

    def test_letters_not_present(self):
        mot_propose = "abcd"
        mot_a_trouver = "chat"
        result = mode_duel.colorier_mot_graphique(mot_propose, mot_a_trouver)
        expected = "\x1b[93ma\x1b[0m\x1b[91mb\x1b[0m\x1b[93mc\x1b[0m\x1b[91md\x1b[0m"  
        self.assertEqual(result, expected)



class TestBotPropositionUltime(unittest.TestCase):
    def setUp(self):
        # Sample list of possible words
        self.mots_possibles = [
            "laser", "lacer", "local", "logic", "liver", "lemon", "lodge", "lapse"
        ]

        # Sample historical data
        self.historiques = [
            ("laser", ["vert", "rouge", "rouge", "orange", "vert"]),
            ("lacer", ["rouge", "vert", "rouge", "rouge", "rouge"]),
        ]

        # Mock frequency data
        self.frequency_data = """l : 0.1
            a : 0.2
            s : 0.3
            e : 0.15
            r : 0.1
            c : 0.05
            o : 0.2
            g : 0.1
            i : 0.1
            v : 0.05
            p : 0.05
            """

    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_bot_proposition_ultime_with_mocked_file(self, mock_file):
        # Setup mock file return value
        mock_file.return_value.__enter__.return_value.read.return_value = self.frequency_data

        # Call the function
        result = mode_duel.bot_proposition_ultime_1(self.mots_possibles, self.historiques)

        # Expected result based on filtering and frequency logic
        expected_result = "laser"  

        # Assert that the result is as expected
        self.assertEqual(result, expected_result)


    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_bot_proposition_ultime_multiple_valid_words(self, mock_file):
        # Setup mock file return value
        mock_file.return_value.__enter__.return_value.read.return_value = self.frequency_data

        # Add more historical guesses that should leave multiple valid words
        historiques_multiple_valid = [
            ("laser", ["vert", "rouge", "rouge", "orange", "vert"]),
            ("liver", ["rouge", "vert", "rouge", "rouge", "rouge"]),
        ]

        # Call the function
        result = mode_duel.bot_proposition_ultime_1(self.mots_possibles, historiques_multiple_valid)

        # Here, we expect the result to be the word with the highest frequency sum
        expected_result = "laser"  

        # Assert that the result is as expected
        self.assertEqual(result, expected_result)
        
    
    
    
    @patch("builtins.input", side_effect=["1", "mottest"])  # Mock user inputs
    @patch("builtins.print")  # Mock print to suppress output
    @patch("os.path.exists", return_value=True)  # Mock file existence check
    @patch("mode_duel.charger_dictionnaire", return_value=["mottest", "autre"])  # Mock dictionary loading
    @patch("mode_duel.choisir_mot", return_value="mottest")  # Mock word selection
    @patch("mode_duel.colorier_mot_graphique", return_value="🎨 Mot coloré")  # Mock color formatting
    @patch("mode_duel.obtenir_definition", return_value="Un mot de test.")  # Mock word definition
    @patch("mode_duel.bot_proposition_facile", return_value="mottest")  # Mock bot behavior for difficulty 1
    def test_jouer_successful_game(
        self, mock_bot, mock_definition, mock_color, mock_choose_word,
        mock_load_dict, mock_exists, mock_print, mock_input
    ):
        jouer()
    
        # Assert the dictionary file was checked for existence
        mock_exists.assert_called_once_with("dictionnaire_clean.txt")
        
        # Assert the dictionary was loaded
        mock_load_dict.assert_called_once_with("dictionnaire_clean.txt")
        
        # Assert the chosen word was "mottest"
        mock_choose_word.assert_called_once_with(["mottest", "autre"])
        
        # Assert print was called with the congratulatory message
        mock_print.assert_any_call("🎉 Félicitations, vous avez trouvé le mot !")
        mock_print.assert_any_call("Définition de 'mottest' :", "Un mot de test.")
        
        
    @patch("builtins.input", side_effect=["5", "1", "invalide", "mottest"])  # Mock invalid and valid inputs
    @patch("builtins.print")  # Mock print to suppress output
    @patch("os.path.exists", return_value=False)  # Mock file not found
    def test_jouer_file_not_found(self, mock_exists, mock_print, mock_input):
        jouer()
        
        # Assert the dictionary file was checked for existence
        mock_exists.assert_called_once_with("dictionnaire_clean.txt")
        
        # Assert print was called with the file-not-found message
        mock_print.assert_any_call("Le fichier dictionnaire_clean.txt est introuvable.")

    @patch("builtins.input", side_effect=["1", "mauvailongueur", "mottest"])  # Mock inputs with wrong word length
    @patch("builtins.print")  # Mock print to suppress output
    @patch("os.path.exists", return_value=True)  # Mock file existence check
    @patch("mode_duel.charger_dictionnaire", return_value=["mottest", "autre"])  # Mock dictionary loading
    @patch("mode_duel.choisir_mot", return_value="mottest")  # Mock word selection
    def test_jouer_invalid_word_length(
        self, mock_choose_word, mock_load_dict, mock_exists, mock_print, mock_input
    ):
        jouer()
        
        # Assert print was called with the length error message
        mock_print.assert_any_call("Le mot proposé n'a pas la bonne longueur.")
    


    

if __name__ == "__main__":
    unittest.main()