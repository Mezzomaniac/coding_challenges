from downloader import download

download(2023, 12)
with open('aoc2023_12input.txt') as inputfile:
    data = inputfile.read()
    
test_data = '''???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1'''
#data = test_data
#print(data)

from copy import deepcopy
import functools
import itertools


class LogicError(Exception):
    pass


class ClueGroup:
    '''Adapted from pixel_puzzle4.py'''
    
    def __init__(self, clues, length):
        self.clues = [Clue(clue, num) for num, clue in enumerate(clues)]
        self.length = length
        self._boxes = set()
        self.blocks = []
        self._crosses = set()
        self._unknowns = set(range(length))
        #self.solved = False
        self.setup()
    
    def __repr__(self):
        return f'ClueGroup({self.clues!r}, {self.length!r})'
    
    
    @property
    def boxes(self):
        return self._boxes.copy()
    
    @boxes.setter
    def boxes(self, value):
        value = self.in_bounds(value)
        if value <= self.boxes:
            return
        error = value & self.crosses
        if error:
            raise LogicError(f'{self!r} wants to change {error} from cross(es) to box(es).')
        self._boxes = value
        self.unknowns -= value
        # Found all boxes:
        if self.unknowns and (len(self._boxes) == sum(self.clues)):
            self.crosses |= self.unknowns
            return
        # Update blocks:
        self.identify_blocks()
    
    @property
    def crosses(self):
        return self._crosses.copy()
    
    @crosses.setter
    def crosses(self, value):
        value = self.in_bounds(value)
        if value <= self.crosses:
            return
        error = value & self.boxes
        if error:
            raise LogicError(f'{self!r} wants to change {error} from box(es) to cross(es).')
        self._crosses = value
        self.unknowns -= value
        # Found all crosses:
        if self.unknowns and (len(self._crosses) == self.length - sum(self.clues)):
            self.boxes |= self.unknowns
            return
        # Update clue possibilities:
        for clue in self.clues:
            clue.eliminate_possibilities(value)

    @property
    def unknowns(self):
        return self._unknowns.copy()
    
    @unknowns.setter
    def unknowns(self, value):
        value = self.in_bounds(value)
        self._unknowns = value
        # Solved:
        #if not self._unknowns:
            #self.solved = True
            #for clue in self.clues:
                #clue.solved = True

    def __len__(self):
        return len(self.clues)
    
    def __getitem__(self, key):
        return self.clues[key]
    
    def __iter__(self):
        return iter(self.clues)

    def __reversed__(self):
        return reversed(self.clues)

    def __contains__(self, item):
        return item in self.clues

    def in_bounds(self, value):
        return value & frozenset(range(self.length))

    def setup(self):
        # Setup context awareness:
        set_contextual_attrs(self)
        for clue in self:
            clue.clue_group = self

            # Initialize possibilities:
            start = area(self[:clue.num + 1]) - clue
            stop = self.length - area(self[clue.num:]) + 1
            clue._possible = {frozenset(range(x, x + clue)) for x in range(start, stop)}

    def identify_blocks(self):
        new_blocks = []
        current_block = set()
        for cell in range(self.length):
            if cell in self.boxes:
                current_block.add(cell)
            elif current_block:
                new_blocks.append(current_block)
                current_block = set()
        if current_block:
            new_blocks.append(current_block)
        modified_blocks = []
        for new_block in new_blocks:
            matching_existing_blocks = list(itertools.takewhile(new_block.intersection, itertools.dropwhile(new_block.isdisjoint, self.blocks)))
            if matching_existing_blocks:
                new_block = Block.merge(matching_existing_blocks, new_block)
            else:
                new_block = Block(new_block, set(self.clues))
            new_block.clue_group = self
            modified_blocks.append(new_block)
        self.blocks = modified_blocks
        set_contextual_attrs(self.blocks)


