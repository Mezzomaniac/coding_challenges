from downloader import download
from collections import Counter

download(2021, 14)
with open('aoc2021_14input.txt') as inputfile:
    data = inputfile.read()
print(data)

template0, rules = data.split('\n\n')
rules = [rule.split(' -> ') for rule in rules.splitlines()]
rules = {pair: element for pair, element in rules}

template = template0
for step in range(10):
    result = [template[0]]
    for i in range(1, len(template)):
        pair = template[i-1: i+1]
        element = rules[pair]
        result.extend([element, template[i]])
    template = ''.join(result)

counts = Counter(template).most_common()
answer = counts[0][1] - counts[-1][1]
print(answer)


template = template0
pairs = Counter(template[i-1: i+1] for i in range(1, len(template)))
elements = Counter(template)
for step in range(40):
    new_pairs = Counter()
    for pair, count in pairs.items():
        element = rules[pair]
        new_pairs[pair[0] + element] += count
        new_pairs[element + pair[1]] += count
        elements[element] += count
    pairs = new_pairs.copy()
    #print(sum(pairs.values()), sum(elements.values()))

counts = elements.most_common()
answer = counts[0][1] - counts[-1][1]
print(answer)
