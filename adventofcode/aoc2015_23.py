data = '''jio a, +16
inc a
inc a
tpl a
tpl a
tpl a
inc a
inc a
tpl a
inc a
inc a
tpl a
tpl a
tpl a
inc a
jmp +23
tpl a
inc a
inc a
tpl a
inc a
inc a
tpl a
tpl a
inc a
inc a
tpl a
inc a
tpl a
inc a
tpl a
inc a
inc a
tpl a
inc a
tpl a
tpl a
inc a
jio a, +8
inc b
jie a, +4
tpl a
inc a
jmp +2
hlf a
jmp -7'''

instructions = data.splitlines()

registers = {'a': 1, 'b': 0}
index = 0
while True:
    try:
        instruction = instructions[index].split()
    except IndexError:
        print(registers['b'])
        break
    command, operands = instruction[0], instruction[1:]
    if command == 'hlf':
        registers[operands[0]] //= 2
        index += 1
    elif command == 'tpl':
        registers[operands[0]] *= 3
        index += 1
    elif command == 'inc':
        registers[operands[0]] += 1
        index += 1
    elif command == 'jmp':
        index += int(operands[0])
    elif command == 'jie':
        r, offset = operands
        if not registers[r[0]] % 2:
            index += int(offset)
        else:
            index += 1
    elif command == 'jio':
        r, offset = operands
        if registers[r[0]] == 1:
            index += int(offset)
        else:
            index += 1
    else:
        raise RuntimeError
