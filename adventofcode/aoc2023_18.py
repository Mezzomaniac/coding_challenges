from downloader import download

download(2023, 18)
with open('aoc2023_18input.txt') as inputfile:
    data = inputfile.read()
test_data = '''R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)'''
test_data2 = '''U 4 _
R 4 _
D 4 _
L 4 _'''
test_data3 = '''R 1 _
U 1 _
R 1 _
D 1 _
R 1 _
D 1 _
L 1 _
D 1 _
L 1 _
U 1 _
L 1 _
U 1 _'''
test_data4 = '''R 2 _
U 1 _
L 1 _
U 1 _
L 1 _
D 2 _'''
test_data5 = '''R 3 _
U 2 _
L 1 _
U 1 _
L 2 _
D 3 _'''
#data = test_data
print(data)

def calculate_area(instructions: list[str, int]):
    # https://en.wikipedia.org/wiki/Pick's_theorem?wprov=sfti1#Formula
    
    area = 0
    perimeter = 0
    current_x, current_y = 0, 0
    for direction, distance in instructions:
        next_x, next_y = current_x, current_y
        if direction == 'U':
            next_y += distance
        elif direction == 'D':
            next_y -= distance
        elif direction == 'L':
            next_x -= distance
        elif direction == 'R':
            next_x += distance
        area += (current_y + next_y) * (current_x - next_x)
        perimeter += distance
        current_x, current_y = next_x, next_y
    area //= 2
    print(abs(area), perimeter)
    return abs(area) + perimeter // 2 + 1

instructions = []
for line in data.splitlines():
    direction, distance = line.split()[:2]
    instructions.append((direction, int(distance)))
print(calculate_area(instructions))

instructions = []
for line in data.splitlines():
    hexcode = line.split()[-1][2:-1]
    distance = int(hexcode[:-1], 16)
    direction = 'RDLU'[int(hexcode[-1])]
    instructions.append((direction, distance))
print(calculate_area(instructions))
