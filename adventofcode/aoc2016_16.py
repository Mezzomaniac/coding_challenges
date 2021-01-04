data = '10011111011011001'
length = 272
length = 35651584

translation_table = str.maketrans('01', '10')

def step(a):
    b = a[::-1].translate(translation_table)
    return f'{a}0{b}'

def checksum(data):
    result = []
    for char1, char2 in zip(data[::2], data[1::2]):
        result.append(str(int(char1 == char2)))
    return ''.join(result)

while len(data) < length:
    data = step(data)
    print(len(data))
data = data[:length]
check = checksum(data)
while not len(check) % 2:
    check = checksum(check)
    print(len(check))
print(check)
