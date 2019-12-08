from more_itertools import chunked

with open('aoc2019_8.txt') as file:
    data = file.read().strip()

layers = chunked(data, 25*6)

least_zeros = 25 * 6
onesbytwos = 0
for layer in layers:
    zeros = layer.count('0')
    if zeros < least_zeros:
        least_zeros = zeros
        onesbytwos = layer.count('1') * layer.count('2')
print(onesbytwos)

visible = []
for pixel in range(25*6):
    for layer in data[pixel::25*6]:
        if layer < '2':
            visible.append(layer)
            break
#print(len(visible))
for line in range(-25*5, -1, 25):
    visible.insert(line, '\n')
image = ''.join(visible)
#print(image)
image = image.replace('0', '⬛️').replace('1', '⬜️')
print(image)