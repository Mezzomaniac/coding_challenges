from collections import defaultdict, deque, Counter
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


roll_probabilities = Counter(sum(combo) for combo in product(range(1, 4), repeat=3))

'''class GameState:
    
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
    for roll_sum, probability in roll_probabilities.items():
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
print(max(wins))'''


#>43_042_313_591

'''coin_probabilities = {2: 1, 3: 2, 4: 1}
coin_probabilities = {1: 1, 2: 1}

def turns_to_end_profile(start, board_size=10, win=21, move_probabilities=None):
    if not move_probabilities:
        move_probabilities = roll_probabilities
    end_worlds = defaultdict(int)
    pos_score_worlds = {(start, 0): 1}
    turn = 0
    #while any(score < win for pos, score in pos_score_worlds.keys()):
    while pos_score_worlds:
        turn += 1
        new_pos_score_worlds = defaultdict(int)
        for (pos, score), worlds in pos_score_worlds.items():
            for move, probability in move_probabilities.items():
                new_pos = pos + move
                if new_pos > board_size:
                    new_pos -= board_size
                new_score = score + new_pos
                new_worlds = worlds * probability
                if new_score >= win:
                    end_worlds[turn] += new_worlds
                    continue
                new_pos_score_worlds[(new_pos, new_score)] += new_worlds
            pos_score_worlds = new_pos_score_worlds
    return end_worlds

def compare_profiles(starts, board_size=10, win=21, move_probabilities=None):
    if not move_probabilities:
        move_probabilities = roll_probabilities
    p1_profile = turns_to_end_profile(starts[0], board_size, win, move_probabilities)
    p2_profile = turns_to_end_profile(starts[1], board_size, win, move_probabilities)
    #p1_profile = {2: 3, 3: 2}
    #p2_profile = {2: 3, 3: 2}
    print(p1_profile)
    print(p2_profile)
    rolls_per_turn = sum(move_probabilities.values())
    #rolls_per_turn = 2
    p1_wins = 0
    p2_wins = 0
    for turn in set(p1_profile.keys()) | set(p2_profile.keys()):
        print(turn)
        p1_wins += p1_profile[turn] * (rolls_per_turn ** (turn - 1) - sum(worlds * (turn - turns) for turns, worlds in p2_profile.items() if turns < turn))
        p2_wins += p2_profile[turn] * (rolls_per_turn ** turn - sum(worlds * (turn - turns + 1) for turns, worlds in p1_profile.items() if turns <= turn))
        print(p1_wins, p2_wins)
    return max(p1_wins, p2_wins)

#print(compare_profiles((2, 4), 5, 11, coin_probabilities))
#print(compare_profiles((5, 5), 5, 5, coin_probabilities))

#print(compare_profiles((4, 8)))
#print(compare_profiles((9, 3)))'''

state_worlds = {((4, 0), (8, 0)): 1}
state_worlds = {((9, 0), (3, 0)): 1}
wins = [0, 0]
player = 0
while state_worlds:
    new_state_worlds = defaultdict(int)
    for state, worlds in state_worlds.items():
        pos, score = state[player]
        for roll, probability in roll_probabilities.items():
            new_pos = pos + roll
            if new_pos > 10:
                new_pos -= 10
            new_score = score + new_pos
            new_worlds = worlds * probability
            if new_score >= 21:
                wins[player] += new_worlds
                continue
            new_state = list(state)
            new_state[player] = (new_pos, new_score)
            new_state = tuple(new_state)
            new_state_worlds[new_state] += new_worlds
        state_worlds = new_state_worlds
    player = not player
print(wins)
print(max(wins))
