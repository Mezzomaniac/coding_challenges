from downloader import download
from itertools import zip_longest

download(2022, 13)
with open('aoc2022_13input.txt') as inputfile:
    data = inputfile.read()
#print(data)

def compare(left, right):
    for left_item, right_item in zip_longest(left, right, fillvalue='x'):
        if isinstance(left_item, list) and isinstance(right_item, int):
            right_item = [right_item]
        elif isinstance(right_item, list) and isinstance(left_item, int):
            left_item = [left_item]
        if left_item == right_item:
            continue
        elif left_item == 'x':
            return True
        elif right_item == 'x':
            return False
        elif isinstance(left_item, list):
            comparison = compare(left_item, right_item)
            if comparison is not None:
                return comparison
        else:
            return left_item < right_item

correct_order_indices_sum = 0
for index, pair in enumerate(data.split('\n\n'), 1):
    left, right = pair.splitlines()
    comparison = compare(eval(left), eval(right))
    if comparison:
        correct_order_indices_sum += index
print(correct_order_indices_sum)

class Packet:
    
    def __init__(self, item):
        self.item = item
    
    def __lt__(self, other):
        return compare(self.item, other.item)
    
    def __str__(self):
        return self.item

dividers = [Packet([[2]]), Packet([[6]])]
packets = [Packet(eval(packet)) for packet in data.replace('\n\n', '\n').splitlines()] + dividers
ordered = sorted(packets)
print((ordered.index(dividers[0]) + 1) * (ordered.index(dividers[1]) + 1))
