data = '59719896749391372935980241840868095901909650477974922926863874668817926756504816327136638260644919270589305499504699701736406883012172909202912675166762841246709052187371758225695359676410279518694947094323466110604412184843328145082858383186144864220867912457193726817225273989002642178918584132902751560672461100948770988856677526693132615515437829437045916042287792937505148994701494994595404345537543400830028374701775936185956190469052693669806665481610052844626982468241111349622754998877546914382626821708059755592288986918651172943415960912020715327234415148476336205299713749014282618817141515873262264265988745414393060010837408970796104077' # len 650
test_data0 = '11111111'
test_data1 = '12345678'
test_data2 = '80871224585914546619083218645595'
test_data3 = '03036732577212944063491565474664'
#data = test_data3
#data *= 3
#data *= 10000

import itertools
from time import time
from math import factorial as fact
import numpy as np

#t = time()

BASE_PATTERN = (0, 1, 0, -1)

def create_patterns(length):
    return [list(itertools.islice(itertools.cycle(itertools.chain.from_iterable(itertools.repeat(multiplier, position) for multiplier in BASE_PATTERN)), 1, length + 1)) for position in range(1, length + 1)]
    
def phase(signal):
    output = []
    for position in range(1, len(signal) + 1):
        #print(position)
        pattern = itertools.cycle(itertools.chain.from_iterable(itertools.repeat(multiplier, position) for multiplier in BASE_PATTERN))
        digit = sum(element * multiplier for element, multiplier in zip(signal, itertools.islice(pattern, 1, len(signal) + 1)))
        output.append(abs(digit) % 10)
    return output

def phase(signal, patterns):
    return np.remainder(np.abs(np.dot(patterns, signal)), 10)

def iterate(data, phases=100, repeat=1, finalize=True):
    data *= repeat
    patterns = create_patterns(len(data))
    signal = [int(d) for d in data]
    print(signal)
    #result = signal.copy()
    for iteration in range(phases - (not finalize)):
        print(iteration)
        signal = phase(signal, patterns)
        print(signal)
    if not finalize:
        signal = np.dot(patterns, signal)
    return signal

def interpret_result(result):
    result = ''.join(str(d) for d in result)
    print(result[:8])
    #offset = int(result[:7]) # WRONG
    offset = int(data[:7])
    print(offset)
    print(result[offset: offset+8])

"""for repeats in range(1, 2):
    #print(repeats)
    finalize = True
    result = iterate(data, phases=100, repeat=repeats, finalize=finalize)
    #print(result)
    if not finalize:
        result = np.remainder(np.abs(result), 10)
    interpret_result(result)"""
#print(time() - t)

def triangle(n):
    return (n ** 2 + n) // 2

def nCr(n, r):
    if r > n:
        return 0
    if r in (0, n):
        return 1
    r = min(r, n - r)
    #return fact(n) // fact(r) // fact(n-r)
    accum = 1
    for i in range(r):
        accum = accum * (n - i) // (i + 1)
    return accum

def shortcut(signal, phases=100):
    result = []
    result.append(signal[-1])
    result.append(signal[-2] + phases * signal[-1])
    result.append(signal[-3] + phases * signal[-2] + triangle(phases) * signal[-1])  # (x**2 - x)/2 + (x-1) + 1
    result.append(signal[-4] + phases * signal[-3] + triangle(phases) * signal[-2] + (phases))
    
    return reversed(np.remainder(result, 10))

def shortcut(data, phases=100, repeat=1):
    data *= repeat
    patterns = create_patterns(len(data))
    signal = [int(d) for d in data]
    print(signal)
    """result = []
    for i, a in enumerate(signal):
        print(f'i={i}, a={a}')
        addition = a
        '''for j, b in enumerate(signal[i+1:]):
            addition += b * nCr(phases+j, 1+j) * patterns[i][i+j+1]
        result.append(addition % 10)'''
        last_multiplier = 1
        counter = -1
        for j, (digit, multiplier) in enumerate(zip(signal[i+1:], patterns[i][i+1:]), 1):
            print(f'j={j}, digit={digit}, mulitplier={multiplier}')
            if multiplier != last_multiplier:
                counter = -1
                last_multiplier = multiplier
            counter += 1
            addition += digit * nCr(phases + j, j + 1) * multiplier
            print(f'addition={addition}')
        result.append(addition % 10)
        print()"""
    # Only correct for digits in second half:
    result = [(a + 
        sum(b * nCr(phases+j, 1+j) * 
        patterns[i][i+j+1] 
        for j, b in enumerate(signal[i+1:]))
        ) % 10
        for i, a in enumerate(signal)
        ]
    return result

