data = '123487596'
test = '389125467'
#data = test

highest = 9 and 1000000
moves = 100 and 10000000

from collections import deque

def setup(data, highest=9):
    '''deque'''
    cups = deque(int(cup) for cup in data)
    high = max(cups)
    if highest > high:
        cups.extend(range(high+1, highest+1))
    return cups

def move(cups, highest):
    '''deque/list'''
    cups = list(cups)
    current = cups[0]
    removed = cups[1:4]
    del cups[1:4]
    destination = current - 1 or highest
    while destination in removed:
        destination = destination - 1 or highest
    index = cups.index(destination) + 1
    cups[index:index] = removed
    cups = deque(cups)
    cups.rotate(-1)
    return cups

def score(cups, simple=True):
    '''deque'''
    while cups[0] != 1:
        cups.rotate()
    cups.popleft()
    if simple:
        return ''.join(str(cup) for cup in cups)
    return cups.popleft() * cups.popleft()

def setup2(data, highest):
    '''dict'''
    cups = {}
    high = 0
    first = int(data[0])
    high = max(high, first)
    current = first
    for cup in data[1:]:
        new = int(cup)
        cups[current] = new
        high = max(high, new)
        current = new
    if highest > high:
        for new in range(high+1, highest+1):
            cups[current] = new
            current = new
    cups[current] = first
    return cups, first

def move2(cups, current, highest):
    '''dict'''
    removed = []
    next = cups[current]
    for cup in range(3):
        removed.append(next)
        next = cups[next]
    cups[current] = next
    destination = current - 1 or highest
    while destination in removed:
        destination = destination - 1 or highest
    following = cups[destination]
    for cup in removed:
        cups[destination] = cup
        destination = cup
    cups[destination] = following
    return cups, next

def score2(cups, simple=False):
    '''dict'''
    return cups[1] * cups[cups[1]]

#cups = setup(data, highest)
cups, current = setup2(data, highest)
for i in range(moves):
    if not i % 100000:
        print(i)
    #cups = move(cups, highest)
    cups, current = move2(cups, current, highest)
    #print(cups)
#print(score(cups, False))
print(score2(cups))
