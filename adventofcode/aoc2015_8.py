total_code_chars = 0
total_eval_chars = 0
total_reencoded_chars = 0
new_chars = 0

with open('aoc2015-8.txt') as file:
    for line in file:
        line = line[:-1]
        print(line)
        print(eval(line))
        code_chars = len(line)
        eval_chars = len(eval(line))
        print(code_chars)
        print(eval_chars)
        total_code_chars += code_chars
        total_eval_chars += eval_chars
        new_chars += sum((line.count("\""), line.count("\\"), 2))

print(total_code_chars - total_eval_chars)
print(new_chars)
