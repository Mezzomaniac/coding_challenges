from downloader import download
from collections import deque

download(2022, 11)
with open('aoc2022_11input.txt') as inputfile:
    data = inputfile.read()
print(data)

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

class Monkey:
    
    def __init__(self):
        self.inspections = 0
    
    def __repr__(self):
        return f'Monkey({self.items} {self.inspections})'

monkeys = []
for monkey_data in data.split('\n\n'):
    lines = monkey_data.splitlines()
    monkey = Monkey()
    monkey.items = deque([int(item) for item in lines[1].split(': ')[1].split(', ')])
    exec(f'monkey.op = lambda old: {lines[2].split("= ")[1]}')
    monkey.test = int(lines[3].split()[-1])
    monkey.throw = (int(lines[4].split()[-1]), int(lines[5].split()[-1]))
    monkeys.append(monkey)
print(monkeys)

last_monkey_business = 0
for round in range(10000):
    last_inspections = [monkey.inspections for monkey in monkeys]
    print(round)
    for monkey in monkeys:
        while monkey.items:
            item = monkey.items.popleft()
            monkey.inspections += 1
            item = monkey.op(item)# // 3
            catcher = monkey.throw[bool(item % monkey.test)]
            monkeys[catcher].items.append(item)
    current_inspections = [monkey.inspections for monkey in monkeys]
    #print([current - last for current, last in zip(current_inspections, last_inspections)])
    activity = sorted(monkeys, key=lambda monkey: monkey.inspections)
    monkey_business = activity[-1].inspections * activity[-2].inspections
    print(monkey_business, monkey_business - last_monkey_business, monkey_business / last_monkey_business if last_monkey_business else '')
    last_monkey_business = monkey_business
