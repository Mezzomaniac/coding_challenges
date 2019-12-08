memory = '3,8,1001,8,10,8,105,1,0,0,21,38,55,72,93,118,199,280,361,442,99999,3,9,1001,9,2,9,1002,9,5,9,101,4,9,9,4,9,99,3,9,1002,9,3,9,1001,9,5,9,1002,9,4,9,4,9,99,3,9,101,4,9,9,1002,9,3,9,1001,9,4,9,4,9,99,3,9,1002,9,4,9,1001,9,4,9,102,5,9,9,1001,9,4,9,4,9,99,3,9,101,3,9,9,1002,9,3,9,1001,9,3,9,102,5,9,9,101,4,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,99'

from itertools import permutations
from operator import add, mul, lt, eq
from queue import Queue
import aoc2019_5

memory = [int(i) for i in memory.split(',')]

max_output = 0
for permutation in permutations(range(5)):
    output = 0
    for phase in permutation:
        inputs = [phase, output]
        output, = aoc2019_5.run(memory.copy(), inputs)
    max_output = max(max_output, output)
print(max_output)

def amp(memory, phase, index, first=False, a=False):
    memory = memory.copy()
    inputs = amps[index-1]
    setting_phase = True
    i = 0
    while True:
        code = str(memory[i])
        opcode = int(code[-2:])
        if opcode == 99:
            return
        elif opcode in (1, 2, 7, 8):
            ops = {1: add, 2: mul, 7: lt, 8: eq}
            op = ops[opcode]
            parameter_modes = code[-3::-1].ljust(2, '0')
            parameter1 = memory[i+1] if parameter_modes[0] == '1' else memory[memory[i+1]]
            parameter2 = memory[i+2] if parameter_modes[1] == '1' else memory[memory[i+2]]
            memory[memory[i+3]] = op(parameter1, parameter2)
            i += 4
        elif opcode == 3:
            if setting_phase:
                input_ = phase
                setting_phase = False
            elif first:
                input_ = 0
                first = False
                a = True
            elif a:
                input_ = e_output
            else:
                try:
                    input_ = next(inputs)
                except StopIteration:
                    #print(output)
                    return
            #print(index, 'input', input_)
            memory[memory[i+1]] = input_
            i += 2
        elif opcode == 4:
            parameter_mode = code[:-2]
            output = memory[i+1] if parameter_mode == '1' else memory[memory[i+1]]
            #print(index, 'output', output)
            yield output
            i += 2
        elif opcode in range(5, 7):
            parameter_modes = code[-3::-1].ljust(2, '0')
            parameter1 = memory[i+1] if parameter_modes[0] == '1' else memory[memory[i+1]]
            if (opcode == 5 and parameter1 != 0) or (opcode == 6 and parameter1 == 0):
                i = memory[i+2] if parameter_modes[1] == '1' else memory[memory[i+2]]
            else:
                i += 3
        else:
            raise ValueError

max_output = 0
for permutation in permutations(range(5, 10)):
    amps = [amp(memory, phase, index, first) for phase, index, first in zip(permutation, range(5), (True, False, False, False, False))]
    while True:
        try:
            e_output = next(amps[-1])
        except StopIteration:
            max_output = max(e_output, max_output)
            #print()
            break

print(max_output)