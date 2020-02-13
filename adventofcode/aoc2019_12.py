data = '''<x=14, y=2, z=8>
<x=7, y=4, z=10>
<x=1, y=17, z=16>
<x=-4, y=-1, z=1>'''

test1 = '''<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>'''
#2772

test2 = '''<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>'''
#4686774924

#data = test2

from collections import defaultdict
import re
from functools import reduce
from math import gcd
from time import time
import matplotlib
import matplotlib.pyplot as plt

class Moon:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.x_vel = 0
        self.y_vel = 0
        self.z_vel = 0
    
    @property
    def pos(self):
        return (self.x, self.y, self.z)
    
    @property
    def vel(self):
        return (self.x_vel, self.y_vel, self.z_vel)
    
    @property
    def potential(self):
        return sum(abs(axis) for axis in self.pos)
    
    @property
    def kinetic(self):
        return sum(abs(axis) for axis in self.vel)
    
    @property
    def energy(self):
        return self.potential * self.kinetic
    
    def __repr__(self):
        return f'Moon{self.pos}'
    
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.z += self.z_vel

t = time()

positions = ((int(d.group()) for d in re.finditer('-?\d+', line)) for line in data.splitlines())
moons = [Moon(*moon) for moon in positions]
print(moons)

def repeating(seq):
    margin = 10000
    length = len(seq)
    if length < 4:
        return False
    #return seq[:length//2] == seq[length//2:]# and seq[:length//4] == list(reversed(seq[length//4:length//2]))
    a = list(reversed(seq[-margin:])) == seq[margin*-2:-margin]
    b = seq[:length//2] == seq[length//2:]
    if a:
        result = (len(seq) - margin + 1) * 2
        print('a', result)
        return result
    if b:
        result = len(seq) // 2
        print('b', result)
        return result
    #return a or b

states = {}
step = 0
positions = tuple(moon.pos for moon in moons)
velocities = tuple(moon.vel for moon in moons)
print(positions)
print(velocities)
#start_positions = positions
print()
#moon0x_history = defaultdict(list) #--> period of (ie repeats from step) 268296
#moon0y_history = defaultdict(list) #--> period of 231614
#moon0z_history = defaultdict(list) #--> period of 52442 * 2 + 2
#moon0x_vel_history = defaultdict(list)
'''histories = {f'moon{n}{attr}': defaultdict(set) for n, moon in enumerate(moons) for attr in vars(moon)}
last_new_values = {}'''
periods = {}
histories = {f'moon{n}{attr}': [] for n, moon in enumerate(moons) for attr in vars(moon)}
sequenced = set()
#print(histories)
#print(len(histories))
#while step < 1000:
#while not states.get(positions, False) == velocities:
#while step < 100:
#while len(periods) < 24:
#while not all(periods.values()) or step < 6:
#while len(sequenced) < 24:
while False:
    #states[positions] = velocities
    #moon0x_history[moons[0].x].append(step)
    #moon0y_history[moons[0].y].append(step)
    #moon0z_history[moons[0].z].append(step)
    #moon0x_vel_history[moons[0].x_vel].append(step)
    for n, moon in enumerate(moons):
        #for attr, value in vars(moon).items():
            #histories[f'moon{n}{attr}'][value].add(step)
        for other in moons:
            for axis in 'xyz':
                moon_axis = getattr(moon, axis)
                other_axis = getattr(other, axis)
                if moon_axis == other_axis:
                    continue
                accel = (-1, 1)[other_axis > moon_axis]
                setattr(moon, axis + '_vel', getattr(moon, axis + '_vel') + accel)
    for moon in moons:
        moon.move()
    positions = tuple(moon.pos for moon in moons)
    velocities = tuple(moon.vel for moon in moons)
    step += 1
    #print(step)
    #print(positions)
    '''if any(start == current for start, current in zip(start_positions, positions)):
        print(step)
        print(positions)
        print(velocities)
        break'''
    #print(velocities)
    #print()
    #moon0x = moons[0].x
    #if moon0x not in moon0x_history:
    #if moon0x in moon0x_history and step > 134147 * 2 - 20:
        #print('moon0x', step, moon0x, moon0x_history[moon0x])
    #moon0y = moons[0].y
    #if moon0y in moon0y_history and step > 115806 * 2:
        #print(step, moon0y, moon0y_history[moon0y])
    #moon0z = moons[0].z
    #if moon0z not in moon0z_history and step > 0 * 2:
        #print(step, moon0z, moon0z_history[moon0z])
    #moon0x_vel = moons[0].x_vel
    #if moon0x_vel not in moon0x_vel_history and step > 0 * 2:
        #print(step, moon0x_vel, moon0x_vel_history[moon0x_vel])
    for n, moon in enumerate(moons):
        for attr, value in vars(moon).items():
            key = f'moon{n}{attr}'
            #repeating = all(len(value) >= 2 for value in histories[key].values())
            #if value not in histories[key]:
                #last_new_values[key] = step
            #elif step > last_new_values[key] + 15 and not periods.get(key, None):
                #period = last_new_values[key] * 2 + 2
                #period = step
            #period = repeating and (periods.get(key, None) or step)
            #periods[key] = period
                #print(key, period)
            if key not in sequenced:
                histories[key].append(value)
                if repeating(histories[key]):
                    sequenced.add(key)
                    print(key, len(histories[key]) // 2)
                    #print(histories[key])
                    periods[key] = len(histories[key]) // 2
                    del histories[key]

    if not step % 10000:
        print(step)
    #print(histories)
    #print()
#print(sum(moon.energy for moon in moons))
#print(step)
#fig, ax = plt.subplots()
#ax.plot(moon0x_history)
#plt.show()
#print(sorted(periods.items()))
#print(histories)
#periods = {key: len(value) // 2 for key, value in histories.items()}

def find_period(start_data, moon_n, attr):
    positions = ((int(d.group()) for d in re.finditer('-?\d+', line)) for line in data.splitlines())
    moons = [Moon(*moon) for moon in positions]
    step = 0
    history = []
    found = False
    while not found:
        for n, moon in enumerate(moons):
            for other in moons:
                for axis in 'xyz':
                    moon_axis = getattr(moon, axis)
                    other_axis = getattr(other, axis)
                    if moon_axis == other_axis:
                        continue
                    accel = (-1, 1)[other_axis > moon_axis]
                    setattr(moon, axis + '_vel', getattr(moon, axis + '_vel') + accel)
        for moon in moons:
            moon.move()
        step += 1
        history.append(getattr(moons[moon_n], attr))
        #if repeating(history):
            #print(history)
            #return len(history) // 2
        repeats = repeating(history)
        if repeats:
            return repeats
        if not step % 1000:
            print(step)

periods = {'moon0x': 268296, 'moon0y': 231614, 'moon0z': 108344, 'moon0x_vel': 268296, 'moon0y_vel': 3, 'moon0z_vel': 108344, 'moon1x': 268296, 'moon1y': 231614, 'moon1z': 4, 'moon1x_vel': 268296, 'moon1y_vel': 231614, 'moon1z_vel': 108344, 'moon2x': 268296, 'moon2y': 231614, 'moon2z': 108344, 'moon2x_vel': 268296}

for n, moon in enumerate(moons):
    for attr in vars(moon).keys():
        key = f'moon{n}{attr}'
        if key in periods:
            continue
        print(key)
        period = find_period(data, n, attr)
        print(period)
        periods[key] = period
        print()
print(sorted(periods.items()))

def lcm(a, b):
    return a * b // gcd(a, b)


print(time() - t)
# < 69950342790490845340587239063270088641562135271274136271238705274797673111146104231306750203392365275465
# != 2844050207793167082493482797979224488916876052411202632379369950655603099120798201440
# != 1422025103896583541246741398989612244458438026205601316189684975327801549560399100720