class Clue:
    '''From pixel_puzzle4.py'''
    
    def __init__(self, clue, num):
        self.clue = clue
        self.num = num
        self.solved = False
        self._found = set()
        self._possible = set()
    
    def __repr__(self):
        return f'Clue({self.clue!r}, {self.num!r})'
    
    @property
    def found(self):
        return self._found.copy()
        
    @found.setter
    def found(self, value):
        if value <= self.found:
            return
        if self.solved:
            raise LogicError(f'{self} is solved with {self.found} but is trying to add {value} as found.')
        self._found = value
        self.refine_possibilities(value)
    
    @property
    def possible(self):
        return self._possible.copy()
    
    @possible.setter
    def possible(self, value):
        '''Modify the set of frozensets of possible cells for the clue to occupy.
        
        Note also the Clue.refine_possibilities(found) and Clue.eliminate_possibilities(crosses) methods,
        which remove possibilities based on identified boxes/crosses.'''
        
        self._possible = value
        if not self.possible:
            raise LogicError(f'{self!r} in {self.clue_group!r} has no possibilities.')
        self.last_possibility()
    
    def __lt__(self, other):
        return self.clue < other
    
    def __le__(self, other):
        return self.clue <= other

    def __gt__(self, other):
        return self.clue > other

    def __ge__(self, other):
        return self.clue >= other
    
    def __add__(self, other):
        try:
            return self.clue + other.clue
        except AttributeError:
            return self.clue + other

    def __sub__(self, other):
        try:
            return self.clue - other.clue
        except AttributeError:
            return self.clue - other

    def __mul__(self, other):
        return self.clue * other

    def __radd__(self, other):
        try:
            return other.clue + self.clue
        except AttributeError:
            return other + self.clue

    def __rsub__(self, other):
        try:
            return other.clue - self.clue
        except AttributeError:
            return other - self.clue

    def __rmul__(self, other):
        return other * self.clue
    
    def sorted_possible(self):
        return sorted(sorted(possibility) for possibility in self.possible)

    def refine_possibilities(self, found):
        if self.solved:
            return
        rejected = {possibility for possibility in self.possible if not found <= possibility}
        if rejected:
            self.possible -= rejected
            if self.previous:
                self.previous.eliminate_possibilities(set(range(min(found) - 1, self.clue_group.length)))
            if self.next:
                self.next.eliminate_possibilities(set(range(max(found) + 2)))
    
    def eliminate_possibilities(self, crosses):
        if self.solved:
            return
        rejected = {possibility for possibility in self.possible if possibility & crosses}
        if rejected:
            self.possible -= rejected
            sorted_possibilities = self.sorted_possible()
            lowest_possible_cells = set(min(sorted_possibilities))
            lowest_possible_cells.add(max(lowest_possible_cells) + 1)
            highest_possible_cells = set(max(sorted_possibilities))
            highest_possible_cells.add(min(highest_possible_cells) - 1)
            if self.previous:
                self.previous.eliminate_possibilities(highest_possible_cells)
            if self.next:
                self.next.eliminate_possibilities(lowest_possible_cells)
    
    def last_possibility(self):
        if len(self.possible) == 1:
            boxes = self.possible.pop()
            caps = get_caps(boxes)
            self.clue_group.boxes |= boxes
            self.clue_group.crosses |= caps
            self.found |= boxes
            self.solved = True

    
