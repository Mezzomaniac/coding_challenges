initial = '''#####
.#.##
#...#
..###
#.##.'''

from pprint import pprint

def point_add_2d(a, b):
    return (a[0] + b[0], a[1] + b[1])

def neighbors1(position):
    return {point_add_2d(position, direction) for direction in ((1, 0), (0, -1), (-1, 0), (0, 1))}

def life(space, adjacent_bugs):
    if space == '#' and adjacent_bugs == 1:
        new_space = '#'
    elif space == '.' and adjacent_bugs in range(1, 3):
        new_space = '#'
    else:
        new_space = '.'
    return new_space

rows = initial.splitlines()
initial_layout = {}
for y, row in enumerate(rows):
    for x, space in enumerate(row):
        initial_layout[(y, x)] = space
layout = initial_layout
layouts = []
while layout not in layouts:
    layouts.append(layout)
    new_layout = {}
    for position, space in layout.items():
        adjacent_bugs = sum(layout.get(neighbor, '.') == '#' for neighbor in neighbors1(position))
        new_layout[position] = life(space, adjacent_bugs)
    layout = new_layout
print(sum(2 ** (y * 5 + x) for (y, x), space in layout.items() if space == '#'))

def point_add_3d(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])

def neighbors2(position):
    y, x, layer = position
    results = set()
    for direction in ((1, 0, 0), (0, -1, 0), (-1, 0, 0), (0, 1, 0)):
        result = point_add_3d(position, direction)
        if result == (2, 2, layer):
            if not direction[1]:
                results |= {(y - direction[0], x, layer + 1) for x in range(5)}
            else:
                results |= {(y, x - direction[1], layer + 1) for y in range(5)}
        elif set(result[:2]) & {-1, 5}:
            if not direction[1]:
                results.add((2 + direction[0], 2, layer - 1))
            else:
                results.add((2, 2 + direction[1], layer - 1))
        else:
            results.add(result)
    return results

def extreme_layers(all_layers):
    minimum = min(layer for y, x, layer in all_layers.keys())
    maximum = max(layer for y, x, layer in all_layers.keys())
    return minimum, maximum

layers = {key + (0,):  value for key, value in initial_layout.items() if key != (2, 2)}
#pprint(layers)
#print(len(layers))
#print()
for minute in range(200):
    new_layers = {}
    min_layer, max_layer = extreme_layers(layers)
    for layer in range(min_layer - 1, max_layer + 2):
        for y in range(5):
            for x in range(5):
                if (y, x) == (2, 2):
                    continue
                position = (y, x, layer)
                space = layers.get(position, '.')
                neighbors = neighbors2(position)
                adjacent_bugs = sum(layers.get(neighbor, '.') == '#' for neighbor in neighbors)
                new_space = life(space, adjacent_bugs)
                #print(position, space, adjacent_bugs, new_space)
                #pprint(neighbors)
                #print()
                new_layers[position] = new_space
    layers = new_layers
    #pprint(layers)
    #print(len(layers))
    #break
print(sum(space == '#' for space in layers.values()))