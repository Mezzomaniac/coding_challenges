from downloader import download

download(2023, 19)
with open('aoc2023_19input.txt') as inputfile:
    data = inputfile.read()
test_data = '''px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}'''
#data = test_data
print(data)

from collections import namedtuple
from copy import copy
from dataclasses import dataclass, astuple
from functools import reduce
from operator import lt, gt, mul

ops = {'<': lt, '>': gt}

@dataclass
class Rule:
    destination: str
    category: str|None=None
    op: str|None=None
    value: int|None=None
    
    def apply(self, part: tuple):
        if not self.category or ops[self.op](getattr(part, self.category), self.value):
            return self.destination

Part = namedtuple('Part', 'x m a s')

workflows_data, parts_data = data.split('\n\n')

workflows = {}
for line in workflows_data.splitlines():
    name, rules_data = line[:-1].split('{')
    rules = []
    for rule in rules_data.split(','):
        if ':' not in rule:
            rules.append(Rule(rule))
            continue
        condition, destination = rule.split(':')
        rules.append(Rule(destination, condition[0], condition[1], int(condition[2:])))
    workflows[name] = rules

parts = [Part(*[int(category[2:]) for category in line[1:-1].split(',')]) for line in parts_data.splitlines()]

accepted_total = 0
for part in parts:
    name = 'in'
    while name not in 'AR':
        workflow = workflows[name]
        for rule in workflow:
            if name := rule.apply(part):
                break
    if name == 'A':
        accepted_total += sum(part)
print(accepted_total)

@dataclass
class PartRanges:
     xmin: int
     xmax: int
     mmin: int
     mmax: int
     amin: int
     amax: int
     smin: int
     smax: int

def explore_workflow(name, part_ranges):
    acceptable_parts = 0
    if name == 'A':
        #print('\n', name, part_ranges)
        acceptable_parts += reduce(mul, (category_max - category_min + 1 for category_min, category_max in zip(astuple(part_ranges)[::2], astuple(part_ranges)[1::2])))
    elif name != 'R':
        for rule in workflows[name]:
            #print('\n', name, part_ranges, rule)
            if not rule.category:
                acceptable_parts += explore_workflow(rule.destination, part_ranges)
            else:
                selected_part_ranges = copy(part_ranges)
                category_min, category_max = getattr(part_ranges, f'{rule.category}min'), getattr(part_ranges, f'{rule.category}max')
                if rule.op == '<':
                    setattr(selected_part_ranges, f'{rule.category}max', min(getattr(part_ranges, f'{rule.category}max'), rule.value - 1))
                    setattr(part_ranges, f'{rule.category}min', max(getattr(part_ranges, f'{rule.category}min'), rule.value))
                else:
                    setattr(selected_part_ranges, f'{rule.category}min', max(getattr(part_ranges, f'{rule.category}min'), rule.value + 1))
                    setattr(part_ranges, f'{rule.category}max', min(getattr(part_ranges, f'{rule.category}max'), rule.value))
                acceptable_parts += explore_workflow(rule.destination, selected_part_ranges)
    return acceptable_parts

print(explore_workflow('in', PartRanges(*[1, 4000] * 4)))
