from downloader import download

download(2021, 8)
with open('aoc2021_8input.txt') as inputfile:
    data = {}
    for line in inputfile.read().splitlines():
        samples, outputs = line.split(' | ')
        data[frozenset(samples.split())] = outputs.split()
print(data)

uniques_count = 0
for outputs in data.values():
    uniques_count += sum(len(output) in (2, 3, 4, 7) for output in outputs)
print(uniques_count)

uniques = {2: '1', 3: '7', 4: '4', 7: '8'}

total = 0
for samples, outputs in data.items():
    mapping = {}
    length5s = set()
    length6s = set()
    for sample in samples:
        length = len(sample)
        if length in uniques:
            mapping[frozenset(sample)] = uniques[length]
        elif length == 5:
            length5s.add(sample)
        elif length == 6:
            length6s.add(sample)
    reverse_mapping = {value: key for key, value in mapping.items()}
    for sample in length6s:
        if len(set(sample) & set(reverse_mapping['4'])) == 4:
            mapping[frozenset(sample)] = '9'
        elif len(set(sample) & set(reverse_mapping['7'])) == 3:
            mapping[frozenset(sample)] = '0'
        else:
            mapping[frozenset(sample)] = '6'
            reverse_mapping['6'] = frozenset(sample)
    for sample in length5s:
        if len(set(sample) & set(reverse_mapping['1'])) == 2:
            mapping[frozenset(sample)] = '3'
        elif len(set(sample) & set(reverse_mapping['6'])) == 5:
            mapping[frozenset(sample)] = '5'
        else:
            mapping[frozenset(sample)] = '2'
    total += int(''.join(mapping[frozenset(output)] for output in outputs))
print(total)
