from collections import deque

steps = 314

buffer = deque()
for i in range(2018):
    buffer.append(i)
    buffer.rotate(-steps)
    #print(buffer)
print(buffer[buffer.index(2017) + 1])

buffer = deque()
for i in range(50_000_000):
    if not i % 1_000_000:
        print(i)
    buffer.append(i)
    buffer.rotate(-steps)
print(buffer[buffer.index(0) + 1])
