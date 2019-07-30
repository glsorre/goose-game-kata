from io import StringIO

import unittest
from unittest.mock import patch

import main
from main import add_player, print_players
 
class TestAdd(unittest.TestCase):

    def test_add_player(self):
        user_input = [
            'add player Giorgio',
            'add player Giorgio'
        ]

        expected_output = 'players: Giorgio\nGiorgio : already existing player'

        with patch('builtins.input', side_effect=user_input), patch('sys.stdout', new_callable=StringIO) as out:
            main.main(1)

        output = out.getvalue().strip()
        self.assertEqual(output, expected_output)

    def test_move_player(self):
        user_input = [
            'add player Giorgio',
            'move Giorgio 3, 4',
            'move Giorgio 2, 2'
        ]

        expected_output = 'players: Giorgio\nGiorgio rolls 3, 4. Giorgio moves from Start to 7\nGiorgio rolls 2, 2. Giorgio moves from 7 to 11'

        with patch('builtins.input', side_effect=user_input), patch('sys.stdout', new_callable=StringIO) as out:
            main.main(2)

        output = out.getvalue().strip()
        self.assertEqual(output, expected_output)

    def test_player_wins(self):
        user_input = [
            'add player Giorgio',
            'move Giorgio 63, 0'
        ]

        expected_output = 'players: Giorgio\nGiorgio rolls 63, 0. Giorgio moves from Start to 63. Giorgio Wins!!'

        with patch('builtins.input', side_effect=user_input), patch('sys.stdout', new_callable=StringIO) as out:
            main.main()

        output = out.getvalue().strip()
        self.assertEqual(output, expected_output)

 
if __name__ == '__main__':
    unittest.main()