#result = shortcut(data, repeat=10000)
#print(result)
#interpret_result(result)

offset = int(data[:7])
#divisions, remainder = divmod(offset, len(data))
#relevant_signal = [int(d) for d in data[remainder:] + (10000 - divisions - 1) * data]
relevant_signal = [int(d) for d in data * 10000][offset:]
print(len(relevant_signal))
result = []
for i, a in enumerate(relevant_signal[:8]):
    print(f'i={i}, a={a}')
    addition = a
    for j, b in enumerate(relevant_signal[i+1:]):
        if not j % 1000:
            print(f'j={j}, b={b}')
        addition += b * nCr(100+j, 1+j)
    result.append(addition % 10)
    #print()
'''result = [(a + 
        sum(b * nCr(100+j, 1+j)
        for j, b in enumerate(relevant_signal[i+1:]))
        ) % 10
        for i, a in enumerate(relevant_signal[:8])]'''
result = ''.join(str(d) for d in result)
print(result)

print()
#for n in range(10):
    #print([nCr(n, r) for r in range(10)])

for i in range(10):
    8 * nCr(i, 0)

for i in range(10):
    (7 * nCr(i, 0) + 8 * nCr(i, 1)) % 10

for i in range(10):
    (6 * nCr(i, 0) + 7 * nCr(i, 1) + 8 * nCr(i+1, 2)) % 10

for i in range(10):
    (4 + 5 * nCr(i, 1) + 6 * nCr(i+1, 2) + 7 * nCr(i+2, 3) + 8 * (nCr(i+3, 4) - nCr(i, 1))) % 10

for i in range(10):
    (3 + 4 * nCr(i, 1) + 5 * nCr(i+1, 2) + 6 * (nCr(i+2, 3) - nCr(i, 1)) + 7 * (nCr(i+3, 4) - nCr(i+1, 2)) + 8 * (nCr(i+4, 5) - nCr(i+2, 3) - nCr(i, 2))) % 10



((3+4+5 + 4+5+6+7 + 5+6+7+8) + (4+5+6+7 + 5+6+7+8 + 6+7+8 + 7+8) + (5+6+7+8 + 6+7+8 + 7+8 + 8)) + ((4+5+6+7 + 5+6+7+8 + 6+7+8 + 7+8) + (5+6+7+8 + 6+7+8 + 7+8 + 8) + (6+7+8 + 7+8 + 8) + (7+8 + 8)) + ((5+6+7+8 + 6+7+8 + 7+8 + 8) + (6+7+8 + 7+8 + 8) + (7+8 + 8) + (8)) \
== \
3*1 + 4*4 + 5*10 + 6*16 + 7*25 + 8*30 \
== \
3*1 + 4*4 + 5*10 + 6*(20-4) + 7*(35-10) + 8*(56-20-6)


abs(abs(abs(2+3-6-7)%10 + (3+4+5)%10 - (6+7+8)%10 - (7+8)%10)%10 + (3+4+5 + 4+5+6+7 + 5+6+7+8)%10 - (6+7+8 + 7+8 + 8)%10 - (7+8 + 8)%10)%10 + ((3+4+5 + 4+5+6+7 + 5+6+7+8) + (4+5+6+7 + 5+6+7+8 + 6+7+8 + 7+8) + (5+6+7+8 + 6+7+8 + 7+8 + 8))%10 - ((6+7+8 + 7+8 + 8) + (7+8 + 8) + (8))%10 - ((7+8 + 8) + (8))%10