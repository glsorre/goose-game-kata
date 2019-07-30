import random
import re

CUBE_FACES = 6

def print_players(players):
    print('players:', ', '.join(players))


def add_player(players, positions, not_won, result):
    if result.group(1) in players:
        print(result.group(1), ': already existing player')
    else:
        players.append(result.group(1))
        positions.append(0)
        print_players(players)


def move_player(players, positions, not_won, result, rolling=False):
    try:
        index = players.index(result.group(1))
    except ValueError:
        print('The player', result.group(1), 'does not exist.')
    else:
        cube_one = roll_dice(CUBE_FACES) if rolling else result.group(2)
        cube_two = roll_dice(CUBE_FACES) if rolling else result.group(3)
        steps = int(cube_one) + int(cube_two)
        old_position = positions[index]
        positions[index] += int(steps)

        msg_components = [
            players[index],
            cube_one,
            cube_two,
            players[index],
            'Start' if old_position == 0 else old_position,
            positions[index],
            players[index],
        ]

        if positions[index] == 63:
            print('{} rolls {}, {}. {} moves from {} to {}. {} Wins!!'.format(*msg_components))
            not_won[0] = False
        else:
            print('{} rolls {}, {}. {} moves from {} to {}'.format(*msg_components))

def roll_dice(cube_faces):
    return random.randint(1, cube_faces)

def move_player_with_rolling(players, positions, not_won, result):
    move_player(players, positions, not_won, result, True)

REGEXES = [
    r'^add player (.*)$',
    r'^move (\w*)(?!\d+, \d+)$',
    r'^move (\w*) (\d+), (\d+)$'
]

FUNCTIONS = [
    add_player,
    move_player_with_rolling,
    move_player
]


def main(commands_number=-1):
    escaper = True
    players = []
    positions = []
    not_won = [True]

    while not_won[0] and escaper:
        if commands_number == 0:
            escaper = False

        cmd = input('Insert your command: ')

        for i, regex in enumerate(REGEXES):
            result = re.match(regex, cmd)
            if result:
                FUNCTIONS[i](players, positions, not_won, result)
                break
            
            if i == len(REGEXES) - 1:
                print('Invalid command!')

        if commands_number != -1:
            commands_number -= 1


if __name__ == '__main__':
    main()
