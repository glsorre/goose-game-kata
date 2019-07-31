from io import StringIO

import unittest
from unittest.mock import patch

import main
 
class TestAdd(unittest.TestCase):

    def test_get_other_indexes(self):
        positions = [7, 11, 11]

        expected_output = 'players: Giorgio\nGiorgio : already existing player\nplayers: Giorgio, Franco\nFranco : already existing player'

        output = main.get_others_indexes(positions, 0, 11)
        self.assertEqual(output, [1, 2])

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
            'move Franco 2, 3'
        ]

        expected_output = 'players: Giorgio\nGiorgio rolls 3, 4. Giorgio moves from Start to 7\nGiorgio rolls 2, 2. Giorgio moves from 7 to 11\nplayers: Giorgio, Franco\nFranco rolls 3, 4. Franco moves from Start to 7\nFranco rolls 2, 3. Franco moves from 7 to 12'

        with patch('builtins.input', side_effect=user_input), patch('sys.stdout', new_callable=StringIO) as out:
            players, positions = main.main(5)

        output = out.getvalue().strip()
        self.assertEqual(output, expected_output)
        self.assertEqual(players, ['Giorgio', 'Franco'])
        self.assertEqual(positions, [11, 12])

    def test_move_player_with_rolling(self):
        user_input = [
            'add player Giorgio',
            'move Giorgio'
        ]

        expected_output = r'players: Giorgio\nGiorgio rolls \d+\, \d+\. Giorgio moves from Start to .*'

        with patch('builtins.input', side_effect=user_input), patch('sys.stdout', new_callable=StringIO) as out:
            players, positions = main.main(1)

        output = out.getvalue().strip()
        self.assertRegex(output, expected_output)

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

    def test_the_prank(self):
        user_input = [
            'add player Giorgio',
            'add player Franco',
            'move Giorgio 0, 10',
            'move Franco 2, 8'
        ]

        expected_output = 'players: Giorgio\nplayers: Giorgio, Franco\nGiorgio rolls 0, 10. Giorgio moves from Start to 10\nFranco rolls 2, 8. Franco moves from Start to 10. On 10 there is Giorgio, who returns to Start'

        with patch('builtins.input', side_effect=user_input), patch('sys.stdout', new_callable=StringIO) as out:
            players, positions = main.main(3)

        output = out.getvalue().strip()
        self.assertEqual(output, expected_output)
        self.assertEqual(players, ['Giorgio', 'Franco'])
        self.assertEqual(positions, [0, 10])

    def test_the_prank_double(self):
        user_input = [
            'add player Giorgio',
            'add player Franco',
            'add player Luca',
            'move Giorgio 3, 2',
            'move Franco 3, 2',
            'move Luca 10, 0'
        ]

        expected_output = 'players: Giorgio\nplayers: Giorgio, Franco\nplayers: Giorgio, Franco, Luca\nGiorgio rolls 3, 2. Giorgio moves from Start to 5, The Goose. Giorgio moves again and goes to 10\nFranco rolls 3, 2. Franco moves from Start to 5, The Goose. Franco moves again and goes to 10. On 10 there is Giorgio, who returns to Start\nLuca rolls 10, 0. Luca moves from Start to 10. On 10 there is Franco, who returns to Start'

        with patch('builtins.input', side_effect=user_input), patch('sys.stdout', new_callable=StringIO) as out:
            players, positions = main.main(5)

        output = out.getvalue().strip()
        self.assertEqual(output, expected_output)
        self.assertEqual(players, ['Giorgio', 'Franco', 'Luca'])
        self.assertEqual(positions, [0, 0, 10])

    def test_full_match(self):
        with patch('builtins.input', return_value='move Giorgio'):
            players, positions = main.main(-1, ['Giorgio'])

        self.assertEqual(players, ['Giorgio'])
        self.assertEqual(positions, [63])
 
if __name__ == '__main__':
    unittest.main()