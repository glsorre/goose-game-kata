import re


def print_players(players):
    print('players:', ', '.join(players))


def add_player(players, positions, not_won, result):
    if result.group(1) in players:
        print(result.group(1), ': already existing player')
    else:
        players.append(result.group(1))
        positions.append(0)
        print_players(players)


def move_player(players, positions, not_won, result):
    try:
        index = players.index(result.group(1))
    except ValueError:
        print('The player', result.group(1), 'does not exist.')
    else:
        steps = int(result.group(2)) + int(result.group(3))
        old_position = positions[index]
        positions[index] += int(steps)

        msg_components = [
            players[index],
            result.group(2),
            result.group(3),
            players[index],
            'Start' if old_position == 0 else old_position,
            positions[index]
        ]

        print('{} rolls {}, {}. {} moves from {} to {}'.format(*msg_components))


REGEXES = [
    r'^add player (.*)$',
    r'^move (.*) (\d), (\d)$'
]

FUNCTIONS = [
    add_player,
    move_player
]


def main(commands_number = -1):
    escaper = True
    players = []
    positions = []
    not_won = True

    while not_won and escaper:
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


if __name__ == "__main__":
    main()
