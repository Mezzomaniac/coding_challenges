from downloader import download

download(2022, 21)
with open('aoc2022_21input.txt') as inputfile:
    data = inputfile.read()
test = '''root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32'''
#data = test
print(data)

monkeys = {}
for line in data.splitlines():
    monkey, job = line.split(': ')
    try:
        job = int(job)
    except ValueError:
        pass
    monkeys[monkey] = job

def solve(monkeys, monkey):
    job = monkeys[monkey]
    if isinstance(job, int):
        return job
    operand1, operator, operand2 = job.split()
    solution = int(eval(f'{solve(monkeys, operand1)} {operator} {solve(monkeys, operand2)}'))
    monkeys[monkey] = solution
    return solution
print(solve(monkeys.copy(), 'root'))

def generate_equation(monkeys, monkey):
    job = monkeys[monkey]
    if isinstance(job, int):
        return job
    operand1, operator, operand2 = job.split()
    operand_solutions = []
    for operand in (operand1, operand2):
        try:
            operand_solution = generate_equation(monkeys, operand)
        except AttributeError:
            operand_solution = operand
        operand_solutions.append(operand_solution)
    equation = f'({operand_solutions[0]} {operator} {operand_solutions[1]})'
    try:
        monkeys[monkey] = eval(equation)
    except NameError:
        monkeys[monkey] = equation
    return monkeys[monkey]

reverse_operators = {'+': '-', '-': '+', '*': '/', '/': '*'}

def solve_equation(left, right):
    left = left[1:-1]
    if left.startswith('('):
        split = left.rindex(')') + 1
        left, operator, operand = left[:split], left[split + 1], left[split + 3:]
        right = eval(f'{right} {reverse_operators[operator]} {operand}')
    elif left.endswith(')'):
        split = left.index('(')
        operand, operator, left = left[:split - 3], left[split - 2], left[split:]
        if operator in '+*':
            right = eval(f'{right} {reverse_operators[operator]} {operand}')
        else:
            right = eval(f'{operand} {operator} {right}')
    else:
        left, operator, operand = left.split()
        right = eval(f'{right} {reverse_operators[operator]} {operand}')
        return right
    return solve_equation(left, right)

monkeys['root'] = monkeys['root'].replace('+', '==')
monkeys['humn'] = None
equation = generate_equation(monkeys.copy(), 'root').replace('.0', '')[1:-1]
print(equation)
print(solve_equation(*equation.split(' == ')))

