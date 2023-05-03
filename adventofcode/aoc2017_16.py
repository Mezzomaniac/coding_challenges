from downloader import download
from string import ascii_lowercase

download(2017, 16)
with open('aoc2017_16input.txt') as inputfile:
    data = inputfile.read()
print(data)

def dance(programs, moves):
    for move in moves.split(','):
        if move.startswith('s'):
            x = int(move[1:])
            programs = programs[-x:] + programs[:-x]
        elif move.startswith('x'):
            a, b = (int(i) for i in move[1:].split('/'))
            programs[a], programs[b] = programs[b], programs[a]
        elif move.startswith('p'):
            a, b = (programs.index(i) for i in move[1:].split('/'))
            programs[a], programs[b] = programs[b], programs[a]
    return programs

print(''.join(dance(list(ascii_lowercase[:16]), data)))

seen = [ascii_lowercase[:16]]
programs = list(ascii_lowercase[:16])
#for i in range(1_000_000_000):
for i in range(1_000_000_000 % 60):
    programs = dance(programs, data)
    joined = ''.join(programs)
    if joined in seen:
        print(i, seen.index(joined))
        if seen.count(joined) == 4:
            break
    seen.append(joined)
print(joined)
