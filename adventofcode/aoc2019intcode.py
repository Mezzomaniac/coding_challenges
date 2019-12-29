from collections import deque
import copy
from operator import add, mul, lt, eq

class StopIntcodeRun(Exception):
    pass

class Intcode:
    def __init__(self, memory):
        if not isinstance(memory, Memory):
            self.memory = Memory(memory)
        else:
            self.memory = memory
        self.pointer = 0
        self.relative_base = 0

    def run(self, inputs=None, *, inspect=False):
        self.run_setup()
        self.inputs = self.input_setup(inputs)
        self.outputs = self.output_setup()
        num_parameters = {1: 3, 2: 3, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3, 9: 1, 99: 0}
        while True:
            code = str(self.memory[self.pointer])
            opcode = int(code[-2:])
            parameter_modes = code[-3::-1].ljust(num_parameters[opcode], '0')
            parameter_addresses = []
            for n, parameter_mode in enumerate(parameter_modes, 1):
                if parameter_mode == '0':
                    address = self.memory[self.pointer + n]
                elif parameter_mode == '1':
                    address = self.pointer + n
                else:
                    address = self.memory[self.pointer + n] + self.relative_base
                parameter_addresses.append(address)
            if inspect:
                print(self.memory[self.pointer: self.pointer + num_parameters[opcode] + 1], opcode, parameter_modes, parameter_addresses, self.inputs, self.outputs)
                #print(self.memory)
                print()
            if opcode == 99:
                halt_result = self.halt_action()
                return halt_result
            elif opcode in (1, 2, 7, 8):
                ops = {1: add, 2: mul, 7: lt, 8: eq}
                op = ops[opcode]
                self.memory[parameter_addresses[2]] = int(op(self.memory[parameter_addresses[0]], self.memory[parameter_addresses[1]]))
                self.pointer += 4
            elif opcode == 3:
                try:
                    self.memory[parameter_addresses[0]] = self.input_action()
                except StopIntcodeRun:
                    return self.outputs
                self.pointer += 2
            elif opcode == 4:
                output = self.memory[parameter_addresses[0]]
                self.output_action(output)
                self.pointer += 2
            elif opcode in range(5, 7):
                parameter1 = self.memory[parameter_addresses[0]]
                if (opcode == 5 and parameter1 != 0) or (opcode == 6 and parameter1 == 0):
                    self.pointer = self.memory[parameter_addresses[1]]
                else:
                    self.pointer += 3
            elif opcode == 9:
                self.relative_base += self.memory[parameter_addresses[0]]
                self.pointer += 2
            else:
                raise ValueError
    
    def run_setup(self):
        pass
    
    def input_setup(self, inputs):
        try:
            return deque(inputs)
        except TypeError:
            return inputs
    
    def output_setup(self):
        return []
    
    def input_action(self):
        return self.inputs.popleft()
    
    def output_action(self, output):
        self.outputs.append(output)
    
    def halt_action(self):
        return self.outputs
    
    def from_ascii(self, instructions):
        return [ord(c) for c in instructions]
    
    def to_ascii(self, outputs):
        value = None
        str_list = []
        for output in outputs:
            try:
                str_list.append(chr(output))
            except ValueError:
                value = output
        #str_list = [chr(output) for output in outputs]
        string = ''.join(str_list).strip()
        if value is None:
            return string
        return (string, value)

class Memory:
    def __init__(self, memory):
        self.memory = memory
        self.extra_memory = {}
    
    def __getitem__(self, key):
        try:
            return self.memory[key]
        except IndexError:
            return self.extra_memory.get(key, 0)

    def __setitem__(self, key, value):
        try:
            self.memory[key] = value
        except IndexError:
            self.extra_memory[key] = value
    
    def __repr__(self):
        return f'Memory({self.memory}, {self.extra_memory})'
    
    def copy(self):
        return copy.deepcopy(self)
