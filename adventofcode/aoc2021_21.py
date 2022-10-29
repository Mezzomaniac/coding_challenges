from collections import defaultdict, deque, Counter
#from copy import deepcopy
from functools import lru_cache
from itertools import product
from pprint import pprint
from queue import Queue

positions = [deque(range(1, 11)), deque(range(1, 11))]
positions[0].rotate(-8)  # 9
positions[1].rotate(-2)  # 3
scores = [0, 0]
player = 0
die = 100
total_rolls = 0

while max(scores) < 1000:
    roll_sum = 0
    for roll in range(3):
        die += 1
        if die > 100:
            die - 100
        roll_sum += die
    total_rolls += 3
    positions[player].rotate(-roll_sum)
    scores[player] += positions[player][0]
    player = not player

print(total_rolls * min(scores))


probabilities = Counter(sum(combo) for combo in product(range(1, 4), repeat=3))

class GameState:
    
    def __init__(self, positions, scores, player):
        self.positions = positions
        self.scores = scores
        self.player = player
         
    def __eq__(self, other):
        return hash(self) == hash(other)
      
    def __hash__(self):
        #return hash(((self.positions[0][0], self.positions[1][0]), tuple(self.scores), self.player))
        return hash(tuple(self.positions), tuple(self.scores), self.player)
      
    def __repr__(self):
        return f'GameState({self.positions}, {self.scores}, {self.player})'
    
    def __str__(self):
        #return f'GameState({(self.positions[0][0], self.positions[1][0])}, {self.scores}, {int(self.player)})'
        return f'GameState({self.positions}, {self.scores}, {int(self.player)})'
      
    def winner(self):
        for player, score in enumerate(self.scores):
            if score >= 21:
                return player
      
    def turn(self, roll_sum):
        #positions = deepcopy(self.positions)
        #positions[self.player].rotate(-roll_sum)
        scores = self.scores.copy()
        scores[self.player] += positions[self.player][0]
        player = not self.player
        return GameState(positions, scores, player)


@lru_cache()
def move(pos):
    


positions = [deque(range(1, 11)), deque(range(1, 11))]
#positions[0].rotate(-8)  # 9
#positions[1].rotate(-2)  # 3
positions[0].rotate(-3)  # 4
positions[1].rotate(-7)  # 8
scores = [0, 0]
player = 0


wins = [0, 0]
universes = defaultdict(int)
frontier = Queue()
start = GameState(positions, scores, player)
universes[start] = 1
frontier.put(start)
while not frontier.empty():
    current = frontier.get()
    #print(current)
    winner = current.winner()
    if winner is not None:
        wins[winner] += universes[current]
        #print([f'{win:_}' for win in wins])
        continue
    for roll_sum, probability in probabilities.items():
        next = current.turn(roll_sum)
        probability *= universes[current]
        if next in universes:
            #print(next, universes[next])
            universes[next] += probability
            frontier.put(next)
        else:
            universes[next] = probability
            frontier.put(next)
    del universes[current]
    #pprint([(str(key), value) for key, value in universes.items()])
    #print()
print(max(wins))


#>43_042_313_591


'''def play(pos, score, turns):
    turns_to_win = {}
    turn += 1
    for move, probability in probabilities.items():
        pos += move
        if pos > 10:
            pos -= 10
        score += pos
        if score >= 21:
            '''
