data = '''rect 1x1
rotate row y=0 by 5
rect 1x1
rotate row y=0 by 5
rect 1x1
rotate row y=0 by 5
rect 1x1
rotate row y=0 by 5
rect 1x1
rotate row y=0 by 2
rect 1x1
rotate row y=0 by 2
rect 1x1
rotate row y=0 by 3
rect 1x1
rotate row y=0 by 3
rect 2x1
rotate row y=0 by 2
rect 1x1
rotate row y=0 by 3
rect 2x1
rotate row y=0 by 2
rect 1x1
rotate row y=0 by 3
rect 2x1
rotate row y=0 by 5
rect 4x1
rotate row y=0 by 5
rotate column x=0 by 1
rect 4x1
rotate row y=0 by 10
rotate column x=5 by 2
rotate column x=0 by 1
rect 9x1
rotate row y=2 by 5
rotate row y=0 by 5
rotate column x=0 by 1
rect 4x1
rotate row y=2 by 5
rotate row y=0 by 5
rotate column x=0 by 1
rect 4x1
rotate column x=40 by 1
rotate column x=27 by 1
rotate column x=22 by 1
rotate column x=17 by 1
rotate column x=12 by 1
rotate column x=7 by 1
rotate column x=2 by 1
rotate row y=2 by 5
rotate row y=1 by 3
rotate row y=0 by 5
rect 1x3
rotate row y=2 by 10
rotate row y=1 by 7
rotate row y=0 by 2
rotate column x=3 by 2
rotate column x=2 by 1
rotate column x=0 by 1
rect 4x1
rotate row y=2 by 5
rotate row y=1 by 3
rotate row y=0 by 3
rect 1x3
rotate column x=45 by 1
rotate row y=2 by 7
rotate row y=1 by 10
rotate row y=0 by 2
rotate column x=3 by 1
rotate column x=2 by 2
rotate column x=0 by 1
rect 4x1
rotate row y=2 by 13
rotate row y=0 by 5
rotate column x=3 by 1
rotate column x=0 by 1
rect 4x1
rotate row y=3 by 10
rotate row y=2 by 10
rotate row y=0 by 5
rotate column x=3 by 1
rotate column x=2 by 1
rotate column x=0 by 1
rect 4x1
rotate row y=3 by 8
rotate row y=0 by 5
rotate column x=3 by 1
rotate column x=2 by 1
rotate column x=0 by 1
rect 4x1
rotate row y=3 by 17
rotate row y=2 by 20
rotate row y=0 by 15
rotate column x=13 by 1
rotate column x=12 by 3
rotate column x=10 by 1
rotate column x=8 by 1
rotate column x=7 by 2
rotate column x=6 by 1
rotate column x=5 by 1
rotate column x=3 by 1
rotate column x=2 by 2
rotate column x=0 by 1
rect 14x1
rotate row y=1 by 47
rotate column x=9 by 1
rotate column x=4 by 1
rotate row y=3 by 3
rotate row y=2 by 10
rotate row y=1 by 8
rotate row y=0 by 5
rotate column x=2 by 2
rotate column x=0 by 2
rect 3x2
rotate row y=3 by 12
rotate row y=2 by 10
rotate row y=0 by 10
rotate column x=8 by 1
rotate column x=7 by 3
rotate column x=5 by 1
rotate column x=3 by 1
rotate column x=2 by 1
rotate column x=1 by 1
rotate column x=0 by 1
rect 9x1
rotate row y=0 by 20
rotate column x=46 by 1
rotate row y=4 by 17
rotate row y=3 by 10
rotate row y=2 by 10
rotate row y=1 by 5
rotate column x=8 by 1
rotate column x=7 by 1
rotate column x=6 by 1
rotate column x=5 by 1
rotate column x=3 by 1
rotate column x=2 by 2
rotate column x=1 by 1
rotate column x=0 by 1
rect 9x1
rotate column x=32 by 4
rotate row y=4 by 33
rotate row y=3 by 5
rotate row y=2 by 15
rotate row y=0 by 15
rotate column x=13 by 1
rotate column x=12 by 3
rotate column x=10 by 1
rotate column x=8 by 1
rotate column x=7 by 2
rotate column x=6 by 1
rotate column x=5 by 1
rotate column x=3 by 1
rotate column x=2 by 1
rotate column x=1 by 1
rotate column x=0 by 1
rect 14x1
rotate column x=39 by 3
rotate column x=35 by 4
rotate column x=20 by 4
rotate column x=19 by 3
rotate column x=10 by 4
rotate column x=9 by 3
rotate column x=8 by 3
rotate column x=5 by 4
rotate column x=4 by 3
rotate row y=5 by 5
rotate row y=4 by 5
rotate row y=3 by 33
rotate row y=1 by 30
rotate column x=48 by 1
rotate column x=47 by 5
rotate column x=46 by 5
rotate column x=45 by 1
rotate column x=43 by 1
rotate column x=38 by 3
rotate column x=37 by 3
rotate column x=36 by 5
rotate column x=35 by 1
rotate column x=33 by 1
rotate column x=32 by 5
rotate column x=31 by 5
rotate column x=30 by 1
rotate column x=23 by 4
rotate column x=22 by 3
rotate column x=21 by 3
rotate column x=20 by 1
rotate column x=12 by 2
rotate column x=11 by 2
rotate column x=3 by 5
rotate column x=2 by 5
rotate column x=1 by 3
rotate column x=0 by 4'''

tests = '''rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1'''

import numpy as np

def parse(instruction):
    global screen
    if instruction.startswith('rect'):
        a, b = instruction.split()[1].split('x')
        a, b = int(a), int(b)
        screen[:b, :a] = 1
    else:
        a, b = instruction[instruction.index('=') + 1:].split(' by ')
        a, b = int(a), int(b)
        if 'row' in instruction:
            screen[a, :] = np.roll(screen[a, :], b)
        else:
            screen[:, a] = np.roll(screen[:, a], b)

screen = np.zeros((6, 50), dtype=int)
#screen = np.zeros((3, 7), dtype=int)

instructions = data.splitlines()
#instructions = tests.splitlines()
for instruction in instructions:
    #print(instruction)
    parse(instruction)
    #print(screen)

#print(screen)
print(np.sum(screen))
for row in screen:
    #print(np.sum(row))
    print(''.join('#' if e else ' ' for e in row))
