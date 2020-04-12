import re 

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

    def move_player(self, name, n1, n2):
        player = self.get_player(name)
        old_position = player.position
        player.position = old_position + n1 + n2
        print(f"{name} rolls {n1}, {n2}. {name} moves from {'Start' if old_position == 0 else old_position} to {player.position}")
        return player.position
            
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
            result = p.search(cmd)
            billboard.move_player(result.group(1), int(result.group(2)), int(result.group(3)))

if __name__ == '__main__':
    main()
