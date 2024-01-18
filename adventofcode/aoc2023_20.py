from downloader import download

download(2023, 20)
with open('aoc2023_20input.txt') as inputfile:
    data = inputfile.read()
test_data1 = '''broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a'''
test_data2 = '''broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output'''
#data = test_data2
print(data)

from collections import namedtuple
from functools import reduce
from operator import mul
from math import lcm
from queue import Queue

Pulse = namedtuple('Pulse', 'source pulse destination')

class Module:
    
    def __init__(self, name: str, type_: str, destinations: list):
        self.name = name
        self.destinations = destinations
        self.type = type_
        if type_ == '%':
            self.status = 0
        elif type_ == '&':
            self.memory = {}
    
    def __repr__(self):
        return f'Module({self.name}, {self.type}, {self.destinations})'
    
    def respond(self, source: str, input: int) -> list[Pulse]:
        if self.type == '%':
            if input:
                return []
            self.status = not self.status
            return [Pulse(self.name, self.status, destination) for destination in self.destinations]
        if self.type == '&':
            self.memory[source] = input
            return [Pulse(self.name, not all(self.memory.values()), destination) for destination in self.destinations]
        return [Pulse(self.name, input, destination) for destination in self.destinations]

modules = {}
conjunctions = set()
for line in data.splitlines():
    module, destinations = line.split(' -> ')
    type_ = None
    if module[0] in '%&':
        type_ = module[0]
        module = module[1:]
    if type_ == '&':
        conjunctions.add(module)
    modules[module] = Module(module, type_, destinations.split(', '))
for name, module in modules.items():
    for conjunction in conjunctions:
        if conjunction in module.destinations:
            modules[conjunction].memory[name] = 0

def press_button(goal=None):
    pulses = [1, 0]
    goal_achieved = False
    start = Pulse('button', 0, 'broadcaster')
    communications = Queue()
    communications.put(start)
    while not communications.empty():
        current_pulse = communications.get()
        if current_pulse.destination == goal:
            if not current_pulse.pulse:
                goal_achieved = True
                break
            if any(modules[current_pulse.source].memory.values()):
                print(button_presses, modules[current_pulse.source].memory)
        if current_pulse.destination not in modules:
            continue
        for next_pulse in modules[current_pulse.destination].respond(current_pulse.source, current_pulse.pulse):
            pulses[next_pulse.pulse] += 1
            communications.put(next_pulse)
    return (pulses, goal_achieved)

#print(reduce(mul, (sum(pulses) for pulses in zip(*(press_button()[0] for time in range(1000))))))

button_presses = 0
goal_achieved = False
while not goal_achieved:
    button_presses += 1
    goal_achieved = press_button('rx')[1]
    if not button_presses % 10000:
        print(button_presses)
print(button_presses)


print(lcm(3823, 3847, 3877, 4001))
