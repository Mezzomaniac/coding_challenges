from downloader import download
from collections import deque

download(2022, 20)
with open('aoc2022_20input.txt') as inputfile:
    data = inputfile.read()
test = '''1
2
-3
3
-2
0
4'''
#data = test
print(data)

class Number:
    
    def __init__(self, n):
        self.n = n
    
    def __repr__(self):
        #return f'Number({self.n})'
        return repr(self.n)
    
    def __str__(self):
        return str(self.n)

#file = deque(Number(int(n)) for n in data.splitlines())
file = deque(Number(int(n) * 811589153) for n in data.splitlines())

#for number in file.copy():
for number in file.copy() * 10:
    if number.n == 0:
        zero = number
    file.rotate(-file.index(number))
    file.popleft()
    file.rotate(-number.n)
    file.appendleft(number)
    #print(file)
file.rotate(-file.index(zero))
print(sum(file[index % len(file)].n for index in range(1000, 3001, 1000)))
