from io import StringIO

import unittest
from unittest.mock import patch

import main
 
class TestAdd(unittest.TestCase):

    def test_add_player(self):
        user_input = [
            'add player Giorgio',
            'add player Giorgio',
            'add player Franco',
            'add player Franco'
        ]

        expected_output = 'players: Giorgio\nGiorgio : already existing player\nplayers: Giorgio, Franco\nFranco : already existing player'

        with patch('builtins.input', side_effect=user_input), patch('sys.stdout', new_callable=StringIO) as out:
            players, positions = main.main(3)

        output = out.getvalue().strip()
        self.assertEqual(output, expected_output)
        self.assertEqual(players, ['Giorgio', 'Franco'])
        self.assertEqual(positions, [0, 0])

    def test_move_player(self):
        user_input = [
            'add player Giorgio',
            'move Giorgio 3, 4',
            'move Giorgio 2, 2',
            'add player Franco',
            'move Franco 3, 4',
            'move Franco 2, 2'
        ]

        expected_output = 'players: Giorgio\nGiorgio rolls 3, 4. Giorgio moves from Start to 7\nGiorgio rolls 2, 2. Giorgio moves from 7 to 11\nplayers: Giorgio, Franco\nFranco rolls 3, 4. Franco moves from Start to 7\nFranco rolls 2, 2. Franco moves from 7 to 11'

        with patch('builtins.input', side_effect=user_input), patch('sys.stdout', new_callable=StringIO) as out:
            players, positions = main.main(5)

        output = out.getvalue().strip()
        self.assertEqual(output, expected_output)
        self.assertEqual(players, ['Giorgio', 'Franco'])
        self.assertEqual(positions, [11, 11])

    def test_player_wins(self):
        user_input = [
            'add player Giorgio',
            'move Giorgio 63, 0'
        ]

        expected_output = 'players: Giorgio\nGiorgio rolls 63, 0. Giorgio moves from Start to 63. Giorgio Wins!!'

        with patch('builtins.input', side_effect=user_input), patch('sys.stdout', new_callable=StringIO) as out:
            players, positions = main.main()

        output = out.getvalue().strip()
        self.assertEqual(output, expected_output)
        self.assertEqual(players, ['Giorgio'])
        self.assertEqual(positions, [63])

    def test_player_bounces(self):
        user_input = [
            'add player Giorgio',
            'move Giorgio 60, 0',
            'move Giorgio 3, 2'
        ]

        expected_output = 'players: Giorgio\nGiorgio rolls 60, 0. Giorgio moves from Start to 60\nGiorgio rolls 3, 2. Giorgio moves from 60 to 63. Giorgio bounces! Giorgio returns to 61'

        with patch('builtins.input', side_effect=user_input), patch('sys.stdout', new_callable=StringIO) as out:
            players, positions = main.main(2)

        output = out.getvalue().strip()
        self.assertEqual(output, expected_output)
        self.assertEqual(players, ['Giorgio'])
        self.assertEqual(positions, [61])

    def test_the_bridge(self):
        user_input = [
            'add player Giorgio',
            'move Giorgio 6, 0'
        ]

        expected_output = 'players: Giorgio\nGiorgio rolls 6, 0. Giorgio moves from Start to The Bridge. Giorgio jumps to 12'

        with patch('builtins.input', side_effect=user_input), patch('sys.stdout', new_callable=StringIO) as out:
            players, positions = main.main(1)

        output = out.getvalue().strip()
        self.assertEqual(output, expected_output)
        self.assertEqual(players, ['Giorgio'])
        self.assertEqual(positions, [12])

    def test_the_goose_single(self):
        user_input = [
            'add player Giorgio',
            'move Giorgio 3, 0',
            'move Giorgio 1, 1'
        ]

        expected_output = 'players: Giorgio\nGiorgio rolls 3, 0. Giorgio moves from Start to 3\nGiorgio rolls 1, 1. Giorgio moves from 3 to 5, The Goose. Giorgio moves again and goes to 7'

        with patch('builtins.input', side_effect=user_input), patch('sys.stdout', new_callable=StringIO) as out:
            players, positions = main.main(2)

        output = out.getvalue().strip()
        self.assertEqual(output, expected_output)
        self.assertEqual(players, ['Giorgio'])
        self.assertEqual(positions, [7])

    def test_the_goose_double(self):
        user_input = [
            'add player Giorgio',
            'move Giorgio 10, 0',
            'move Giorgio 2, 2'
        ]

        expected_output = 'players: Giorgio\nGiorgio rolls 10, 0. Giorgio moves from Start to 10\nGiorgio rolls 2, 2. Giorgio moves from 10 to 14, The Goose. Giorgio moves again and goes to 18, The Goose. Giorgio moves again and goes to 22'

        with patch('builtins.input', side_effect=user_input), patch('sys.stdout', new_callable=StringIO) as out:
            players, positions = main.main(2)

        output = out.getvalue().strip()
        self.assertEqual(output, expected_output)
        self.assertEqual(players, ['Giorgio'])
        self.assertEqual(positions, [22])
 
if __name__ == '__main__':
    unittest.main()