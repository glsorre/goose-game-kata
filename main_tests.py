from io import StringIO

import unittest
from unittest.mock import patch

import main
from main import BillBoard, Player
 
class TestAddPlayer(unittest.TestCase):

    def setUp(self):
        self.billboard = BillBoard()

    def test_player_instantiation(self):
        player = Player("Franco")
        self.assertEqual(player.name, "Franco")
        self.assertEqual(player.position, 0)

    def test_add_player(self):
        player = Player("Franco")
        self.billboard.add_player(player)
        self.assertEqual(self.billboard.get_players_name(), ['Franco'])
        player = Player("Francois")
        self.billboard.add_player(player)
        self.assertEqual(self.billboard.get_players_name(), ['Franco', 'Francois'])

    def test_acceptance(self):
        user_input = [
            'add player Giorgio',
            'add player Giorgio',
            'add player Franco',
            'add player Franco',
            'exit'
        ]

        expected_output = 'players: Giorgio\nGiorgio : already existing player\nplayers: Giorgio, Franco\nFranco : already existing player'

        with patch('builtins.input', side_effect=user_input), patch('sys.stdout', new_callable=StringIO) as out:
            main.main()
        
        output = out.getvalue().strip()
        self.assertEqual(output, expected_output)

class TestMovePlayer(unittest.TestCase):

    def setUp(self):
        self.billboard = BillBoard()
        self.player1 = Player("Franco")
        self.billboard.add_player(self.player1)
        self.player2 = Player("Francois")
        self.billboard.add_player(self.player2)

    def test_get_player(self):
        player1 = self.billboard.get_player('Franco')
        player2 = self.billboard.get_player('Francois')
        self.assertEqual(player1, self.player1)
        self.assertEqual(player2, self.player2)

    def test_acceptance(self):
        user_input = [
            'add player Giorgio',
            'move Giorgio 3, 4',
            'move Giorgio 2, 2',
            'add player Franco',
            'move Franco 3, 4',
            'move Franco 2, 3',
            'exit'
        ]

        expected_output = 'players: Giorgio\nGiorgio rolls 3, 4. Giorgio moves from Start to 7\nGiorgio rolls 2, 2. Giorgio moves from 7 to 11\nplayers: Giorgio, Franco\nFranco rolls 3, 4. Franco moves from Start to 7\nFranco rolls 2, 3. Franco moves from 7 to 12'

        with patch('builtins.input', side_effect=user_input), patch('sys.stdout', new_callable=StringIO) as out:
            main.main()

        output = out.getvalue().strip()
        self.assertEqual(output, expected_output)

class TestWinBouncePlayer(unittest.TestCase):

    def test_acceptance_wins(self):
        user_input = [
            'add player Giorgio',
            'move Giorgio 63, 0',
            'exit'
        ]

        expected_output = 'players: Giorgio\nGiorgio rolls 63, 0. Giorgio moves from Start to 63. Giorgio Wins!!'

        with patch('builtins.input', side_effect=user_input), patch('sys.stdout', new_callable=StringIO) as out:
            main.main()

        output = out.getvalue().strip()
        self.assertEqual(output, expected_output)

    def test_acceptance_bounce(self):
        user_input = [
            'add player Giorgio',
            'move Giorgio 60, 0',
            'move Giorgio 3, 2',
            'exit'
        ]

        expected_output = 'players: Giorgio\nGiorgio rolls 60, 0. Giorgio moves from Start to 60\nGiorgio rolls 3, 2. Giorgio moves from 60 to 63. Giorgio bounces! Giorgio returns to 61'

        with patch('builtins.input', side_effect=user_input), patch('sys.stdout', new_callable=StringIO) as out:
            main.main()

        output = out.getvalue().strip()
        self.assertEqual(output, expected_output)

class TestBridgePlayer(unittest.TestCase):

    def test_acceptance(self):
        user_input = [
            'add player Giorgio',
            'move Giorgio 6, 0',
            'exit'
        ]

        expected_output = 'players: Giorgio\nGiorgio rolls 6, 0. Giorgio moves from Start to The Bridge. Giorgio jumps to 12'

        with patch('builtins.input', side_effect=user_input), patch('sys.stdout', new_callable=StringIO) as out:
            main.main()

        output = out.getvalue().strip()
        self.assertEqual(output, expected_output)

class TestGoosePlayer(unittest.TestCase):
    def test_the_goose_single(self):
        user_input = [
            'add player Giorgio',
            'move Giorgio 3, 0',
            'move Giorgio 1, 1',
            'exit'
        ]

        expected_output = 'players: Giorgio\nGiorgio rolls 3, 0. Giorgio moves from Start to 3\nGiorgio rolls 1, 1. Giorgio moves from 3 to 5, The Goose. Giorgio moves again and goes to 7'

        with patch('builtins.input', side_effect=user_input), patch('sys.stdout', new_callable=StringIO) as out:
            main.main()

        output = out.getvalue().strip()
        self.assertEqual(output, expected_output)

    def test_the_goose_double(self):
        user_input = [
            'add player Giorgio',
            'move Giorgio 10, 0',
            'move Giorgio 2, 2',
            'exit'
        ]

        expected_output = 'players: Giorgio\nGiorgio rolls 10, 0. Giorgio moves from Start to 10\nGiorgio rolls 2, 2. Giorgio moves from 10 to 14, The Goose. Giorgio moves again and goes to 18, The Goose. Giorgio moves again and goes to 22'

        with patch('builtins.input', side_effect=user_input), patch('sys.stdout', new_callable=StringIO) as out:
            main.main()

        output = out.getvalue().strip()
        self.assertEqual(output, expected_output)
 
if __name__ == '__main__':
    unittest.main()