map = '''################################
###################........#####
###################..G..#G..####
####################........####
##..G###############G......#####
###..G###############.....######
#####.######..######....G##..###
#####.........####............##
#########...#####.............##
#########...####..............##
#########E#####.......GE......##
#########............E...G...###
######.###....#####..G........##
#.G#....##...#######.........###
##.#....##GG#########.........##
#....G#....E#########....#....##
#...........#########.......####
#####..G....#########...##....##
#####....G..#########.#.......##
#######...G..#######G.....#...##
######....E...#####............#
######...GG.......E......#...E.#
#######.G...#....#..#...#.....##
#######..........#####..####.###
########.......E################
#######..........###############
########.............###########
#########...#...##....##########
#########.....#.#..E..##########
################.....###########
################.##E.###########
################################'''

testmap1 = '''#######
#E..G.#
#...#.#
#.G.#G#
#######'''

testmap2 = '''#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######'''

testmap3 = '''#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######'''

testmap4 = '''#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######'''

testmap5 = '''#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######'''

testmap6 = '''#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######'''

testmap7 = '''#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########'''

from queue import Queue
import re

DIRECTIONS = ((0, -1), (-1, 0), (1, 0), (0, 1))

class Unit:
    def __init__(self, race, position, attack=3, hp=200):
        self.race = race
        self.position = position
        self.attack = attack if race == 'E' else 3
        self.hp = hp
    
    def __repr__(self):
        return f'Unit({self.race}, {self.position}, {self.hp})'

class Map:
    def __init__(self, map, name='', elf_attack=3):
        self.map = map
        self.name = name
        #self.grid = [list(row) for row in map.splitlines()]
        self.units = self.find_units(elf_attack)
        #self.map = self.map.replace('E', '.').replace('G', '.')
    
    def __repr__(self):
        return f'<Map object "{self.name}">'
    
    def __str__(self):
        return self.map
    
    def __getitem__(self, index):
        return self.map.splitlines()[index[1]][index[0]]
    
    def __setitem__(self, index, value):
        map = [list(row) for row in self.map.splitlines()]
        map[index[1]][index[0]] = value
        self.map = '\n'.join(''.join(row) for row in map)
    
    def __delitem__(self, index):
        map = [list(row) for row in self.map.splitlines()]
        map[index[1]][index[0]] = '.'
        self.map = '\n'.join(''.join(row) for row in map)
    
    def find_units(self, elf_attack):
        units = set()
        for y, row in enumerate(self.map.splitlines()):
            units |= {Unit(match.group(), (match.start(), y), elf_attack) for match in re.finditer('[EG]', row)}
        #print(units)
        return units
    
    def adjacent(self, position):
        return [(position[0] + direction[0], position[1] + direction[1]) for direction in DIRECTIONS]
    
    def play(self, safe_elves=False):
        #print(self)
        round = 0
        while True:
            #print(f'\nRound {round}')
            for unit in sorted((unit for unit in self.units.copy()), key=lambda u: u.position[::-1]):
                if unit.hp <= 0:
                    continue
                #print(f"{unit}'s turn")
                targets = {other for other in self.units if other.race != unit.race}
                if not targets:
                    print(self)
                    print(f'Game over on round {round} with {sum(unit.hp for unit in self.units)} total hp left')
                    #print(f'Units: {sorted(self.units, key=lambda u: u.position[::-1])}')
                    return round * sum(unit.hp for unit in self.units)
                try:
                    self.attack(unit, safe_elves)
                    continue
                except IndexError:
                    pass
                in_range = {square for target in targets for square in self.adjacent(target.position) if self[square] == '.'}
                moved = self.move(unit, in_range)
                try:
                    self.attack(unit, safe_elves)
                except IndexError:
                    pass
                #if moved:
                    #print(self)
            round += 1

    def attack(self, unit, safe_elves=False):
        targets = sorted({other for other in self.units if other.race != unit.race and other.position in self.adjacent(unit.position)}, key=lambda o: o.position[::-1])
        attacked = sorted(targets, key=lambda t: t.hp)[0]
        attacked.hp -= unit.attack
        #print(f'Attacked {attacked}')
        if attacked.hp <= 0:
            #print(f'{attacked} was killed!')
            del self[attacked.position]
            self.units.remove(attacked)
            if attacked.race == 'E' and safe_elves:
                raise RuntimeWarning(f'Dead Elf (Elf attack={attacked.attack})')
    
    def move(self, unit, in_range):
        start = unit.position
        #if start == (23,5):
            #print(self)
            #print(f'in_range={sorted(in_range, key=lambda x: x[::-1])}')
            #print(f'len(in_range)={len(in_range)}')
        frontier = Queue()
        frontier.put(start)
        came_from = {}
        came_from[start] = None
        
        while not frontier.empty():
            #if start == (23,5):
                #print(f'frontier={frontier.queue}')
                #print(f'came_from={came_from}')
            current = frontier.get()
            #if start == (23,5):
                #print(f'current={current}')
            if current in in_range:
                path = []
                while current != start:
                    path.append(current)
                    current = came_from[current]
                #if start == (23,5):
                    #print(f'path={path}')
                step = path[-1]
                del self[unit.position]
                self[step] = unit.race
                unit.position = step
                #print(f'Moved to {unit.position}')
                return True
            for next in self.adjacent(current):
                #if start == (23,5):
                    #print(f'next={next}, {self[next]}')
                if next not in came_from and self[next] == '.':
                    frontier.put(next)
                    came_from[next] = current
        return False

test1 = Map(testmap1, 'Test Map 1')
#print(test1.play())

test2 = Map(testmap2, 'Test Map 2')
#print(test2.play())

test3 = Map(testmap3, 'Test Map 3')
#print(test3.play())

test4 = Map(testmap4, 'Test Map 4')
#print(test4.play())

test5 = Map(testmap5, 'Test Map 5')
#print(test5.play())

test6 = Map(testmap6, 'Test Map 6')
#print(test6.play())

test7 = Map(testmap7, 'Test Map 7')
#print(test7.play())

print(Map(map, 'AoC2018-15.1').play())  #<203116, <205689, >186000  # WHY DO I NEED TO ADD AN EXTRA ROUND TO GET THE RIGHT ANSWER (189000)???

elf_attack = 0
while True:
    print(elf_attack)
    try:
        print(Map(map, 'AoC2018-15.2', elf_attack).play(True))
        break
    except RuntimeWarning:
        elf_attack += 1
