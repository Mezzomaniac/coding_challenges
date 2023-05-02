from downloader import download
from functools import reduce
from operator import xor
from more_itertools import chunked

download(2017, 10)
with open('aoc2017_10input.txt') as inputfile:
    data = inputfile.read()
#print(data)

test = '3,4,1,5'
test = ''
#data = test

marks = 256
#marks = 5

def knot(data):
    string = list(range(marks))
    pos = 0
    skip = 0
    for length in data.split(','):
        length = int(length)
        string[:length] = reversed(string[:length])
        jump = length + skip
        string = string[jump % marks:] + string[:jump % marks]
        pos += jump
        skip += 1
        print(length, string, skip, pos)
    string = string[-pos % marks:] + string[:-pos % marks]
    return string

def knothash(data):
    string = list(range(marks))
    pos = 0
    skip = 0
    for length in ([ord(c) for c in data.strip()] + [17, 31, 73, 47, 23]) * 64:
        string[:length] = reversed(string[:length])
        jump = length + skip
        string = string[jump % marks:] + string[:jump % marks]
        pos += jump
        skip += 1
    string = string[-pos % marks:] + string[:-pos % marks]
    densehash = [reduce(xor, chunk) for chunk in chunked(string, 16)]
    result = ''.join(f'{n:02x}' for n in densehash)
    return result

if __name__ == '__main__':
    string = knot(data)
    print(string)
    print(string[0] * string[1])
    
    hash = knothash(data)
    print(hash)
