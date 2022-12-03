from downloader import download

download(2022, 2)
with open('aoc2022_2input.txt') as inputfile:
    data = inputfile.read()
print(data)

translation = str.maketrans('XYZ', 'ABC')
translated = data.translate(translation)
values = {'A': 1, 'B': 2, 'C': 3}
defeats = {'A': 'C', 'B': 'A', 'C': 'B'}

score = 0
for line in translated.splitlines():
    opponent, me = line.split(' ')
    score += values[me]
    if opponent == me:
        score += 3
    elif defeats[me] == opponent:
        score += 6
print(score)

score = 0
for line in data.splitlines():
    opponent, me = line.split(' ')
    if me == 'X':
        score += values[defeats[opponent]]
    elif me == 'Y':
        score += values[opponent] + 3
    else:
        score += values[(set('ABC') - {opponent, defeats[opponent]}).pop()] + 6
print(score)