class Block:
    '''From pixel_puzzle4.py'''
    
    @classmethod
    def merge(cls, existing_blocks, new_boxes):
        '''Preserve data from existing Block instances even when new boxes change the composition of the blocks.
        
        existing_blocks parameter is a list of existing Block instances to be merged
        
        new_boxes parameter is a set of boxes (integers) that is equal to or a superset of the union of sets of boxes of existing_blocks'''
        
        if len(existing_blocks) == 1:
            existing_blocks[0].boxes = new_boxes
            return existing_blocks[0]
        new_possible_clues = set.intersection(*(block.possible_clues for block in existing_blocks))
        new_assigned = functools.reduce(lambda x,y: x or y, (block.assigned for block in existing_blocks))
        new_completed = any(block.completed for block in existing_blocks)
        return cls(new_boxes, new_possible_clues, new_assigned, new_completed)
    
    def __init__(self, boxes, possible_clues=None, assigned=None, completed=False):
        self.boxes = boxes
        self._possible_clues = possible_clues or set()
        self._assigned = assigned
        self._completed = completed
    
    def __repr__(self):
        return f'Block({self.boxes!r}, {self.possible_clues!r}, {self.assigned!r}, {self.completed!r})'
    
    @property
    def possible_clues(self):
        return self._possible_clues.copy()

    @possible_clues.setter
    def possible_clues(self, value):
        self._possible_clues = value
        if len(self.possible_clues) == 1:
            clue = self.possible_clues.pop()
            self.assigned = clue
        elif not self.possible_clues:
            raise LogicError(f'{self!r} in {self.clue_group!r} has no possible clues.')

    @property
    def assigned(self):
        return self._assigned
    
    @assigned.setter
    def assigned(self, clue):
        self._assigned = clue
        if len(self.possible_clues) != 1:
            self._possible_clues = {clue}
        clue.found |= self.boxes

    @property
    def completed(self):
        if self._completed:
            return True
        completed = len(self.boxes) == self.max_length
        if completed:
            self.completed = True
        return completed
    
    @completed.setter
    def completed(self, value):
        self._completed = value
        if self.completed:
            self.clue_group.crosses |= get_caps(self.boxes)
    
    @property
    def min_length(self):
        if self.assigned:
            return self.assigned.clue
        return min(self.possible_clues).clue

    @property
    def max_length(self):
        if self.assigned:
            return self.assigned.clue
        try:
            return max(self.possible_clues).clue
        except ValueError:
            # Necessary so self.completed can be determined for self.__repr__ when needed for the output of a LogicError
            return

    def __eq__(self, other):
        return (self.boxes, self.min_length, self.max_length, len(self.possible_clues)) == (other.boxes, other.min_length, other.max_length, len(other.possible_clues))
    
    def __hash__(self):
        return hash((frozenset(self.boxes), self.min_length, self.max_length, len(self.possible_clues)))

    def __len__(self):
        return len(self.boxes)
    
    def __iter__(self):
        return iter(self.boxes)

    def __contains__(self, item):
        return item in self.boxes


def area(clues):
    """Calculates the minimum number of cells required for clues plus the gaps between them.
    
    From pixel_puzzle4.py"""
    return sum(clues) + len(clues) - 1

def get_caps(boxes):
    '''From pixel_puzzle4.py'''
    return {min(boxes) - 1, max(boxes) + 1}

def set_contextual_attrs(group):
    '''From pixel_puzzle4.py'''
    for index, item in enumerate(group):
        item.previous = group[index - 1] if index else None
        try:
            item.next = group[index + 1]
        except IndexError:
            item.next = None
        item.before = group[:index]
        item.after = group[index + 1:]

def avoid_oversized_blocks(clue):
    rejected = {possibility for possibility in clue.possible if get_caps(possibility) & clue.clue_group.boxes}
    clue.possible -= rejected

