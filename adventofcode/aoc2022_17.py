from downloader import download
from collections import deque
from itertools import cycle

download(2022, 17)
with open('aoc2022_17input.txt') as inputfile:
    data = inputfile.read()
test = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'
#data = test
print(data)

class Space:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)
    
    def __repr__(self):
        return f'Space({self.x}, {self.y})'
        
    def __add__(self, other):
        return Space(self.x + other.x, self.y + other.y)

class Rock:
    
    def __init__(self):
        self.spaces = set()
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.spaces})'
    
    @property
    def left_edge(self):
        return min(space.x for space in self.spaces)

    @property
    def right_edge(self):
        return max(space.x for space in self.spaces)

    @property
    def bottom_edge(self):
        return min(space.y for space in self.spaces)

    @property
    def top_edge(self):
        return max(space.y for space in self.spaces)
    
    def move_left(self):
        if self.left_edge == 0:
            return
        spaces = {space + Space(-1, 0) for space in self.spaces}
        if spaces.isdisjoint(settled):
            self.spaces = spaces
    
    def move_right(self):
        if self.right_edge == 6:
            return 
        spaces = {space + Space(1, 0) for space in self.spaces}
        if spaces.isdisjoint(settled):
            self.spaces = spaces
    
    def move_down(self):
        if self.bottom_edge == 1:
            return 
        spaces = {space + Space(0, -1) for space in self.spaces}
        if spaces.isdisjoint(settled):
            self.spaces = spaces
            return True

class HorizontalLine(Rock):
    
    def __init__(self, height):
        self.spaces = {Space(x, height) for x in range(2, 6)}

class Plus(Rock):
    
    def __init__(self, height):
        self.spaces = {Space(3, height), *(Space(x, height + 1) for x in range(2, 5)), Space(3, height + 2)}

class ReverseL(Rock):
    
    def __init__(self, height):
        self.spaces = {*(Space(x, height) for x in range(2, 5)), Space(4, height + 1), Space(4, height + 2)}

class VerticalLine(Rock):
    
    def __init__(self, height):
        self.spaces = {Space(2, height + x) for x in range(4)}

class Square(Rock):
    
    def __init__(self, height):
        self.spaces = {Space(2, height), Space(3, height), Space(2, height + 1), Space(3, height + 1)}

rocks = cycle([HorizontalLine, Plus, ReverseL, VerticalLine, Square])
jets = cycle(data.strip())

limit = 2022
limit = 1000000000000

settled = set()
rock_count = 0
active_rock = None
heights = [0]
recent_height_changes = deque(maxlen=5)
min_seq_length = 6
min_seq_length = 20
recent_round_height_changes = deque(maxlen=min_seq_length)
round_height_sequences = {}
while rock_count < limit:
    if not active_rock:
        height = max((space.y for space in settled), default=0)
        recent_height_changes.append(height - heights[-1])
        if rock_count and not rock_count % 5:
            round_height_change = height - heights[-5]
            recent_round_height_changes.append(round_height_change)
            print(rock_count, recent_height_changes, round_height_change)
            if rock_count > min_seq_length:
                round_height_sequence = tuple(recent_round_height_changes)
                if round_height_sequence in round_height_sequences:
                    first_repeated_seq_point = round_height_sequences[round_height_sequence]
                    seq_start = first_repeated_seq_point - ((min_seq_length - 1) * 5)
                    period = rock_count - first_repeated_seq_point
                    initial_height = heights[seq_start - 5]
                    print(round_height_sequence)
                    print(seq_start, rock_count - seq_start)
                    break
                round_height_sequences[round_height_sequence] = rock_count
        if height:
            heights.append(height)
        active_rock = next(rocks)(height + 4)
    jet = next(jets)
    if jet == '<':
        active_rock.move_left()
    else:
        active_rock.move_right()
    down = active_rock.move_down()
    if not down:
        settled |= active_rock.spaces
        rock_count += 1
        #print(rock_count, active_rock.__class__.__name__)
        active_rock = None
print(max(space.y for space in settled))

repeats, extras = divmod(limit - (seq_start - 5), period)
final_height = initial_height + repeats * (heights[seq_start + period - 5] - initial_height)
#print(final_height)
if extras:
    final_height += heights[seq_start + extras - 5] - initial_height
    
print(final_height)
