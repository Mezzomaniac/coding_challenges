memory = '3,8,1005,8,361,1106,0,11,0,0,0,104,1,104,0,3,8,102,-1,8,10,101,1,10,10,4,10,108,0,8,10,4,10,1001,8,0,28,2,1104,18,10,1006,0,65,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,1001,8,0,57,1,1101,5,10,2,108,15,10,2,102,12,10,3,8,1002,8,-1,10,101,1,10,10,4,10,108,0,8,10,4,10,102,1,8,91,2,1005,4,10,2,1107,10,10,1006,0,16,2,109,19,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,129,1,104,3,10,1,1008,9,10,1006,0,65,1,104,5,10,3,8,1002,8,-1,10,101,1,10,10,4,10,108,1,8,10,4,10,102,1,8,165,1,1106,11,10,1,1106,18,10,1,8,11,10,1,4,11,10,3,8,1002,8,-1,10,101,1,10,10,4,10,108,1,8,10,4,10,1001,8,0,203,2,1003,11,10,1,1105,13,10,1,101,13,10,3,8,102,-1,8,10,101,1,10,10,4,10,108,0,8,10,4,10,101,0,8,237,2,7,4,10,1006,0,73,1,1003,7,10,1006,0,44,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,101,0,8,273,2,108,14,10,3,8,102,-1,8,10,101,1,10,10,4,10,108,0,8,10,4,10,102,1,8,299,1,1107,6,10,1006,0,85,1,1107,20,10,1,1008,18,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,0,10,4,10,1001,8,0,337,2,107,18,10,101,1,9,9,1007,9,951,10,1005,10,15,99,109,683,104,0,104,1,21102,1,825594852248,1,21101,378,0,0,1105,1,482,21101,0,387240006552,1,21101,0,389,0,1106,0,482,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21101,0,29032025091,1,21101,436,0,0,1106,0,482,21101,29033143299,0,1,21102,1,447,0,1105,1,482,3,10,104,0,104,0,3,10,104,0,104,0,21101,988669698916,0,1,21101,0,470,0,1106,0,482,21101,0,709052072804,1,21102,1,481,0,1106,0,482,99,109,2,21202,-1,1,1,21101,0,40,2,21101,0,513,3,21101,503,0,0,1106,0,546,109,-2,2105,1,0,0,1,0,0,1,109,2,3,10,204,-1,1001,508,509,524,4,0,1001,508,1,508,108,4,508,10,1006,10,540,1101,0,0,508,109,-2,2105,1,0,0,109,4,1202,-1,1,545,1207,-3,0,10,1006,10,563,21102,0,1,-3,21202,-3,1,1,22101,0,-2,2,21102,1,1,3,21101,582,0,0,1105,1,587,109,-4,2106,0,0,109,5,1207,-3,1,10,1006,10,610,2207,-4,-2,10,1006,10,610,21202,-4,1,-4,1106,0,678,22102,1,-4,1,21201,-3,-1,2,21202,-2,2,3,21102,629,1,0,1106,0,587,22102,1,1,-4,21101,0,1,-1,2207,-4,-2,10,1006,10,648,21102,0,1,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,670,21202,-1,1,1,21101,670,0,0,105,1,545,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2106,0,0'

from operator import add, mul, lt, eq
from enum import Enum
import aoc2019_9

class Direction(Enum):
    UP = (-1, 0), (1, 0)
    RIGHT = (0, -1), (0, 1)
    DOWN = (1, 0), (-1, 0)
    LEFT = (0, 1), (0, -1)
DIRECTIONS = list(Direction)

class Robot:
    def __init__(self, memory, position:tuple, direction:Direction):
        self.memory = aoc2019_9.Memory(memory)
        self.pos = position
        self.dir = direction
    
    def move(self, direction:int):
        self.pos = (self.pos[0] + self.dir.value[direction][0], self.pos[1] + self.dir.value[direction][1])
        new_dir_index = (DIRECTIONS.index(self.dir) + (-1, 1)[direction]) % 4
        self.dir = DIRECTIONS[new_dir_index]

    def run(self):
        memory = self.memory
        num_parameters = {1: 3, 2: 3, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3, 9: 1, 99: 0}
        relative_base = 0
        output_is_color = True
        i = 0
        while True:
            code = str(memory[i])
            opcode = int(code[-2:])
            parameter_modes = code[-3::-1].ljust(num_parameters[opcode], '0')
            parameter_addresses = []
            for n, parameter_mode in enumerate(parameter_modes, 1):
                if parameter_mode == '0':
                    address = memory[i + n]
                elif parameter_mode == '1':
                    address = i + n
                else:
                    address = memory[i + n] + relative_base
                parameter_addresses.append(address)
            if opcode == 99:
                return
            elif opcode in (1, 2, 7, 8):
                ops = {1: add, 2: mul, 7: lt, 8: eq}
                op = ops[opcode]
                memory[parameter_addresses[2]] = int(op(memory[parameter_addresses[0]], memory[parameter_addresses[1]]))
                i += 4
            elif opcode == 3:
                memory[parameter_addresses[0]] = grid.get(self.pos, 0)
                i += 2
            elif opcode == 4:
                output = memory[parameter_addresses[0]]
                if output_is_color:
                    grid[self.pos] = str(output)
                else:
                    self.move(output)
                output_is_color = not output_is_color
                i += 2
            elif opcode in range(5, 7):
                parameter1 = memory[parameter_addresses[0]]
                if (opcode == 5 and parameter1 != 0) or (opcode == 6 and parameter1 == 0):
                    i = memory[parameter_addresses[1]]
                else:
                    i += 3
            elif opcode == 9:
                relative_base += memory[parameter_addresses[0]]
                i += 2
            else:
                raise ValueError

grid = {(0, 0): 1}
memory = [int(i) for i in memory.split(',')]
robot = Robot(memory, (0, 0), Direction.UP)
robot.run()
#print(len(grid))

xs = [x for x, y in grid.keys()]
minx = min(xs)
maxx = max(xs)
ys = [y for x, y in grid.keys()]
miny = min(ys)
maxy = max(ys)
print(minx, maxx, miny, maxy)

image = [['⬛️' for x in range(maxx + 1)] for y in range(maxy + 1)]
for panel, color in grid.items():
    if color == '1':
        image[panel[1]][panel[0]] = '⬜️'
for row in image:
    print(''.join(row[:21]))
print()
for row in image:
    print(''.join(row[21:]))