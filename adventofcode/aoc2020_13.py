ready_time = 1005595
data = '''41,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,37,x,x,x,x,x,557,x,29,x,x,x,x,x,x,x,x,x,x,13,x,x,x,17,x,x,x,x,x,23,x,x,x,x,x,x,x,419,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,19'''
test1 = '17,x,13,19'
test2 = '67,7,59,61'
test3 = '67,x,7,59,61'
test4 = '67,7,x,59,61'
test5 = '1789,37,47,1889'
test = '3,5,7'
#data = test5

import itertools
#import matplotlib.pyplot as plt

buses = set(data.split(','))
buses.discard('x')
buses = {int(bus) for bus in buses}
soonest_bus = None
shortest_wait = ready_time
for bus in buses:
    wait = bus - (ready_time % bus)
    if wait < shortest_wait:
        soonest_bus = bus
        shortest_wait = wait
print(soonest_bus * shortest_wait)

'''buses = data.split(',')
sets = []
prev_set = {x - 0 for x in range(0, 100000000, int(buses[0]))}
for i, bus in enumerate(data.split(',')[1:], 1):
    if bus == 'x':
        continue
    current_set = {x - i for x in range(0, 100000000, int(bus))}
    match = prev_set | current_set
    print(match)
    prev_set = current_set
    #sets.append(numbers)
#print(min(set.intersection(*sets)))'''
    
first = int(data.split(',')[0])
offsets = {int(bus): offset for offset, bus in enumerate(data.split(',')[1:], 1) if bus != 'x'}
print(offsets, first)
'''offsets = {int(bus): offset for offset, bus in enumerate(data.split(',')) if bus != 'x'}
highest = max(offsets.keys())
offset_for_highest = offsets[highest]
offsets.pop(highest)
print(offsets, highest, offset_for_highest)'''
skip_factor = 1
skip_factor = 0 #100000000000000 // 1000
start = first * skip_factor
step = first
#start = highest * skip_factor - offset_for_highest
#step = highest
'''for t in itertools.count(start=start, step=step):
    #if not t % 1000000:
        #print(t)
    difs = [bus - (t % bus) for bus in offsets.keys()]
    #print(t, difs)#, sum(difs), sum(difs) - sum(offsets.values()))
    if all((bus - (t % bus)) == (offset or bus) for bus, offset in offsets.items()):
        print(t)
        break'''

# https://en.wikipedia.org/wiki/Chinese_remainder_theorem
offsets = {int(bus): (int(bus) - offset) % int(bus) for offset, bus in enumerate(data.split(',')) if bus != 'x'}
offsets = list(sorted(list(offsets.items()), reverse=True))
print(offsets)
factor, answer = offsets[0]
for bus, offset in offsets[1:]:
    print(bus, offset)
    while (answer % bus) != offset:
        answer += factor
        #print(answer)
    factor *= bus
print(answer)

'''offsets = {int(bus): offset for offset, bus in enumerate(data.split(',')) if bus != 'x'}
#series = [[(bus * x - offset) % (2*3*5*7) for x in range(0, 20)] for bus, offset in offsets.items()]
plot = [sum(bus * (bus - ((x - offset) % bus)) for x in range(10) for bus, offset in offsets.items())]
#for plot in series:
    #plt.plot(plot)
plt.plot(plot)
plt.show()'''

#all_offsets = {int(bus): offset for offset, bus in enumerate(data.split(',')[1:], 1) if bus != 'x'}
#offsets = reversed(list(all_offsets.items()))

'''answer = 1
for bus, offset in all_offsets.items():
    print(answer, bus, offset)
    inverse = (answer ** (bus - 2)) % bus
    answer *= (inverse * ((bus - offset) % bus)) % bus
    #factors.append(factor)
#print(factors)
#answer = reduce(mul, factors, 1)
print(answer)'''
