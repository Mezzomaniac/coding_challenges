from downloader import download
from copy import copy
from queue import Queue

download(2017, 24)
with open('aoc2017_24input.txt') as inputfile:
    data = inputfile.read()
print(data)


class Component:
    
    def __init__(self, ports):
        self.value = sum(ports)
        self.ports = frozenset(ports)
        self._first = None
        self._second = None
    
    def __eq__(self, other):
        return self.ports == other.ports
    
    def __hash__(self):
        return hash(self.ports)
    
    def __contains__(self, item):
        return item in self.ports
    
    def __repr__(self):
        return f'Component({self.ports})'
    
    def __str__(self):
        return f'{self.first}/{self.second}'
    
    @property
    def first(self):
        if self._first is None:
            raise ValueError
        return self._first
    
    @first.setter
    def first(self, port):
        self._first = port
        if len(self.ports) == 1:
            self._second = port
        else:
            self._second = (set(self.ports) - {port}).pop()
    
    @property
    def second(self):
        if self._second is None:
            raise ValueError
        return self._second
        

components = {Component([int(n) for n in component.split('/')]) for component in data.splitlines()}
starts = {component for component in components if 0 in component}

strongest = 0
longest = 0
longest_strength = 0
frontier = Queue()
for start in starts:
    start.first = 0
    frontier.put((copy(start),))
while not frontier.empty():
    current = frontier.get()
    #print([str(component) for component in current])
    if (length := len(current)) > longest:
        longest = length
        longest_strength = 0
        print(length)
    port = current[-1].second
    if not (options := {component for component in components if component not in current and port in component}):
        strength = sum(component.value for component in current)
        if strength > strongest:
            strongest = strength
            #print(strength)
        if length == longest and strength > longest_strength:
            longest_strength = strength
        continue
    for option in options:
        option.first = port
        frontier.put(current + (copy(option),))
print(strongest)
print(longest_strength)
