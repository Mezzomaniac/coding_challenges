from downloader import download

download(2017, 12)
with open('aoc2017_12input.txt') as inputfile:
    data = inputfile.read()
#print(data)

test = '''0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5'''
#data = test

programs = [[int(n) for n in line.replace(',', '').split()[2:]] for line in data.splitlines()]

def n_group(n, group=None):
    if group is None:
        group = {n}
    #print(n, programs[n])
    for program in programs[n]:
        if program not in group:
            group.add(program)
            group.update(n_group(program, group))
    return group

print(len(n_group(0)))

grouped = set()
groups = 0
for program in range(len(programs)):
    if program not in grouped:
        grouped.update(n_group(program))
        groups += 1
print(groups)
