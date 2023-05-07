from downloader import download
from collections import defaultdict
from math import sqrt

download(2017, 23)
with open('aoc2017_23input.txt') as inputfile:
    data = inputfile.read()
print(data)

instructions = data.splitlines()

registers = defaultdict(int)
registers['a'] = 1
#registers.update(zip('abcdefgh', [1, 126300, 126300, 126290, 126300, 0, -10, 999]))
#23 jnz g -13 [1, 126300, 126300, 22, 126300, 0, -126278, 1000]
index = 0
muls = 0
while index in range(len(instructions)):
    break
    #if index == 19:
        #print(registers)
    #if index not in range(11, 20):
        #print('\t', index)
    #else:
        #print(index)
    instruction = instructions[index].split()
    print([value for register, value in sorted(registers.items())], index, ' '.join(instruction))
    command = instruction[0]
    match command:
        case 'set':
            if instruction[2].isalpha():
                registers[instruction[1]] = registers[instruction[2]]
            else:
                registers[instruction[1]] = int(instruction[2])
        case 'sub':
            if instruction[2].isalpha():
                registers[instruction[1]] -= registers[instruction[2]]
            else:
                registers[instruction[1]] -= int(instruction[2])
            if instruction[1] == 'h':
                print(registers['h'])
        case 'mul':
            muls += 1
            if instruction[2].isalpha():
                registers[instruction[1]] *= registers[instruction[2]]
            else:
                registers[instruction[1]] *= int(instruction[2])
        case 'jnz':
            if instruction[1].isalpha():
                check = registers[instruction[1]]
            else:
                check = int(instruction[1])
            #if registers['d'] > 2:
            #if index > 22:
                #print(index, ' '.join(instruction), [value for register, value in sorted(registers.items())])
            if check:
                if instruction[2].isalpha():
                    index += registers[instruction[2]]
                else:
                    index += int(instruction[2])
                continue
    index += 1
print(muls)
#print(registers['h'])

'''registers.update(zip('abcdefgh', [1, 109300, 126300, 2, 3, 1, -109297, 0]))
while registers['g']:
    while registers['g']:
        if not registers['f']:
            registers['h'] += 1
        while registers['g']:
            # increment d until it == b
            registers['e'] = 2
            while registers['g']:
                # increment e until it == b
                registers['g'] = registers['d'] * registers['e'] - registers['b']
                if not registers['g']:
                    # when d * e == b
                    registers['f'] = 0
                    #print('f')
                    print([value for register, value in sorted(registers.items())])
                registers['e'] -= -1
                registers['g'] = registers['e'] - registers['b']
                #print([value for register, value in sorted(registers.items())])
            #print([value for register, value in sorted(registers.items())])
            registers['d'] -= -1
            registers['g'] = registers['d'] - registers['b']
        print([value for register, value in sorted(registers.items())])
        registers['g'] = registers['b'] - registers['c']
    registers['b'] -= -17
print([value for register, value in sorted(registers.items())])'''


def composite(n):
    for i in range(2, int(sqrt(n)) + 1):
        if not n % i:
            return True
    return False

answer = sum(composite(b) for b in range(109300, 126301, 17))
print(answer)
