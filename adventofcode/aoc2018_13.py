with open('aoc2018-13.txt') as file:
    paths = file.read()

from itertools import count, cycle
import re

DIRECTIONS = ((0, -1), (0, 1), (-1, 0), (1, 0))

class Paths:
    def __init__(self, paths):
        self.paths = paths
        self.rows = self.paths.splitlines()
        self.carts = self.find_carts()
        self.reveal_tracks()
    
    def find_carts(self):
        carts = set()
        for y, row in enumerate(self.rows):
            carts |= {Cart(match.group(), (match.start(), y)) for match in re.finditer(r'[v^<>]', row)}
        #print(carts)
        return carts

    def reveal_tracks(self):
        for cart in self.carts:
            hidden = self.reveal_track(cart.position)
            self.rows[cart.position[1]] = ''.join((self.rows[cart.position[1]][:cart.position[0]], hidden, self.rows[cart.position[1]][cart.position[0]+1:]))
        self.paths = ''.join(self.rows)

    def reveal_track(self, position):
        orthogonals = self.get_orthogonals(position)
        vert = r'|\\/+'
        horiz = r'-\\/+'
        if re.match(rf'[{vert}]{{2}}[{horiz}]{{2}}', orthogonals):
            hidden = '+'
        elif re.match(rf'[{vert}]{{2}}[^{horiz}]{{2}}', orthogonals):
            hidden = '|'
        elif re.match(rf'[^{vert}]{{2}}[{horiz}]{{2}}', orthogonals):
            hidden = '-'
        elif re.match(rf'([{vert}][^{vert}][{horiz}][^{horiz}])|([^{vert}][{vert}][^{horiz}][{horiz}])', orthogonals):
            hidden = '/'
        elif re.match(rf'([{vert}][^{vert}][^{horiz}][{horiz}])|([^{vert}][{vert}][{horiz}][^{horiz}])', orthogonals):
            hidden = r'\\'
        else:
            raise ValueError(f'No valid hidden result. orthogonals={orthogonals}')
        return hidden

    def get_orthogonals(self, position):
        coords = ((position[0] + direction[0], position[1] + direction[1]) for direction in DIRECTIONS)
        return ''.join(self.rows[y][x] for x, y in coords)

    def run(self):
        ticks = 0
        while True:
            ticks += 1
            print(ticks)
            for cart in sorted((cart for cart in self.carts if not cart.crashed), key=lambda c: c.position[::-1]):
                #if cart.id in (6, 8):
                    #print(cart)
                    #print(self.rows[cart.position[1]][cart.position[0]])
                position, crash = self.step(cart)
                #if cart.id in (6, 8):
                    #print(cart)
                    #print(self.rows[cart.position[1]][cart.position[0]])
                    #print()
                #if crash:
                    #print(position)
                    #return
            if len([cart for cart in self.carts if not cart.crashed]) == 1:
                print({cart for cart in self.carts if not cart.crashed}.pop().position)
                return
    
    def step(self, cart):
        cart.move()
        new_path = self.rows[cart.position[1]][cart.position[0]]
        corners_dict = {r'\^': '<', r'\>': 'v', r'\<': '^', r'\v': '>', r'/^': '>', r'/<': 'v', r'/>': '^', r'/v': '<'}
        intersections_dict = {'^': '<^>', '>': '^>v', 'v': '>v<', '<': 'v<^'}
        crash = False
        if cart.position in (other.position for other in self.carts if other is not cart and not other.crashed):
            crash_position = cart.position
            for cart in (cart for cart in self.carts if not cart.crashed):
                cart.crashed = cart.position == crash_position
            print(sorted(self.carts, key=lambda c: c.id))
            #cart.direction = 'X'
            crash = True
        elif new_path + cart.direction in corners_dict:
            cart.direction = corners_dict[new_path + cart.direction]
        elif new_path == '+':
            cart.direction = intersections_dict[cart.direction][next(cart.next_turn)]
        return (cart.position, crash)

class Cart:
    UP = '^'
    DOWN = 'v'
    LEFT = '<'
    RIGHT = '>'
    DIRECTIONS_DICT = dict(zip((UP, DOWN, LEFT, RIGHT), DIRECTIONS))
    ids = count()
    
    def __init__(self, direction, position):
        self.direction = direction
        self.position = position
        self.id = next(Cart.ids)
        self.next_turn = cycle(range(3))
        self.crashed = False
    
    def __repr__(self):
        return f'Cart({self.direction}, {self.position}, {self.id}, {self.crashed})'
    
    def move(self):
        vector = Cart.DIRECTIONS_DICT[self.direction]
        self.position = (self.position[0] + vector[0], self.position[1] + vector[1])

Paths(paths).run()