def assign_block_to_clues(block):
    '''From pixel_puzzle4.py'''
    
    boxes = set()
    crosses = set()
    
    # Find possible clues to assign block to:
    rejected_clues = {clue for clue in block.possible_clues if not (clue >= len(block) and any(block.boxes <= possibility for possibility in clue.possible))} 
    block.possible_clues -= rejected_clues
    
    # Extend block near a cross/edge:
    if block.min_length > len(block):
        start = max(block.boxes) - block.min_length + 1
        stop = min(block.boxes) + 1
        possible_cells = {block.clue_group.in_bounds(frozenset(range(x, x + block.min_length))) for x in range(start, stop)}
        new_boxes = frozenset.intersection(*(possibility for possibility in possible_cells if possibility.isdisjoint(block.clue_group.crosses)))
        boxes |= new_boxes
        block.boxes = set(new_boxes)

    # Assign block to a clue if there's only 1 possible clue to assign to:
    if len(block.possible_clues) == 1:
        # Handled by Block.possible_clues setter: clue.found will handle anything else important below
        return boxes, crosses

    caps = get_caps(block.boxes)

    for clue in rejected_clues:
        clue.eliminate_possibilities(block.boxes | caps)
    
    # Mark the block as completed if there's only 1 possible clue size and the block is that size:
    if len(set(clue.clue for clue in block.possible_clues)) == 1 and block.possible_clues.pop().clue == len(block):
        block.completed = True
        crosses |= caps
        
    # If assigning one clue to a block would solve it and the other clue's possibilities can't reach one of the block's adjacent cells, that cell must be a cross:
    # This covers the situation where a block as long as the first clue is close enough to the start of the line that either
    # it is the first clue or there is only just enough space before it to fit the first clue with 1 cross in between them
    elif len(block.possible_clues) == 2 and block.min_length == len(block):
        crosses |= caps - frozenset.union(*(max(block.possible_clues).possible))
    return boxes, crosses

#@functools.lru_cache()
def linkable(*blocks):
    max_length = min(block.max_length for block in blocks)
    combined_boxes = set.union(*(block.boxes for block in blocks))
    distance = max(combined_boxes) - min(combined_boxes)
    return distance < max_length and set(range(min(combined_boxes), max(combined_boxes))).isdisjoint(blocks[0].clue_group.crosses)

def refine_block_assignment_possibilities(clue_group, debug=False):
    '''Remove offside clues from block.possible_clues ie if assigning the clue to that block would leave more blocks before/after that block than (available) clues before/after that clue.
    
    Facilitates assigning each block to a corresponding clue when there are the same number of each and no blocks are potentially linked to each other.'''
    
    if all(block.assigned for block in clue_group.blocks) or len(clue_group.blocks) == 1 or len(clue_group) == 1:
        if debug:
            print('c')
        return
    for n, block in enumerate(clue_group.blocks):
        if debug:
            print(f'refine: {n=}, {block=}')
        if block.assigned:
            continue
        offside_clues = clues_needed_for_other_blocks(block, block.before, iter(clue_group), debug) | clues_needed_for_other_blocks(block, reversed(block.after), reversed(clue_group), debug)
        if debug:
            print(f'{offside_clues=}')
        block.possible_clues -= offside_clues
        if debug:
            print(f'{block}, \n')
        for clue in offside_clues:
            clue.eliminate_possibilities(block.boxes | get_caps(block.boxes))

def clues_needed_for_other_blocks(block, other_blocks, clues, debug):
    if debug:
        #print(f'clues needed: {block=}, {block.links=}, {other_blocks=}, {clues=}')
        print(f'clues needed: {block=}, {other_blocks=}, {clues=}')
    clues_needed_for_other_blocks = set()
    boxes_counted_in_blocks = 0
    boxes_allotted_from_clues = 0
    for other_block in other_blocks:
        if debug:
            print(f'{other_block}')
        #if block in other_block.links:
        if linkable(block, other_block):
            if debug:
                print('a')
            break
        boxes_counted_in_blocks += len(other_block)
        while boxes_counted_in_blocks > boxes_allotted_from_clues:
            next_clue = next(clues)
            boxes_allotted_from_clues += next_clue.clue
            clues_needed_for_other_blocks.add(next_clue)
            if debug:
                print(f'{next_clue=}, {boxes_counted_in_blocks=}, {boxes_allotted_from_clues=}, {clues_needed_for_other_blocks=}')
    if debug:
        print(f'{clues_needed_for_other_blocks=}')
    return clues_needed_for_other_blocks

