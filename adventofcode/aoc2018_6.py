data = '''154, 159
172, 84
235, 204
181, 122
161, 337
305, 104
128, 298
176, 328
146, 71
210, 87
341, 195
50, 96
225, 151
86, 171
239, 68
79, 50
191, 284
200, 122
282, 240
224, 282
327, 74
158, 289
331, 244
154, 327
317, 110
272, 179
173, 175
187, 104
44, 194
202, 332
249, 197
244, 225
52, 127
299, 198
123, 198
349, 75
233, 72
284, 130
119, 150
172, 355
147, 314
58, 335
341, 348
236, 115
185, 270
173, 145
46, 288
214, 127
158, 293
237, 311'''

test = '''1, 1
1, 6
8, 3
3, 4
5, 5
8, 9'''

from collections import defaultdict

coords = {tuple(int(x) for x in line.split(', ')) for line in data.splitlines()}
#coords = {tuple(int(x) for x in line.split(', ')) for line in test.splitlines()}
min_x = min(coord[0] for coord in coords)
max_x = max(coord[0] for coord in coords)
min_y = min(coord[1] for coord in coords)
max_y = max(coord[1] for coord in coords)

areas = defaultdict(int)
num_safe_locations = 0
for x1, y1 in ((x, y) for x in range(min_x - 1, max_x + 2) for y in range(min_y - 1, max_y + 2)):
    distances = {}
    total_distance = 0
    for x2, y2 in coords:
        distance = abs(x2 - x1) + abs(y2 - y1)
        distances[(x2, y2)] = distance
        total_distance += distance
    nearest_coords = sorted(distances, key=distances.__getitem__)
    if distances[nearest_coords[1]] != distances[nearest_coords[0]]:
        areas[nearest_coords[0]] += 1
    if total_distance < 10000:
        num_safe_locations += 1

#print(areas)

expanded_areas = defaultdict(int)
for x1, y1 in {(x, y) for x in range(min_x - 2, max_x + 3, max_x - min_x + 4) for y in range(min_y - 2, max_y + 3)} | {(x, y) for x in range(min_x - 2, max_x + 3) for y in range(min_y - 2, max_y + 3, max_y - min_y + 4)}:
    #print(x1, y1)
    distances = {}
    for x2, y2 in coords:
        distance = abs(x2 - x1) + abs(y2 - y1)
        distances[(x2, y2)] = distance
    nearest_coords = sorted(distances, key=distances.__getitem__)
    if distances[nearest_coords[1]] != distances[nearest_coords[0]]:
        expanded_areas[nearest_coords[0]] += 1

#print(expanded_areas)

for coord in expanded_areas:
    del areas[coord]

#print(areas)
#print(sum(areas.values()))

largest_area = max(areas.values())
print(largest_area)

print(num_safe_locations)
