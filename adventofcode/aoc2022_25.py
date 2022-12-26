from downloader import download

download(2022, 25)
with open('aoc2022_25input.txt') as inputfile:
    data = inputfile.read()
test = '''1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122'''
#data = test
print(data)

digits = '=-012'

total = 0
for number in data.splitlines():
    total += sum((digits.index(digit) - 2) * 5 ** place for place, digit in enumerate(reversed(number)))
print(total)

answer = []
while total:
    total, remainder = divmod(total + 2, 5)
    answer.append(digits[remainder])
print(''.join(reversed(answer)))
