players = []

def main():
    while True:
        command = input()
        if command.startswith("add player"):
            player = command.split()[2]
            if player not in players:
                players.append(player)
                print("players:", ", ".join(players))
            else:
                print(player, ": already existing player")

if __name__ == '__main__':
    main()
