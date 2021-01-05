size = 3005290

from collections import deque

def play(size):
    elves = deque(range(1, size+1))
    elves.rotate(-1)
    while len(elves) > 1:
        elves.popleft()
        elves.rotate(-1)
    return elves.pop()

def play(size):
    elves = deque(range(1, size+1))
    elves.rotate(-(size // 2))
    while len(elves) > 1:
        elves.popleft()
        elves.rotate(-1 +len(elves)%2)
        if not len(elves) % 10000:
            print(len(elves))
        #print(elves)
    return elves.pop()

#for size in range(2, 21):
print(play(size))
