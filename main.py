import random
import re

CUBE_FACES = 6
WIN_POSITION = 63
BRIDGE_START = 6
BRIDGE_ARRIVE = 12
GOOSES = [5, 9, 14, 18, 23, 27]

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
        old_position = positions[index]
        cube_one, cube_two, steps = build_movements(result, rolling)
        new_position = old_position + steps
        move_player_to_position(index, positions, old_position + steps)

        msg_components = {
            'name': players[index],
            'cube_one': cube_one,
            'cube_two': cube_two,
            'old_position': 'Start' if old_position == 0 else old_position,
            'new_position': positions[index],
            'bridge_arrive': BRIDGE_ARRIVE
        }

        if positions[index] == WIN_POSITION:
            print('{name} rolls {cube_one}, {cube_two}. {name} moves from {old_position} to {new_position}. {name} Wins!!'.format(**msg_components))
            not_won[0] = False
        elif positions[index] == BRIDGE_START:
            print('{name} rolls {cube_one}, {cube_two}. {name} moves from {old_position} to The Bridge. {name} jumps to {bridge_arrive}'.format(**msg_components))
            move_player_to_position(index, positions, BRIDGE_ARRIVE)
        elif positions[index] in GOOSES:
            print('{name} rolls {cube_one}, {cube_two}. {name} moves from {old_position} to {new_position}, The Goose. '.format(**msg_components),  end='')
            move_player_gooses(index, positions, new_position, steps, players)
        else:
            print('{name} rolls {cube_one}, {cube_two}. {name} moves from {old_position} to {new_position}'.format(**msg_components))

def roll_dice(cube_faces):
    return random.randint(1, cube_faces)

def build_movements(result, rolling):
    cube_one = roll_dice(CUBE_FACES) if rolling else result.group(2)
    cube_two = roll_dice(CUBE_FACES) if rolling else result.group(3)
    steps = int(cube_one) + int(cube_two)

    return cube_one, cube_two, steps

def move_player_with_rolling(players, positions, not_won, result):
    move_player(players, positions, not_won, result, True)

def move_player_to_position(index, positions, position):
    positions[index] = position

def move_player_gooses(index, positions, old_position, steps, players):
    new_position = old_position + steps
    if new_position in GOOSES:
        print('{} moves again and goes to {}, The Goose. '.format(players[index], new_position), end='')
        move_player_gooses(index, positions, new_position, steps, players)
    else:
        move_player_to_position(index, positions, new_position)
        print('{} moves again and goes to {}'.format(players[index], new_position))

REGEXES = [
    r'^add player (.*)$',
    r'^move (\w*)$',
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

    return players, positions


if __name__ == '__main__':
    main()
