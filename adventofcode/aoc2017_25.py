from downloader import download

download(2017, 25)
with open('aoc2017_25input.txt') as inputfile:
    data = inputfile.read()
print(data)

blueprint = []
for i, state in enumerate(data.split('\n\n')[1:]):
    lines = state.splitlines()
    rules = []
    for base in (2, 6):
        write = int(lines[base][-2])
        move = (-1, 1)['r' in lines[base + 1]]
        next_state = 'ABCDEF'.index(lines[base + 2][-2])
        rules.append((write, move, next_state))
    blueprint.append(rules)

tape = set()
cursor = 0
state = 0
for step in range(12317297):
    rules = blueprint[state][cursor in tape]
    if rules[0]:
        tape.add(cursor)
    else:
        tape.discard(cursor)
    cursor += rules[1]
    state = rules[2]
print(len(tape))
