keys = {14788856: None, 19316454: None}
#keys = {5764801: None, 17807724: None}

def transform(value, subject):
    value *= subject
    value %= 20201227
    return value

found = 0
value = 1
for loop in range(1, 20201227+1):
    value = transform(value, 7)
    #if not loop % 100000:
        #print(loop, value)
    if value in keys:
        keys[value] = loop
        found += 1
        print(loop, value)
    if found == 2:
        break

keys = list(keys.items())
value = 1
for loop in range(keys[0][1]):
    value = transform(value, keys[1][0])
print(value)
value = 1
for loop in range(keys[1][1]):
    value = transform(value, keys[0][0])
print(value)
