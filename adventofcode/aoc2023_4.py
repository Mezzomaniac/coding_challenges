from downloader import download

download(2023, 4)
with open('aoc2023_4input.txt') as inputfile:
    data = inputfile.read()
print(data)

def calculate_wins(line):
    winning, mine = [group.split() for group in line[line.index(':') + 1:].split('|')]
    return sum(number in winning for number in mine)

score = 0
cards = [1 for card in data.splitlines()]
for i, line in enumerate(data.splitlines()):
    wins = calculate_wins(line)
    if wins:
        score += 2 ** (wins - 1)
    for j in range(wins):
        cards[i + j + 1] += cards[i]
print(score)
print(sum(cards))
