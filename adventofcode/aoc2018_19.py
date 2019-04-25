data = '''addi 5 16 5
seti 1 3 1
seti 1 1 2
mulr 1 2 4
eqrr 4 3 4
addr 4 5 5
addi 5 1 5
addr 1 0 0
addi 2 1 2
gtrr 2 3 4
addr 5 4 5
seti 2 4 5
addi 1 1 1
gtrr 1 3 4
addr 4 5 5
seti 1 5 5
mulr 5 5 5
addi 3 2 3
mulr 3 3 3
mulr 5 3 3
muli 3 11 3
addi 4 8 4
mulr 4 5 4
addi 4 13 4
addr 3 4 3
addr 5 0 5
seti 0 8 5
setr 5 3 4
mulr 4 5 4
addr 5 4 4
mulr 5 4 4
muli 4 14 4
mulr 4 5 4
addr 3 4 3
seti 0 8 0
seti 0 4 5'''

from aoc2018_16 import *

#registers = [1, 0, 0, 0, 0, 0]
registers = [422088, 422056, 10551422, 10551425, 0, 5]
#registers = [423088, 422056, 422055, 10551425, 0, 5]
instructions = [[eval(line.split()[0]), int(line.split()[1]), int(line.split()[2]), int(line.split()[3])] for line in data.splitlines()]
#print(len(instructions))
'''while True:
    print(registers)
    try:
        instruction = instructions[registers[5]]
        #print(instruction)
        registers = instruction[0](registers, instruction[1:])
    except IndexError:
        print(registers[0])
        break
    registers[5] += 1'''

a = 0
b = 0
c = 0
d = 10551425
e = 0
'''while True:
    c += 1
    e = c * b
    if e == d:
        a += b
        print(a)
    if c >= d:
        b += 1
        c = 0
    if a >= d:
        print(a, b, c, d, e)
        break'''

while True:
    b += 1
    if not d % b:
        a += b
        print(a)
    if b >= d:
        print(a, b, c, d, e)
        break
