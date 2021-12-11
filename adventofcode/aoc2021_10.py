from downloader import download
from statistics import median

download(2021, 10)
with open('aoc2021_10input.txt') as inputfile:
    data = inputfile.read().splitlines()

test = '''[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]'''.splitlines()
#data = test

print(data)

pairs = dict(zip(')]}>', '([{<'))
inverse_pairs = dict(zip(pairs.values(), pairs.keys()))
syntax_points_table = dict(zip(pairs.keys(), (3, 57, 1197, 25137)))
syntax_score = 0
autocomplete_points_table = dict(zip(pairs.keys(), (1, 2, 3, 4)))
autocomplete_scores = []
for line in data:
    stack = []
    for char in line:
        if char in pairs.values():
            stack.append(char)
        elif stack[-1] == pairs[char]:
            stack.pop()
        else:
            syntax_score += syntax_points_table[char]
            break
    else:
        autocomplete_score = 0
        for char in reversed(stack):
            autocomplete_score *= 5
            autocomplete_score += autocomplete_points_table[inverse_pairs[char]]
        autocomplete_scores.append(autocomplete_score)

print(syntax_score)
print(median(autocomplete_scores))
