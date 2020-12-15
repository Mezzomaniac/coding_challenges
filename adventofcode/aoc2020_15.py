data = '13,0,10,12,1,5,8'

from collections import deque

numbers = deque(int(n) for n in data.split(','))
numbers.reverse()
prev = numbers[0]
limit = 2020
#limit = 30000000
while len(numbers) < limit:
    if numbers.count(prev) == 1:
        prev = 0
        numbers.appendleft(prev)
    else:
        last = numbers.index(prev, 1)
        prev = last
        numbers.appendleft(prev)
    #print(prev)
    #if not len(numbers) % 1000:
        #print(len(numbers))
print(prev)

#print('\n' * 10)
numbers = {int(number): turn for turn, number in enumerate(data.split(','), 1)}
turn = len(data.split(','))
limit = 30000000
#last = int(data.split(',')[-1])
next = 0
while turn < limit:
    turn += 1
    prev = next
    try:
        next = turn - numbers[next]
    except KeyError:
        next = 0
    numbers[prev] = turn
    #print(prev)
    if not turn % 100000:
        print(turn)
print(prev)
