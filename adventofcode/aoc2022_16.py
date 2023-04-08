from downloader import download
from queue import Queue, PriorityQueue
from itertools import product

download(2022, 16)
with open('aoc2022_16input.txt') as inputfile:
    data = inputfile.read()
    
test_data = '''Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II'''
#data = test_data
print(data)

class Valve:
    
    def __init__(self, label: str, flow: int, tunnels: list):
        self.label = label
        self.flow = flow
        self.tunnels = tunnels
    
    def __repr__(self):
        return f'Valve({self.label}, {self.flow}, {self.tunnels})'

class State:
    
    def __init__(self, location: str, opened: dict=None):
        self.location = location
        if opened is None:
            opened = {}
        self.opened = opened
    
    def __repr__(self):
        return f'Valve({self.location}, {self.opened})'
    
    def __hash__(self):
        return hash((self.location, tuple(self.opened.items())))
    
    def __eq__(self, other):
        return hash(self) == hash(other)
        
valves = {}
for line in data.splitlines():
    label = line[6: 8]
    flow = int(line[23: line.index(';')])
    tunnels = [valve.strip() for valve in line[line.index('valve') + 6:].split(', ')]
    valves[label] = Valve(label, flow, tunnels)
number_of_valves_to_open = len([valve for valve in valves.values() if valve.flow])
#print(valves)
print(number_of_valves_to_open)

def total_flow(opened, period):
    return sum(valves[label].flow * (period - time) for label, time in opened.items())

most_flow = 0
minutes_explored = 0
start = State('AA')
costs = {start: 1}
frontier = Queue()
frontier.put(start)
while not frontier.empty():
    break
    current_state = frontier.get()
    if costs[current_state] > minutes_explored:
        minutes_explored = costs[current_state]
        print(minutes_explored)
    if costs[current_state] == 31 or len(current_state.opened) == number_of_valves_to_open:
        flow = total_flow(current_state.opened, 30)
        if flow > most_flow:
            most_flow = flow
            print(most_flow)
        continue
    next_cost = costs[current_state] + 1
    if valves[current_state.location].flow and current_state.location not in current_state.opened:
        next_opened = current_state.opened.copy()
        next_opened[current_state.location] = costs[current_state]
        next_state = State(current_state.location, next_opened)
        if next_state not in costs or next_cost < costs[next_state]:
            frontier.put(next_state)
            costs[next_state] = next_cost
    for next_location in valves[current_state.location].tunnels:
        next_state = State(next_location, current_state.opened.copy())
        if next_state not in costs or next_cost < costs[next_state]:
            frontier.put(next_state)
            costs[next_state] = next_cost
print(most_flow)

class DoubleState:
    
    def __init__(self, locations: tuple, opened: dict=None, minute: int=1):
        self.locations = locations
        if opened is None:
            opened = {}
        self.opened = opened
        self.minute = minute
        self.flow = 0
    
    def __repr__(self):
        return f'Valve({self.locations}, {self.opened}, {self.minute})'
    
    def __hash__(self):
        return hash((frozenset(self.locations), tuple(self.opened.items())))
    
    def __eq__(self, other):
        return hash(self) == hash(other)
    
    def __lt__(self, other):
        return self.flow < other.flow

'''most_flow = 0
minutes_explored = 0
start = DoubleState(('AA', 'AA'))
costs = {start: 1}
frontier = Queue()
frontier.put(start)
while not frontier.empty():
    current_state = frontier.get()
    minute = current_state.minute
    if minute > minutes_explored:
        minutes_explored = minute
        print(minutes_explored, frontier.qsize(), len(costs))
        #if minutes_explored > 9:
            #costs = {state: cost for state, cost in costs.items() if cost > minutes_explored - 4}
    if minute == 27 or len(current_state.opened) == number_of_valves_to_open:
        flow = total_flow(current_state.opened, 26)
        if flow > most_flow:
            most_flow = flow
            print(most_flow, minute, len(current_state.opened))
        continue
    next_cost = minute + 1
    partial_next_states = [set(), set()]
    for index, location in enumerate(current_state.locations):
        if valves[location].flow and location not in current_state.opened:
            partial_next_opened = current_state.opened.copy()
            partial_next_opened[location] = minute
            partial_next_state = State(location, partial_next_opened)
            partial_next_states[index].add(partial_next_state)
            continue
        for next_location in valves[location].tunnels:
            partial_next_state = State(next_location, current_state.opened.copy())
            partial_next_states[index].add(partial_next_state)
    for partial_next_state1, partial_next_state2 in product(*partial_next_states):
        next_opened = partial_next_state1.opened.copy()
        next_opened.update(partial_next_state2.opened)
        next_state = DoubleState((partial_next_state1.location, partial_next_state2.location), next_opened, next_cost)
        if next_state not in costs or next_cost < costs[next_state]:
            frontier.put(next_state)
            costs[next_state] = next_cost
            #print(next_state)
print(most_flow)'''

most_flow = 0
minutes_explored = 0
start = DoubleState(('AA', 'AA'))
costs = {start: 1}
frontier = PriorityQueue()
frontier.put((1, start))
while not frontier.empty():
    priority, current_state = frontier.get()
    minute = current_state.minute
    if minute > minutes_explored:
        minutes_explored = minute
        print(minutes_explored, frontier.qsize(), len(costs))
    if minute == 27 or len(current_state.opened) == number_of_valves_to_open:
        flow = current_state.flow
        if flow > most_flow:
            most_flow = flow
            print(most_flow, minute, len(current_state.opened), frontier.qsize(), len(costs))
            #costs = {state: cost for state, cost in costs.items() if cost < 22}
        continue
    next_cost = minute + 1
    partial_next_states = [[], []]
    for index, location in enumerate(current_state.locations):
        if valves[location].flow and location not in current_state.opened:
            partial_next_opened = current_state.opened.copy()
            partial_next_opened[location] = minute
            partial_next_state = State(location, partial_next_opened)
            partial_next_states[index].append(partial_next_state)
            continue
        for next_location in valves[location].tunnels:
            partial_next_state = State(next_location, current_state.opened.copy())
            partial_next_states[index].append(partial_next_state)
    for partial_next_state1, partial_next_state2 in product(*partial_next_states):
        next_opened = partial_next_state1.opened.copy()
        next_opened.update(partial_next_state2.opened)
        next_state = DoubleState((partial_next_state1.location, partial_next_state2.location), next_opened, next_cost)
        if next_state not in costs or next_cost < costs[next_state]:
            flow = total_flow(next_opened, 26)
            next_state.flow = flow
            num_valves_opened = len(next_opened)
            step_value = sum(valves[location].flow for location in next_state.locations if location not in next_opened)
            priority = next_cost - 1.7 * num_valves_opened - step_value - 0.0015 * flow
            #priority = (-flow, -step_value, -num_valves_opened, next_cost)
            frontier.put((priority, next_state))
            costs[next_state] = next_cost
            #print(next_state)
            if len(costs) + frontier.qsize() > 3100000:
                costs = {state: cost for state, cost in costs.items() if cost < 20}
                print('a')
print(most_flow)
