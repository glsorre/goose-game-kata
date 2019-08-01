import random
import re

CUBE_FACES = 6
WIN_POSITION = 63
BRIDGE_START = 6
BRIDGE_ARRIVE = 12
GOOSES = [5, 9, 14, 18, 23, 27]

def print_players(players):
    print('players:', ', '.join(players))

def add_player(players, positions, result):
    if result.group(1) in players:
        print(result.group(1), ': already existing player')
    else:
        players.append(result.group(1))
        positions.append(0)
        print_players(players)

def get_others_indexes(positions, index, new_position):
    result = []
    for i, position in enumerate(positions):
        if position == new_position and i != index:
            result.append(i)
    return result

def move_player_basic(name, index, positions, players, steps):
    old_position = positions[index]
    new_position = old_position + steps
    move_player_to_position(index, positions, new_position)
    return old_position, new_position

def build_msg_components(name, cube_one, cube_two, old_position, new_position):
    msg_components = {
      'name': name,
      'cube_one': cube_one,
      'cube_two': cube_two,
      'old_position': 'Start' if old_position == 0 else old_position,
      'new_position': new_position,
      'bridge_arrive': BRIDGE_ARRIVE,
      'win_position': WIN_POSITION
    }
    
    if new_position > WIN_POSITION:
        msg_components['new_position'] = WIN_POSITION
    elif new_position == BRIDGE_START:
        msg_components['new_position'] = 'The Bridge'
    
    return msg_components

def get_player_id(name, players):
    try: index = players.index(name)
    except ValueError: print('The player', name, 'does not exist.')
    return index

def match_ended(not_won, msg_components):
    print(MSGS['win'].format(**msg_components))
    not_won[0] = False

def roll_dice(cube_faces):
    return random.randint(1, cube_faces)

def build_movements(result, rolling):
    cube_one = roll_dice(CUBE_FACES) if rolling else result.group(2)
    cube_two = roll_dice(CUBE_FACES) if rolling else result.group(3)
    steps = int(cube_one) + int(cube_two)
    return cube_one, cube_two, steps

def move_player(players, positions, not_won, with_rolling, result):
    name = result.group(1)
    index = get_player_id(name, players)
    if index is not None:
        cube_one, cube_two, steps = build_movements(result, with_rolling)
        old_position, new_position = move_player_basic(name, index, positions, players, steps)
        msg_components = build_msg_components(name, cube_one, cube_two, old_position, new_position)

        print(MSGS['rolls'].format(**msg_components), end='')
        print(MSGS['move'].format(**msg_components), end='')

        if new_position == WIN_POSITION:
            match_ended(not_won, msg_components)
        elif new_position > WIN_POSITION:
            new_position = bounce_player(index, positions, msg_components)
        elif new_position == BRIDGE_START:
            new_position = move_player_bridge(index, positions, BRIDGE_ARRIVE, msg_components)
        elif new_position in GOOSES:
            print(MSGS['goose_start'].format(**msg_components), end='')
            new_position = move_player_gooses(index, positions, new_position, steps, msg_components)

        others_indexes = get_others_indexes(positions, index, new_position)

        if others_indexes:
            move_players_prank(positions, players, old_position, new_position, msg_components, others_indexes)

        print('')

def move_player_to_position(index, positions, position):
    positions[index] = position

def move_player_bridge(index, positions, position, msg_components):
    print(MSGS['bridge'].format(**msg_components), end='')
    move_player_to_position(index, positions, position)
    return position

def bounce_player(index, positions, msg_components):
    print(MSGS['bounce_start'].format(**msg_components), end='')
    bounce = positions[index] - WIN_POSITION
    new_position = WIN_POSITION - bounce
    move_player_to_position(index, positions, new_position)
    print(MSGS['bounce_end'].format(msg_components['name'], new_position), end='')
    return new_position

def move_player_gooses(index, positions, old_position, steps, msg_components):
    new_position = old_position + steps
    if new_position in GOOSES:
        print(MSGS['goose_middle'].format(msg_components['name'], new_position), end='')
        move_player_gooses(index, positions, new_position, steps, msg_components)
    else:
        print(MSGS['goose_end'].format(msg_components['name'], new_position), end='')
        move_player_to_position(index, positions, new_position)
        return new_position

def move_players_prank(positions, players, old_position, new_position, msg_components, others_indexes):
    for i, other_index in enumerate(others_indexes):
        msg = MSGS['prank'].format(new_position, players[other_index], msg_components['old_position'], end='')
        if i == len(others_indexes) - 1:
            print(msg, end='')
        else:
            print(msg, end='')
        move_player_to_position(other_index, positions, old_position) 
    
REGEXES = [
    r'^add player (.*)$',
    r'^move (\w*)$',
    r'^move (\w*) (\d+), (\d+)$'
]

FUNCTIONS = [
    add_player,
    move_player,
    move_player
]

MSGS = {
    'rolls':        '{name} rolls {cube_one}, {cube_two}. ',
    'win':          '. {name} Wins!!',
    'bounce_start': '. {name} bounces! ',
    'bounce_end':   '{} returns to {}',
    'bridge':       '. {name} jumps to {bridge_arrive}',
    'goose_start':  ', The Goose. ',
    'goose_middle': '{} moves again and goes to {}, The Goose. ',
    'goose_end':    '{} moves again and goes to {}',
    'move':         '{name} moves from {old_position} to {new_position}',
    'prank':        '. On {} there is {}, who returns to {}'
}

def initialize(initialization):
    players = []
    positions = []

    if initialization is not None:
        players = initialization
        positions = [0 for x in initialization]

    return players, positions

def main(commands_number=-1, initialization=None):
    escaper = True
    not_won = [True]
    players, positions = initialize(initialization)

    function_args = [
      [players, positions],
      [players, positions, not_won, True],
      [players, positions, not_won, False]
    ]

    while not_won[0] and escaper:
        if commands_number == 0: escaper = False

        cmd = input('Insert your command: ')

        for i, regex in enumerate(REGEXES):
            result = re.match(regex, cmd)
            if result:
                FUNCTIONS[i](*function_args[i], result)
                break

            if i == len(REGEXES) - 1: print('Invalid command!')

        if commands_number != -1: commands_number -= 1

    return players, positions

if __name__ == '__main__':
    main()
