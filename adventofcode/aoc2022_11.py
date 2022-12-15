from downloader import download
from collections import deque#, Counter
from functools import reduce
#from math import sqrt
from operator import mul

download(2022, 11)
with open('aoc2022_11input.txt') as inputfile:
    data = inputfile.read()

test = '''Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1'''
#data = test
print(data)

class Monkey:
    
    def __init__(self, id):
        self.id = id
        self.inspections = 0
    
    def __repr__(self):
        return f'Monkey({self.items} {self.inspections})'

"""class Item:
    
    def __init__(self, value):
        self.value = int(value)
        self.inspected_by = []
    
    def __repr__(self):
        return f'Item({self.value})'"""

'''def factor(n):
    factors = set()
    for i in range(1, round(sqrt(n)) + 1):
        result = n // i
        if result * i == n:
            factors.add(i)
            factors.add(result)
    return factors'''

monkeys = []
for monkey_data in data.split('\n\n'):
    lines = monkey_data.splitlines()
    monkey = Monkey(lines[0][-2])
    monkey.items = deque([int(item) for item in lines[1].split(': ')[1].split(', ')])
    #monkey.items = deque([Item(item) for item in lines[1].split(': ')[1].split(', ')])
    #monkey.items = deque([factor(int(item)) for item in lines[1].split(': ')[1].split(', ')])
    exec(f'monkey.op = lambda old: {lines[2].split("= ")[1]}')
    #monkey.op = lines[2].split("= ")[1].split()[1:]
    monkey.test = int(lines[3].split()[-1])
    monkey.throw = (int(lines[4].split()[-1]), int(lines[5].split()[-1]))
    monkeys.append(monkey)
print(monkeys)

modulo = reduce(mul, (monkey.test for monkey in monkeys))
print(modulo)

#busiest_monkeys = Counter()
#last_monkey_business = 0
#for round_ in range(20):
for round_ in range(10000):
    #last_inspections = [monkey.inspections for monkey in monkeys]
    #print(round_)
    for monkey in monkeys:
        #print(monkey.op, monkey.test, monkey.throw)
        while monkey.items:
            item = monkey.items.popleft()
            #print(item)
            monkey.inspections += 1
            #item = monkey.op(item) // 3
            item = monkey.op(item) % modulo
            #item.value = monkey.op(item.value)
            '''if monkey.op[0] == '*' and monkey.op[1].isdigit():
                item.add(int(monkey.op[1]))
            elif monkey.op[0] == '+':
                item = factor(max(item) + int(monkey.op[1]))
            print(item)'''
            #item.inspected_by.append(monkey.id)
            catcher = monkey.throw[bool(item % monkey.test)]
            #catcher = monkey.throw[bool(item.value % monkey.test)]
            #catcher = monkey.throw[monkey.test not in item]
            #print(catcher)
            monkeys[catcher].items.append(item)
            #print(monkeys)
        #print()
    #print('\n\n')
    #current_inspections = [monkey.inspections for monkey in monkeys]
    #print([current - last for current, last in zip(current_inspections, last_inspections)], sum(current_inspections), sum(last_inspections), sum(current_inspections) - sum(last_inspections))
activity = sorted(monkeys, key=lambda monkey: monkey.inspections)
monkey_business = activity[-1].inspections * activity[-2].inspections
print(monkey_business)
    #busiest_monkeys.update(monkey.id for monkey in activity[-2:])
    #print(sorted(busiest_monkeys.items()))
    #print(monkey_business, monkey_business - last_monkey_business, monkey_business / last_monkey_business if last_monkey_business else '')
    #last_monkey_business = monkey_business
    #print([''.join(item.inspected_by) for monkey in monkeys for item in monkey.items])
    #print()
