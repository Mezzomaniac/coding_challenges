from downloader import download

download(2021, 13)
with open('aoc2021_13input.txt') as inputfile:
    data = inputfile.read()
print(data)

dots, folds = data.split('\n\n')
dots = {tuple(int(n) for n in line.split(',')) for line in dots.splitlines()}
folds = [fold.split()[-1] for fold in folds.splitlines()]
print(dots)

for line in folds:
    axis, pos = line.split('=')
    pos = int(pos)
    if axis == 'y':
        dots = {(x, y) if y < pos else (x, pos - (y - pos)) for x, y in dots}
    elif axis == 'x':
        dots = {(x, y) if x < pos else (pos - (x - pos), y) for x, y in dots}
    #break
print(len(dots))

max_x = max(dot[0] for dot in dots)
max_y = max(dot[1] for dot in dots)
for y in range(max_y + 1):
    row = []
    for x in range(max_x + 1):
        space = '#' if (x, y) in dots else ' '
        row.append(space)
    print(''.join(row))
