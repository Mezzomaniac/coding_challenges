from downloader import download
import numpy as np

download(2017, 21)
with open('aoc2017_21input.txt') as inputfile:
    data = inputfile.read()
print(data)

class HashableArray:
    
    def __init__(self, array):
        self.array = array
    
    def __eq__(self, other):
        return np.all(np.equal(self.array, other.array))
    
    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.array))
    
    def __repr__(self):
        return repr(self.array)
    
    def __str__(self):
        return str(self.array)

def parse_pixels(string):
    string = string.replace('#', '1').replace('.', '0')
    return np.array([[int(n) for n in row] for row in string.split('/')])

rules = {}
for line in data.splitlines():
    input, output = [parse_pixels(pattern) for pattern in line.split(' => ')]
    for flip in range(2):
        input = np.flipud(input)
        for rotation in range(4):
            input = np.rot90(input).copy()
            rules[HashableArray(input)] = output
#print(rules)

image = '.#./..#/###'
image = parse_pixels(image)

iterations = 5
iterations = 18
for i in range(iterations):
    size = image.shape[0]
    if not size % 2:
        sq_size = 2
    else:
        sq_size = 3
    stride = image.strides[-1]
    row_stride = stride * size
    squares = np.lib.stride_tricks.as_strided(image, (size // sq_size, size // sq_size, sq_size, sq_size), strides=(row_stride * sq_size, stride * sq_size, row_stride, stride))
    new_sq_size = sq_size + 1
    new_size = size // sq_size * new_sq_size
    new = np.zeros((new_size, new_size))
    new_stride = new.strides[-1]
    new_row_stride = new_stride * new_size
    new_squares = np.lib.stride_tricks.as_strided(new, (new_size // new_sq_size, new_size // new_sq_size, new_sq_size, new_sq_size), strides=(new_row_stride * new_sq_size, new_stride * new_sq_size, new_row_stride, new_stride))
    for square, new_square in zip((square for row in squares for square in row), (new_square for new_row in new_squares for new_square in new_row)):
        new_square[...] = rules[HashableArray(square)]
    image = new
    #print(image)
print(np.count_nonzero(image))
