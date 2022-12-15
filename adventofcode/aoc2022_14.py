from downloader import download

download(2022, 14)
with open('aoc2022_14input.txt') as inputfile:
    data = inputfile.read()

test = '''498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9'''
#data = test
print(data)

rocks = set()
for line in data.splitlines():
    positions = line.split(' -> ')
    start_x, start_y = tuple(int(coord) for coord in positions[0].split(','))
    for end_pos in positions[1:]:
        end_x, end_y = tuple(int(coord) for coord in end_pos.split(','))
        sorted_xs = sorted((start_x, end_x))
        sorted_ys = sorted((start_y, end_y))
        rocks |= {(x, y) for x in range(sorted_xs[0], sorted_xs[1] + 1) for y in range(sorted_ys[0], sorted_ys[1] + 1)}
        start_x, start_y = end_x, end_y
nadir = max(rock[1] for rock in rocks)

abyss_reached = False
sand = set()
while not abyss_reached:
    current_pos = (500, 0)
    settled = False
    while not settled:
        for movement in [(0, 1), (-1, 1), (1, 1)]:
            next_pos = (current_pos[0] + movement[0], current_pos[1] + movement[1])
            if next_pos[1] > nadir:
                settled = True
                abyss_reached = True
                break
            if next_pos not in rocks | sand:
                current_pos = next_pos
                break
        else:
            settled = True
            sand.add(current_pos)
print(len(sand))

rocks |= {(x, nadir + 2) for x in range(min(rock[0] for rock in rocks) - 500, max(rock[0] for rock in rocks) + 500)}
source_reached = False
sand = set()
left_most_sand = right_most_sand = 500
highest_sand = nadir
heights = 0
while not source_reached:
    current_pos = (500, 0)
    settled = False
    while not settled:
        for movement in [(0, 1), (-1, 1), (1, 1)]:
            next_pos = (current_pos[0] + movement[0], current_pos[1] + movement[1])
            #if next_pos not in rocks | sand:
            # Wow set union is really slow!
            if next_pos not in rocks and next_pos not in sand:
                current_pos = next_pos
                break
        else:
            settled = True
            sand.add(current_pos)
            if current_pos == (500, 0):
                source_reached = True
    updated = False
    if current_pos[0] < left_most_sand:
        left_most_sand = current_pos[0]
        updated = True
    if current_pos[0] > right_most_sand:
        right_most_sand = current_pos[0]
        updated = True
    if current_pos[1] < highest_sand:
        highest_sand = current_pos[1]
        updated = True
    if len(set(pos[1] for pos in sand)) > heights:
        heights = len(set(pos[1] for pos in sand))
        updated = True
    if updated:
        print(len(sand), left_most_sand, right_most_sand, highest_sand, heights)
print(len(sand))
