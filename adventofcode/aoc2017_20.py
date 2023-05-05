from downloader import download

download(2017, 20)
with open('aoc2017_20input.txt') as inputfile:
    data = inputfile.read()
print(data)

class Vector:
    
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __iter__(self):
        return iter((self.x, self.y, self.z))
    
    def __eq__(self, other):
        return (self.x, self.y, self.z) == (other.x, other.y, other.z)
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

class Particle:
    
    def __init__(self, id, pos, vel, acc):
        self.id = id
        self.pos = pos
        self.vel = vel
        self.acc = acc

lowest_acc = None
lowest_acc_id = None
particles = []
for i, line in enumerate(data.splitlines()):
    particle = Particle(i, *[Vector(*[int(n) for n in vector[3:-1].split(',')]) for vector in line.split(', ')])
    scalar_acc = sum(abs(axis) for axis in particle.acc)
    if lowest_acc_id is None or scalar_acc < lowest_acc:
        lowest_acc = scalar_acc
        lowest_acc_id = particle.id
    particles.append(particle)
print(lowest_acc_id)

last_collision = 0
step = 0
while step < last_collision + 100:
    step += 1
    updated = []
    positions = []
    collisions = []
    for particle in particles:
        particle.vel += particle.acc
        particle.pos += particle.vel
        pos = particle.pos
        if pos in collisions:
            continue
        elif pos in positions:
            collisions.append(pos)
            updated = [particle for particle in updated if particle.pos != pos]
            last_collision = step
        else:
            positions.append(pos)
            updated.append(particle)
    particles = updated
print(len(particles))
