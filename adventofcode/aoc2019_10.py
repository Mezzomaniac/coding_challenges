map = '''.#......#...#.....#..#......#..##..#
..#.......#..........#..##.##.......
##......#.#..#..#..##...#.##.###....
..#........#...........#.......##...
.##.....#.......#........#..#.#.....
.#...#...#.....#.##.......#...#....#
#...#..##....#....#......#..........
....#......#.#.....#..#...#......#..
......###.......#..........#.##.#...
#......#..#.....#..#......#..#..####
.##...##......##..#####.......##....
.....#...#.........#........#....#..
....##.....#...#........#.##..#....#
....#........#.###.#........#...#..#
....#..#.#.##....#.........#.....#.#
##....###....##..#..#........#......
.....#.#.........#.......#....#....#
.###.....#....#.#......#...##.##....
...##...##....##.........#...#......
.....#....##....#..#.#.#...##.#...#.
#...#.#.#.#..##.#...#..#..#..#......
......#...#...#.#.....#.#.....#.####
..........#..................#.#.##.
....#....#....#...#..#....#.....#...
.#####..####........#...............
#....#.#..#..#....##......#...#.....
...####....#..#......#.#...##.....#.
..##....#.###.##.#.##.#.....#......#
....#.####...#......###.....##......
.#.....#....#......#..#..#.#..#.....
..#.......#...#........#.##...#.....
#.....####.#..........#.#.......#...
..##..#..#.....#.#.........#..#.#.##
.........#..........##.#.##.......##
#..#.....#....#....#.#.......####..#
..............#.#...........##.#.#..'''
test1 = '''.#..#
.....
#####
....#
...##'''
test2 = '''.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##'''
test3 = '''.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....#...###..
..#.#.....#....##'''
test4 = '''###
###
###'''
#map = test2


import math
import re
from collections import defaultdict

asteroids = [asteroid.span()[0] for asteroid in re.finditer('#', ''.join(map.splitlines()))]
#print(asteroids)
asteroids = [divmod(asteroid, len(map.splitlines()[0]))[::-1] for asteroid in asteroids]
#print(sorted(asteroids))
#print(len(asteroids))
#print()

def point_diff(a, b):
    return (a[0] - b[0], a[1] - b[1])

#print(max(len({math.atan2(*point_diff(asteroid, other)) for asteroid in asteroids if other != asteroid}) for other in asteroids))


most_seen = 0
for asteroid in asteroids:
    visible = defaultdict(set)
    for other in asteroids:
        if asteroid == other:
            continue
        diff = point_diff(other, asteroid)
        angle = math.atan2(*diff)
        #angle = math.atan2(diff[0], -diff[1])
        #print(asteroid, other, diff, math.degrees(angle))
        visible[angle].add(diff)
    seen = len(visible)
    if seen > most_seen:
        most_seen = seen
        station = asteroid
        station_view = visible

#def normalise_and_rotate(angle):
    #return (angle + math.pi * 1.5) % (math.pi * 2 + 1e-10)
    #return (angle + math.pi * 0) % (math.pi * 2 + 1e-10)

def abs_vector(vector):
    return (abs(vector[0]), abs(vector[1]))

#print({math.degrees(angle): diffs for angle, diffs in station_view.items()})
#print()

station_view = sorted(
    (
        (angle, sorted(diffs, key=abs_vector, reverse=True)) 
    for angle, diffs in station_view.items()), reverse=True)
    #key=lambda item: normalise_and_rotate(item[0]), reverse=True)

print(station)
print([(math.degrees(angle), diffs) for angle, diffs in station_view])
print()

count = 0
found = False
while not found:
    for i, (angle, diffs) in enumerate(station_view):
        #print(i, angle, diffs)
        print(i, math.degrees(angle), diffs)
        if not diffs:
            continue
        *station_view[i], vaporized = diffs
        asteroid = (station[0] + vaporized[0], station[1] + vaporized[1])
        print(vaporized, asteroid)
        count += 1
        if count == 200:
            print(station, vaporized)
            two100 = asteroid#(station[0] + vaporized[0], station[1] + vaporized[1])
            print(two100)
            print(two100[0] * 100 + two100[1])
            found = True
            break