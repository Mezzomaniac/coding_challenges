data = '''Al => ThF
Al => ThRnFAr
B => BCa
B => TiB
B => TiRnFAr
Ca => CaCa
Ca => PB
Ca => PRnFAr
Ca => SiRnFYFAr
Ca => SiRnMgAr
Ca => SiTh
F => CaF
F => PMg
F => SiAl
H => CRnAlAr
H => CRnFYFYFAr
H => CRnFYMgAr
H => CRnMgYFAr
H => HCa
H => NRnFYFAr
H => NRnMgAr
H => NTh
H => OB
H => ORnFAr
Mg => BF
Mg => TiMg
N => CRnFAr
N => HSi
O => CRnFYFAr
O => CRnMgAr
O => HP
O => NRnFAr
O => OTi
P => CaP
P => PTi
P => SiRnFAr
Si => CaSi
Th => ThCa
Ti => BP
Ti => TiTi
e => HF
e => NAl
e => OMg'''

GOAL = 'CRnCaCaCaSiRnBPTiMgArSiRnSiRnMgArSiRnCaFArTiTiBSiThFYCaFArCaCaSiThCaPBSiThSiThCaCaPTiRnPBSiThRnFArArCaCaSiThCaSiThSiRnMgArCaPTiBPRnFArSiThCaSiRnFArBCaSiRnCaPRnFArPMgYCaFArCaPTiTiTiBPBSiThCaPTiBPBSiRnFArBPBSiRnCaFArBPRnSiRnFArRnSiRnBFArCaFArCaCaCaSiThSiThCaCaPBPTiTiRnFArCaPTiBSiAlArPBCaCaCaCaCaSiRnMgArCaSiThFArThCaSiThCaSiRnCaFYCaSiRnFYFArFArCaSiRnFYFArCaSiRnBPMgArSiThPRnFArCaSiRnFArTiRnSiRnFYFArCaSiRnBFArCaSiRnTiMgArSiThCaSiThCaFArPRnFArSiRnFArTiTiTiTiBCaCaSiRnCaCaFYFArSiThCaPTiBPTiBCaSiThSiRnMgArCaF'

from collections import defaultdict
from difflib import SequenceMatcher
from functools import lru_cache
from queue import PriorityQueue
import re

rules = [line.split(' => ') for line in data.splitlines()]
#print(rules)

reverse_rules = [line.split(' => ')[::-1] for line in data.splitlines()]
#print(reverse_rules)
#print(len(reverse_rules) == len(rules))

START = 'e'

rules = reverse_rules
START, GOAL = GOAL, START

#@lru_cache(maxsize=1024)
def neighbors(molecule):
    molecules = set()
    for atom, repl in rules:
        for instance in re.finditer(atom, molecule):
            start, end = instance.span()
            molecules.add(molecule[:start] + repl + molecule[end:])
    return molecules
print(len(neighbors(GOAL)))

sequence_matcher = SequenceMatcher(b=GOAL, autojunk=False)
#@lru_cache(maxsize=1024)
def heuristic(molecule):
    sequence_matcher.set_seq1(molecule)
    ratio = sequence_matcher.real_quick_ratio()
    print(ratio)
    return ratio# or .001

frontier = PriorityQueue()
start = START
cost = 0
cost_so_far = {start: cost}
#priority = cost / heuristic(start)
priority = (-heuristic(start), cost)
frontier.put((priority, start))
while not frontier.empty():
    current = frontier.get()[1]
    if current == GOAL:
        print(cost_so_far[current])
        break
    for next in neighbors(current):
        cost = cost_so_far[current] + 1
        if next not in cost_so_far or cost < cost_so_far[next]:
            cost_so_far[next] = cost
            #priority = cost / heuristic(next)
            priority = (-heuristic(next), cost)
            frontier.put((priority, next))
