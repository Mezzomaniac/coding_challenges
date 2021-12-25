from downloader import download
import numpy as np

download(2021, 20)
with open('aoc2021_20input.txt') as inputfile:
    data = inputfile.read()

test = '''..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###'''
#data = test


algorithm, image = data.split('\n\n')
algorithm = ''.join(algorithm.splitlines()).replace('.', '0').replace('#', '1')
image = np.array([[int(char) for char in line] for line in image.replace('.', '0').replace('#', '1').splitlines()])

print(algorithm)
print(image, '\n\n')

window_shape = (3, 3)
for iteration in range(50):
    print(iteration)
    pad_mode = ('minimum', 'maximum')[iteration % 2]
    image = np.pad(image, ((3, 3), (3, 3)), mode=pad_mode)
    #print(image, '\n\n')
    image_shape = image.shape
    stride = image.strides[-1]
    row_stride = stride * image_shape[1]
    windows = np.lib.stride_tricks.as_strided(image, (image_shape[0] - window_shape[0] + 1, image_shape[1] - window_shape[1] + 1, *window_shape), strides=(row_stride, stride, row_stride, stride))
    '''for window in windows:
        print(window)
        number = ''.join(str(pixel) for pixel in window.ravel())
        print(number)
        index = int(number, 2)
        print(index)
        output = algorithm[index]
        print(output)'''
    image = np.array([int(algorithm[int(''.join(str(pixel) for pixel in window.ravel()), 2)]) for axis in windows for window in axis]).reshape(image_shape[0] - 2, image_shape[1] - 2)
    #print(image, '\n\n')
print(np.count_nonzero(image))

#<6097
#<5860
