from downloader import download

download(2023, 15)
with open('aoc2023_15input.txt') as inputfile:
    data = inputfile.read().strip()
test_data = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'
#data = test_data
print(data)

from collections import defaultdict
from dataclasses import dataclass
import re

def hASH(string):
    current_value = 0
    for char in string:
        if char == '\n':
            continue
        current_value = ((current_value + ord(char)) * 17) % 256
    return current_value

total = 0
for step in data.split(','):
    total += hASH(step)
print(total)

@dataclass()
class Lens:
    label: str
    focal_length: str

boxes = defaultdict(list)
for step in data.split(','):
    label, op = re.split('=|-', step)
    box = hASH(label)
    if not op:
        for lens in boxes[box]:
            if lens.label == label:
                boxes[box].remove(lens)
                break
    else:
        for lens in boxes[box]:
            if lens.label == label:
                lens.focal_length = op
                break
        else:
            boxes[box].append(Lens(label, op))

focussing_power = 0
for box in boxes:
    for slot, lens in enumerate(boxes[box], 1):
        focussing_power += (box + 1) * slot * int(lens.focal_length)
print(focussing_power)
