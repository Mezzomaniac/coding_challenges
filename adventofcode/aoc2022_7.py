from downloader import download

download(2022, 7)
with open('aoc2022_7input.txt') as inputfile:
    data = inputfile.read()
print(data)

current_dir = {'size': 0, 'prev': None}
candidates_total = 0
sizes = set()
for line in data.splitlines()[1:]:
    line = line.split()
    if line[0].isdigit():
        current_dir[line[1]] = int(line[0])
        current_dir['size'] += int(line[0])
    elif line[0] == 'dir':
        current_dir[line[1]] = {'size': 0, 'prev': current_dir}
    elif line[1] == 'cd':
        if line[2] == '..':
            size = current_dir['size']
            current_dir = current_dir['prev']
            current_dir['size'] += size
            if size <= 100000:
                candidates_total += size
            sizes.add(size)
        elif line[2] != '/':
            current_dir = current_dir[line[2]]
while current_dir['prev']:
    size = current_dir['size']
    current_dir = current_dir['prev']
    current_dir['size'] += size
    sizes.add(size)
sizes.add(current_dir['size'])
print(candidates_total)

required_space = 30000000 - (70000000 - current_dir['size'])
print(min(filter(lambda size: size >= required_space, sizes)))
