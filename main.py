import random
import re

WIN_POSITION = 63
BRIDGE_HEAD = 6
BRIDGE_TAIL = 12
DICE_FACE = 6
GOOSES = [5, 9, 14, 18, 23, 27]

def get_old_label(old_position):
    if old_position == 0:
        old_label = "Start"
    else:
        old_label = old_position
    return old_label

def get_new_label(new_position):
    if new_position in GOOSES:
        new_label = f"{new_position}, The Goose. "
    elif new_position == 6:
        new_label = "The Bridge."
    elif new_position > 63:
        new_label = 63
    else:
        new_label = new_position
    return new_label

class Player():
    def __init__(self, name):
        self.name = name
        self.position = 0

class BillBoard():
    def __init__(self):
        self.players = []

    def __contains__(self, player):
        return player.name in self.get_players_name()

    def add_player(self, player):
        if player in self:
            print(player.name, ": already existing player")
        else:
            self.players.append(player)
            print("players:", ", ".join(self.get_players_name()))

    def get_player(self, name):
        return next(filter(lambda player: player.name == name, self.players))

    def move_player_goose(self, name, n1, n2):
        player = self.get_player(name)

        player.position += (n1 + n2)

        old_position = player.position
        new_position = old_position + n1 + n2

        if new_position in GOOSES:
            print(f"{name} moves again and goes to {new_position}, The Goose. ", end="")
            self.move_player_goose(name, n1, n2)
        else:
            print(f"{name} moves again and goes to {new_position}")

    def move_player(self, name, n1, n2):
        player = self.get_player(name)
        
        old_position = player.position
        new_position = old_position + n1 + n2

        old_label = get_old_label(old_position)
        new_label = get_new_label(new_position)

        print(f"{name} rolls {n1}, {n2}. {name} moves from {old_label} to {new_label}", end="")

        if new_position in GOOSES:
            self.move_player_goose(name, n1, n2)

        elif new_position == BRIDGE_HEAD:
            new_position = BRIDGE_TAIL
            print(f" {name} jumps to {BRIDGE_TAIL}", end="")

        elif new_position == WIN_POSITION:
            print(f". {name} Wins!!")
        
        elif new_position > WIN_POSITION:
            new_position = WIN_POSITION - (new_position - WIN_POSITION)
            print(f". {name} bounces! {name} returns to {new_position}")

        print("")
        player.position = new_position
            
    def get_players_name(self):
        return [player.name for player in self.players]

def main():
    billboard = BillBoard()
    while True:
        cmd = input('Insert your command: ')
        if cmd == 'exit':
            break

        elif cmd.startswith("add player"):
            player = Player(cmd.split()[2])
            billboard.add_player(player)

        elif cmd.startswith("move"):
            p = re.compile('^move (\w*) (\d+), (\d+)$')
            match = p.match(cmd)
            result = p.search(cmd)
            if match:
                billboard.move_player(result.group(1), int(result.group(2)), int(result.group(3)))
            else:
                billboard.move_player(cmd.split()[1], random.randint(1, DICE_FACE), random.randint(1, DICE_FACE))

if __name__ == '__main__':
    main()
