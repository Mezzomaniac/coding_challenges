from downloader import download

download(2017, 11)
with open('aoc2017_11input.txt') as inputfile:
    data = inputfile.read()
#print(data)

def hexdistance(q, r, s):
    return (abs(q) + abs(r) + abs(s)) // 2

q = 0
r = 0
s = 0
maxdistance = 0
for step in data.strip().split(','):
    if step == 'n':
        s += 1
        r -= 1
    elif step == 's':
        s -= 1
        r += 1
    elif step == 'nw':
        q -= 1
        s += 1
    elif step == 'sw':
        q -= 1
        r += 1
    elif step == 'ne':
        q += 1
        r -= 1
    elif step == 'se':
        q += 1
        s -= 1
    #print(step, (q, r, s))
    maxdistance = max(maxdistance, hexdistance(q, r, s))
print(hexdistance(q, r, s))
print(maxdistance)
