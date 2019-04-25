data = '''Vixen can fly 8 km/s for 8 seconds, but then must rest for 53 seconds.
Blitzen can fly 13 km/s for 4 seconds, but then must rest for 49 seconds.
Rudolph can fly 20 km/s for 7 seconds, but then must rest for 132 seconds.
Cupid can fly 12 km/s for 4 seconds, but then must rest for 43 seconds.
Donner can fly 9 km/s for 5 seconds, but then must rest for 38 seconds.
Dasher can fly 10 km/s for 4 seconds, but then must rest for 37 seconds.
Comet can fly 3 km/s for 37 seconds, but then must rest for 76 seconds.
Prancer can fly 9 km/s for 12 seconds, but then must rest for 97 seconds.
Dancer can fly 37 km/s for 1 seconds, but then must rest for 36 seconds.'''

from collections import namedtuple

Reindeer = namedtuple('Reindeer', 'speed stamina rest')

tests = [Reindeer(14, 10, 127), Reindeer(16, 11, 162)]

reindeers = []
for line in data.splitlines():
    words = line.split()
    reindeers.append(Reindeer(int(words[3]), int(words[6]), int(words[-2])))
#print(reindeers)

def distance(reindeer, seconds):
    rounds, remainder = divmod(seconds, reindeer.stamina + reindeer.rest)
    return rounds * reindeer.speed * reindeer.stamina + reindeer.speed * min(remainder, reindeer.stamina)

#for reindeer in tests:
#    print(distance(reindeer, 1000))

#print(max(distance(reindeer, 2503) for reindeer in reindeers))

#reindeers = tests

scores = [0 for _ in range(len(reindeers))]
for sec in range(1, 2504):
    leads = set()
    furthest = 0
    for n, reindeer in enumerate(reindeers):
        flown = distance(reindeer, sec)
        if flown == furthest:
            leads.add(n)
        elif flown > furthest:
            leads = {n}
            furthest = flown
    for lead in leads:
        scores[lead] += 1
print(max(scores))
