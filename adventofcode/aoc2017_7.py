from downloader import download
from collections import Counter

download(2017, 7)
with open('aoc2017_7input.txt') as inputfile:
    data = inputfile.read()
#print(data)

test = '''pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)'''
#data = test

programs = {}
balancing = set()
for line in data.splitlines():
    parts = line.replace(',', '').split()
    programs[parts[0]] = {'weight': int(parts[1].strip('()')), 'tower': parts[3:], 'total': 0}
    balancing.update(parts[3:])
base = (set(programs) - balancing).pop()
print(base)

def calc_total(program):
    print(program, programs[program])
    if not programs[program]['tower']:
        programs[program]['total'] = programs[program]['weight']
    if programs[program]['total']:
        return programs[program]['total']
    tower_programs_weights = Counter(calc_total(balancing) for balancing in programs[program]['tower'])
    if len(tower_programs_weights) != 1:
        right_weight = tower_programs_weights.most_common()[0][0]
        wrong_weight = tower_programs_weights.most_common()[1][0]
        difference = right_weight - wrong_weight
        print(difference)
        faulty_program = set(balancing for balancing in programs[program]['tower'] if programs[balancing]['total'] == wrong_weight).pop()
        print(programs[faulty_program]['weight'] + difference)
        raise Exception()
    programs[program]['total'] = programs[program]['weight'] + sum(tower_programs_weights.elements())
    print(program, programs[program])
    print()
    return programs[program]['total']

calc_total(base)
