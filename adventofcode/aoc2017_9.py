from downloader import download

download(2017, 9)
with open('aoc2017_9input.txt') as inputfile:
    data = inputfile.read()
print(data)

score = 0
level = 0
skip = False
garbage = False
remove = 0
for c in data.strip():
    if skip:
        skip = False
    elif c == '!':
        skip = True
    elif c == '>':
        garbage = False
    elif garbage:
        remove += 1
        continue
    elif c == '<':
        garbage = True
    elif c == '{':
        level += 1
        score += level
    elif c == '}':
        level -= 1
print(score)
print(remove)
