data = '''L3, R1, L4, L1, L2, R4, L3, L3, R2, R3, L5, R1, R3, L4, L1, L2, R2, R1, L4, L4, R2, L5, R3, R2, R1, L1, L2, R2, R2, L1, L1, R2, R1, L3, L5, R4, L3, R3, R3, L5, L190, L4, R4, R51, L4, R5, R5, R2, L1, L3, R1, R4, L3, R1, R3, L5, L4, R2, R5, R2, L1, L5, L1, L1, R78, L3, R2, L3, R5, L2, R2, R4, L1, L4, R1, R185, R3, L4, L1, L1, L3, R4, L4, L1, R5, L5, L1, R5, L1, R2, L5, L2, R4, R3, L2, R3, R1, L3, L5, L4, R3, L2, L4, L5, L4, R1, L1, R5, L2, R4, R2, R3, L1, L1, L4, L3, R4, L3, L5, R2, L5, L1, L1, R2, R3, L5, L3, L2, L1, L4, R4, R4, L2, R3, R1, L2, R1, L2, L2, R3, R3, L1, R4, L5, L3, R4, R4, R1, L2, L5, L3, R1, R4, L2, R5, R4, R2, L5, L3, R4, R1, L1, R5, L3, R1, R5, L2, R1, L5, L2, R2, L2, L3, R3, R3, R1'''

data = data.split(', ')
position = (0, 0)
directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
direction = 0

def coordadd(coord1, coord2):
    return (coord1[0] + coord2[0], coord1[1] + coord2[1])

def coordmul(coord, steps):
    return (coord[0] * steps, coord[1] * steps)

visited = {position}
done = False
for instruction in data:
    if done:
        break
    turn, steps = instruction[0], instruction[1:]
    steps = int(steps)
    direction += 1 if turn == 'R' else -1
    direction %= 4
    #position = coordadd(position, coordmul(directions[direction], steps))
    for i in range(steps):
        position = coordadd(position, directions[direction])
        if position in visited:
            done = True
            break
        visited.add(position)

print(abs(position[0]) + abs(position[1]))
