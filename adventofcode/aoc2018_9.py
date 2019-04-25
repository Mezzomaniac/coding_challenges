from collections import deque
import time

import matplotlib
import matplotlib.pyplot as plt

PLAYERS, MARBLES = 463, 7178700
PLAYERS1, MARBLES1 = 10, 1618  # 8317

def play(players, last_marble):
    '''list'''
    marbles = [0]
    scores = [0 for _ in range(players)]
    #scoring = []
    current = 0
    for marble in range(1, last_marble - last_marble % 23 + 1):
        if marble % 23:
            insertion_index = marbles.index(current) + 2
            if insertion_index > len(marbles):
                insertion_index = 1
            marbles.insert(insertion_index, marble)
            current = marble
            #if not marble % 1000:
                #print(marble)
        else:
            player = (marble - 1) % players
            removal_index = marbles.index(current) - 7
            if removal_index < 0:
                removal_index += len(marbles)
            score = (marble, marbles[removal_index])
            #scoring.append(score)
            scores[player] += sum(score)
            del marbles[removal_index]
            current = marbles[removal_index]
    #x,y = zip(*scoring)
    #fig, ax = plt.subplots()
    #ax.plot(x,y)
    #plt.show()
    #print(scoring)
    return max(scores)

#start = time.time()
#print(play(463, 71787))
#try:
#print(play(PLAYERS, MARBLES))
#except KeyboardInterrupt:
#print(time.time() - start)


def play2(players, last_marble):
    '''deque'''
    marbles = deque([0])
    scores = [0 for _ in range(players)]
    current = 0
    for marble in range(1, last_marble - last_marble % 23 + 1):
        if marble % 23:
            insertion_index = marbles.index(current) + 2
            if insertion_index > len(marbles):
                insertion_index = 1
            marbles.insert(insertion_index, marble)
            current = marble
            #if not marble % 1000:
                #print(marble)
        else:
            player = (marble - 1) % players
            removal_index = marbles.index(current) - 7
            if removal_index < 0:
                removal_index += len(marbles)
            score = (marble, marbles[removal_index])
            scores[player] += sum(score)
            delete_nth(marbles, removal_index)
            current = marbles[removal_index]
    return max(scores)

def delete_nth(d, n):
    d.rotate(-n)
    d.popleft()
    d.rotate(n)

#start = time.time()
#try:
#print(play2(PLAYERS, MARBLES))
#except KeyboardInterrupt:
#print(time.time() - start)


class Node:
    def __init__(self, value, prev=None, next=None):
        self.value = value
        self.prev = prev
        self.next = next

def play3(players, last_marble):
    '''double-linked list'''
    first = Node(0)
    first.prev = first
    first.next = first
    scores = [0 for _ in range(players)]
    current = first
    for marble in range(1, last_marble - last_marble % 23 + 1):
        if marble % 23:
            new = Node(marble)
            new.next = current.next.next
            new.prev = current.next
            current.next.next.prev = new
            current.next.next = new
            current = new
            #if not marble % 1000:
                #print(marble)
        else:
            player = (marble - 1) % players
            removing = current
            for _ in range(7):
                removing = removing.prev
            score = (marble, removing.value)
            scores[player] += sum(score)
            removing.prev.next = removing.next
            removing.next.prev = removing.prev
            current = removing.next
            del removing
    return max(scores)


for func in (play3,):# play2, play3):
    #print(func.__name__)
    start = time.time()
#try:
    print(func(PLAYERS, MARBLES))
#except KeyboardInterrupt:
    print(time.time() - start)
    #print()
