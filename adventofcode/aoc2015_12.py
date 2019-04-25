import json
from pprint import pprint

with open('aoc2015-12.txt') as file:
    data = file.read()

total = 0
for match in re.finditer('\d+', data):
    try:
        number = int(data[match.start() - 1: match.end()])
    except ValueError:
        number = int(match.group())
    total += number
print(total)


data = json.loads(data)
#pprint(data)

def traverse(obj):
    if isinstance(obj, int):
        return obj
    elif isinstance(obj, str):
        return 0
    elif isinstance(obj, list):
        return sum(traverse(item) for item in obj)
    elif isinstance(obj, dict):
        return 0 if "red" in obj.values() else sum(traverse(item) for item in obj.values())
    else:
        raise TypeError

print(traverse(data))
