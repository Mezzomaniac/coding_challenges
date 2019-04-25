from string import ascii_lowercase as abc
import time
import clipboard

data = clipboard.get()

def react(polymer):
    polymer = list(polymer)
    delete = []
    for i, unit in enumerate(polymer[:-1]):
        if i in delete:
            continue
        if abs(ord(unit) - ord(polymer[i+1])) == 32:
            delete.extend([i, i+1])
    for i in delete[::-1]:
        del polymer[i]
    return ''.join(polymer)

def react_v2(polymer):
    for letter in abc:
        polymer = polymer.replace(letter + letter.upper(), '').replace(letter.upper() + letter, '')
    return polymer

def react_fully(polymer):
    while True:
        previous = polymer
        polymer = react(polymer)
        if polymer == previous:
            return polymer

def react_fully_v2(polymer):
    while True:
        previous = polymer
        polymer = react_v2(polymer)
        if polymer == previous:
            return polymer

#start = time.time()
#print(len(react_fully(data)))
#print(time.time() - start)

#start = time.time()
print(len(react_fully_v2(data)))
#print(time.time() - start)

trials = set()
for letter in abc:
    #print(letter)
    trial = data.replace(letter, '').replace(letter.upper(), '')
    trials.add(len(react_fully_v2(trial)))
print(min(trials))
