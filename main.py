import re

players = []
not_won = True
regexes = [
    r'Hello World!'
]

def main():
    while not_won:
        cmd = input('Insert your command: ')
        
        result = ''

        for regex in regexes:
            result = re.match(regex, cmd)

        if result:
            print('valid command')
        else:
            print('Invalid command!')

if __name__ == "__main__":
    main()
