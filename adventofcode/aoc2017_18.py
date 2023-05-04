from downloader import download
from collections import defaultdict
import asyncio

download(2017, 18)
with open('aoc2017_18input.txt') as inputfile:
    data = inputfile.read()
print(data)

test = '''snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d'''
#data = test

instructions = data.splitlines()

registers = defaultdict(int)
sounds = []
index = 0
while index in range(len(instructions)):
    #print(list(registers.items()), sounds, index, instructions[index])
    instruction = instructions[index].split()
    command = instruction[0]
    match command:
        case 'snd':
            sounds.append(registers[instruction[1]])
        case 'set':
            if instruction[2].isalpha():
                registers[instruction[1]] = registers[instruction[2]]
            else:
                registers[instruction[1]] = int(instruction[2])
        case 'add':
            if instruction[2].isalpha():
                registers[instruction[1]] += registers[instruction[2]]
            else:
                registers[instruction[1]] += int(instruction[2])
        case 'mul':
            if instruction[2].isalpha():
                registers[instruction[1]] *= registers[instruction[2]]
            else:
                registers[instruction[1]] *= int(instruction[2])
        case 'mod':
            if instruction[2].isalpha():
                registers[instruction[1]] %= registers[instruction[2]]
            else:
                registers[instruction[1]] %= int(instruction[2])
        case 'rcv':
            if registers[instruction[1]]:
                print(sounds[-1])
                break
        case 'jgz':
            if instruction[1].isalpha():
                check = registers[instruction[1]]
            else:
                check = int(instruction[1])
            if check > 0:
                if instruction[2].isalpha():
                    index += registers[instruction[2]]
                else:
                    index += int(instruction[2])
                continue
    index += 1

print()


async def program(id, this_queue, other_queue):
    try:
        sent_count = 0
        registers = defaultdict(int)
        registers['p'] = id
        index = 0
        while index in range(len(instructions)):
            instruction = instructions[index].split()
            command = instruction[0]
            match command:
                case 'snd':
                    await other_queue.put(registers[instruction[1]])
                    if id == 1:
                        sent_count += 1
                        if not sent_count % 1000:
                            print(sent_count)
                case 'set':
                    if instruction[2].isalpha():
                        registers[instruction[1]] = registers[instruction[2]]
                    else:
                        registers[instruction[1]] = int(instruction[2])
                case 'add':
                    if instruction[2].isalpha():
                        registers[instruction[1]] += registers[instruction[2]]
                    else:
                        registers[instruction[1]] += int(instruction[2])
                case 'mul':
                    if instruction[2].isalpha():
                        registers[instruction[1]] *= registers[instruction[2]]
                    else:
                        registers[instruction[1]] *= int(instruction[2])
                case 'mod':
                    if instruction[2].isalpha():
                        registers[instruction[1]] %= registers[instruction[2]]
                    else:
                        registers[instruction[1]] %= int(instruction[2])
                case 'rcv':
                    received = await this_queue.get()
                    registers[instruction[1]] = received
                case 'jgz':
                    if instruction[1].isalpha():
                        check = registers[instruction[1]]
                    else:
                        check = int(instruction[1])
                    if check > 0:
                        if instruction[2].isalpha():
                            index += registers[instruction[2]]
                        else:
                            index += int(instruction[2])
                        continue
            index += 1
    except asyncio.CancelledError:
        return sent_count
    return sent_count

async def main():
    queues = [asyncio.Queue(), asyncio.Queue()]
    tasks = [asyncio.create_task(p) for p in [program(0, queues[0], queues[1]), program(1, queues[1], queues[0])]]
    
    done, pending = await asyncio.wait(tasks, timeout=2)
    for task in pending:
        task.cancel()
        await task
    return max(task.result() for task in done | pending)
        
result = asyncio.run(main())
print(result)
