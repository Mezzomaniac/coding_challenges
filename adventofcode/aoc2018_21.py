data = '''seti 123 0 3
bani 3 456 3
eqri 3 72 3
addr 3 4 4
seti 0 0 4
seti 0 2 3
bori 3 65536 2
seti 1397714 1 3
bani 2 255 5
addr 3 5 3
bani 3 16777215 3
muli 3 65899 3
bani 3 16777215 3
gtir 256 2 5
addr 5 4 4
addi 4 1 4
seti 27 6 4
seti 0 6 5
addi 5 1 1
muli 1 256 1
gtrr 1 2 1
addr 1 4 4
addi 4 1 4
seti 25 2 4
addi 5 1 5
seti 17 0 4
setr 5 7 2
seti 7 4 4
eqrr 3 0 5
addr 5 4 4
seti 5 8 4'''

import matplotlib
import matplotlib.pyplot as plt

from aoc2018_16 import *

instructions = [[eval(line.split()[0]), int(line.split()[1]), int(line.split()[2]), int(line.split()[3])] for line in data.splitlines()]
#print(len(instructions))  # 31

'''r = 0
try:
    registers = [r, 0, 0, 0, 0, 0]
    #executed = 0
    halts = []
    while True:
        print(registers)
        if registers[4] == 30:
            if registers[3] in halts:
                print(registers[3])
            #else:
                #print(f'{registers[3]}')
            halts.append(registers[3])
            #print(max(halts))
            #print(min(halts))
            #print()
        instruction = instructions[registers[4]]
        #print(instruction)
        registers = instruction[0](registers, instruction[1:])
        #executed += 1
        registers[4] += 1
except IndexError:
    print(registers)
except KeyboardInterrupt:
    print(halts)
    #fig, ax = plt.subplots()
    #ax.plot(halts)
    #plt.show()'''

# <16744756, >204067

'''a = 3909249
b = 0
c = 65536 #6
d = 1397714 #7
f = 0
while True:
    print(a,b,c,d,f)
    f = c & 255 #8
    print(a,b,c,d,f)
    d += f #9
    print(a,b,c,d,f)
    d &= 16777215 #10
    print(a,b,c,d,f)
    d *= 65899 #11
    print(a,b,c,d,f)
    d &= 16777215 #12
    print(a,b,c,d,f)
    if 256 > c: #13-14,16
        if a == d: #28
            break #29
        else: #30
            c = d | 65536 #6
            print(a,b,c,d,f)
            d = 1397714 #7
            print(a,b,c,d,f)
    else: #15
        print(a,b,c,d,f)
        f = 0 #17
        while True: #25
            print(a,b,c,d,f)
            b = f + 1 #18
            print(a,b,c,d,f)
            b *= 256 #19
            print(a,b,c,d,f)
            b = int(b > c) #20
            print(a,b,c,d,f)
            if b: #21,23
                c = f #26
                print(a,b,c,d,f)
                break #27
            else: #22
                f += 1 #24
                print(a,b,c,d,f)'''

a = 0
b = 0
c = 65536 #6
d = 1397714 #7
halts = []
while True:
    #print(a,b,c,d)
    d += c & 255 #8-9
    #print(a,b,c,d)
    d &= 16777215 #10
    #print(a,b,c,d)
    d *= 65899 #11
    #print(a,b,c,d)
    d &= 16777215 #12
    #print(a,b,c,d)
    if 256 > c: #13-14,16
        if d in halts:
            print(halts[-1])
            break
        halts.append(d)
        if a == d: #28
            break #29
        else: #30
            c = d | 65536 #6
            #print(a,b,c,d)
            d = 1397714 #7
            #print(a,b,c,d)
    else: #15
        #print(a,b,c,d)
        b = 1 #17
        #print(a,b,c,d)
        while True: #25
            if b * 256 > c: #21,23
                c = b - 1 #26
                #print(a,b,c,d)
                break #27
            else: #22
                b += 1 #24
                #print(a,b,c,d)