debug = None
total_arrangements = 0
for i, line in enumerate(data.splitlines()):
    if debug is not None and i != debug:
        continue
    row, clues = line.split()
    clues = [int(clue) for clue in clues.split(',')]
    length = len(row)
    print(i, line, length)
    clue_group = ClueGroup(clues, length)
    springs = {'.': set(), '#': set(), '?': set()}
    for index, spring in enumerate(row):
        springs[spring].add(index)
    clue_group.boxes |= springs['#']
    clue_group.crosses |= springs['.']
    for clue in clue_group:
        avoid_oversized_blocks(clue)
    for block in clue_group.blocks:
        boxes, crosses = assign_block_to_clues(block)
        if boxes:
            clue_group.boxes |= boxes
        if crosses:
            clue_group.crosses |= crosses
    if i == debug:
        print(f'{clue_group=}, {clue_group.boxes=}, {clue_group.crosses=}, {clue_group.unknowns=}, {clue_group.blocks=}')
    refine_block_assignment_possibilities(clue_group, debug=i==debug)
    clue_group_possibilities = [clue.possible for clue in clue_group]
    combinations = list(itertools.product(*clue_group_possibilities))
    #combinations = itertools.product(*clue_group_possibilities)
    #combinations = {tuple(sorted(tuple(sorted(possibility)) for possibility in combo)) for combo in combinations}
    if i == debug:
        print(f'{clue_group=}, {clue_group.boxes=}, {clue_group.crosses=}, {clue_group.unknowns=}, {clue_group.blocks=}')
        #print(combinations)
        print(len(combinations))
    for combo in combinations.copy():
        extended_possibilities = [frozenset(range(min(possibility), max(possibility) + 2)) for possibility in combo]
        if any(frozenset.intersection(*frozenset(pair)) for pair in itertools.combinations(extended_possibilities, 2)) or not clue_group.boxes <= frozenset.union(*combo):
            combinations.remove(combo)
            continue
        if i == debug:
            print(f'\n{combo=}')
        try:
            d = deepcopy(clue_group)
            if i == debug:
                print(f'{d=}, {d.boxes=}, {d.crosses=}, {d.unknowns=}, {d.blocks=}')
            """for possibility in combo:
                if i == debug:
                    print(f'{possibility=}')
                d.boxes |= possibility
                for block in d.blocks:
                    boxes, crosses = assign_block_to_clues(block)
                    if boxes:
                        d.boxes |= boxes
                    if crosses:
                        d.crosses |= crosses
                    link_blocks(block)
                if i == debug:
                    print(f'{d=}, {d.boxes=}, {d.crosses=}, {d.unknowns=}, {d.blocks=}')
            refine_block_assignment_possibilities(d, debug=i==debug)
            if i == debug:
                print(f'{d=}, {d.boxes=}, {d.crosses=}, {d.unknowns=}, {d.blocks=}')
                #break"""
            added = set()
            for possibility, clue in zip(combo, d):
                if not all(box > max(added, default=-1) for box in possibility):
                    combinations.remove(combo)
                    break
                clue.found |= possibility
                added |= possibility
        except (LogicError, ValueError) as e:
            combinations.remove(combo)
            if i == debug:
                print('b', type(e), e, combo)
    unique_legal_combinations =     {tuple(sorted(tuple(sorted(possibility)) for possibility in combo)) for combo in combinations}
    if i == debug:
        print(clue_group)
        print(clue_group.boxes, clue_group.crosses, clue_group.unknowns, clue_group.blocks)
        print(sorted(sorted(sorted(block) for block in combo) for combo in combinations))
    if i == debug:
        print(len(unique_legal_combinations))
        break
    #print(len(combinations))
    print(len(unique_legal_combinations))
    print()
    total_arrangements += len(unique_legal_combinations)
print(total_arrangements)
