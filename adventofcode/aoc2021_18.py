from downloader import download
from functools import reduce
from itertools import permutations
from operator import add

download(2021, 18)
with open('aoc2021_18input.txt') as inputfile:
    data = inputfile.read()
#print(data)

test1 = '''[[[[4,3],4],4],[7,[[8,4],9]]]
[1,1]'''

test2 = '''[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]'''

test3 = '''[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]
[7,[5,[[3,8],[1,4]]]]'''

test4 = '''[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]'''

#data = test4

class SnailfishNumber:
    def __init__(self, value, parent=None):
        self.value = value
        self.parent = parent
        try:
            self.left = SnailfishNumber(value[0], self)
        except TypeError:
            self.left = value[0]
        try:
            self.right = SnailfishNumber(value[1], self)
        except TypeError:
            self.right = value[1]

    def __getitem__(self, index):
        if index == 0:
            return self.left
        if index == 1:
            return self.right

    def __repr__(self):
        return f'SN [{self.left!r}, {self.right!r}] depth={self.depth}'
    
    def __str__(self):
        return f'[{self.left}, {self.right}]'
    
    def __add__(self, other):
        if not isinstance(other, SnailfishNumber):
            raise TypeError
        result = SnailfishNumber([self, other])
        done = False
        while not done:
            #print('a')
            #print(result, '\n')
            reduce_snailfish_number_by_explosion(result)
            #print('b')
            #print(result, '\n')
            done = not reduce_snailfish_number_by_splitting(result)
            #print('c')
            #print(result, '\n')
        return result

    @property
    def depth(self):
        try:
            return self.parent.depth + 1
        except AttributeError:
            return 1

    def explode(self):
        #print('d')
        if self.depth != 5:
            #print('r')
            return
        #print(self, '\n')
        current = self
        try:
            while current.parent.left is current:
                #print('e')
                current = current.parent
        except AttributeError:
            #print('u')
            pass
        else:
            prev = current.parent
            try:
                #print('s')
                prev.left += self.left
            except TypeError:
                prev = prev.left
                while True:
                    #print('g')
                    try:
                        prev.right += self.left
                        break
                    except TypeError:
                        #print('h')
                        prev = prev.right
                        
        current = self
        try:
            while current.parent.right is current:
                #print('i')
                current = current.parent
        except AttributeError:
            #print('v')
            pass
        else:
            prev = current.parent
            try:
                #print('k')
                prev.right += self.right
            except TypeError:
                prev = prev.right
                while True:
                    #print('l')
                    try:
                        prev.left += self.right
                        break
                    except TypeError:
                        #print('t')
                        prev = prev.left
        for side in ('left', 'right'):
            if getattr(self.parent, side) is self:
                setattr(self.parent, side, 0)
        
    def split(self):
        #print('w')
        for side in ('left', 'right'):
            #print('x')
            value = getattr(self, side)
            try:
                 splittable = value >= 10
            except TypeError:
                #print('y')
                continue
            if splittable:
                #print('z')
                left = value // 2
                right = value - left
                setattr(self, side, SnailfishNumber([left, right], self))
                return True
        return False
    
    @property
    def magnitude(self):
        try:
            left = 3 * self.left
        except TypeError:
            left = 3 * self.left.magnitude
        try:
            right = 2 * self.right
        except TypeError:
            right = 2 * self.right.magnitude
        return left + right

def reduce_snailfish_number_by_explosion(node):
    #print('m')
    #print(node, '\n')
    if isinstance(node, SnailfishNumber):
        #print('n')
        node.explode()
        #print('o')
        #print(node, '\n')
        reduce_snailfish_number_by_explosion(node.left)
        #print('p')
        #print(node, '\n')
        reduce_snailfish_number_by_explosion(node.right)
        #print('q')
        #print(node, '\n')
        
def reduce_snailfish_number_by_splitting(node, stop=False):
    #print('z')
    #print(node, '\n')
    if isinstance(node, SnailfishNumber) and not stop:
        #print('A')
        stop = reduce_snailfish_number_by_splitting(node.left, stop)
        #print('B')
        #print(node, '\n')
        if not stop:
            stop = node.split()
        #print('C')
        #print(node, '\n')
        stop = reduce_snailfish_number_by_splitting(node.right, stop)
        #print('D')
        #print(node, '\n')
    return stop
        

snailfish_numbers = [SnailfishNumber(eval(line), None) for line in data.splitlines()]
print(snailfish_numbers)

final_sum = reduce(add, snailfish_numbers)
#print(repr(final_sum), '\n')
print(final_sum)
print(final_sum.magnitude)

print(max((a + b).magnitude for a, b in permutations(snailfish_numbers, 2)))
