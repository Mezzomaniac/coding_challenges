data = '''deal with increment 55
cut -6984
deal into new stack
cut -2833
deal with increment 75
cut 2488
deal with increment 54
cut 9056
deal with increment 52
cut -2717
deal with increment 4
deal into new stack
cut -852
deal with increment 21
cut -3041
deal with increment 38
cut -6871
deal into new stack
deal with increment 32
cut 988
deal with increment 29
deal into new stack
deal with increment 68
cut 5695
deal with increment 36
cut -27
deal with increment 33
deal into new stack
cut -1306
deal with increment 30
cut -4033
deal with increment 28
cut -442
deal into new stack
deal with increment 30
cut -6295
deal with increment 56
cut -4065
deal into new stack
cut 5275
deal with increment 64
cut 9747
deal into new stack
deal with increment 63
cut -3772
deal with increment 61
deal into new stack
cut 1021
deal with increment 73
deal into new stack
deal with increment 7
cut -1232
deal with increment 52
cut -3439
deal with increment 31
cut 1128
deal into new stack
deal with increment 55
deal into new stack
deal with increment 39
cut -3424
deal with increment 11
deal into new stack
cut 4139
deal with increment 15
deal into new stack
cut 5333
deal with increment 16
cut -6787
deal with increment 39
cut -5817
deal into new stack
deal with increment 62
cut -2704
deal with increment 64
deal into new stack
deal with increment 70
cut 3436
deal with increment 65
cut -8686
deal with increment 22
cut -6190
deal with increment 13
cut -100
deal into new stack
cut -619
deal into new stack
cut 3079
deal with increment 53
cut 1725
deal with increment 19
cut 3440
deal with increment 64
cut 8578
deal with increment 5
cut 2341
deal with increment 45
cut 2217
deal with increment 13
deal into new stack'''

test1 = '''deal with increment 7
deal into new stack
deal into new stack'''

test2 = '''cut 6
deal with increment 7
deal into new stack'''

test3 = '''deal with increment 7
deal with increment 9
cut -2'''

test4 = '''deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1'''

test = '''deal with increment 3
deal into new stack
deal with increment 1
cut -2
cut 5
deal into new stack'''

#data = test
print(data)

from collections import deque, namedtuple
from functools import lru_cache
import itertools
from time import time
import more_itertools

def deal(deck, techniques):
    techniques = techniques.splitlines()
    for technique in techniques:
        #print(technique)
        if technique.endswith('k'):
            deck.reverse()
        elif technique.startswith('c'):
            n = int(technique.split()[-1])
            deck.rotate(-n)
        else:
            n = int(technique.split()[-1])
            for card in list(deck):
                deck[0] = card
                deck.rotate(-n)
        #print(deck)
    #print(deck.index(2019))
    #print(deck[2020])
    return deck

def newstack(deck):
    deck.reverse()
    return deck
    #return reversed(deck)
    #return more_itertools.always_reversible(deck)

def cut_n(n, size=10007):
    '''if n < 0:
        n = size + n'''
    def cut(deck):
        deck.rotate(-n)
        return deck
        '''head = itertools.islice(deck, n)
        body = itertools.islice(deck, n, None)
        return itertools.chain(body, head)'''
    return cut

def increment_n(n):
    def increment(deck):
        for card in list(deck):
            deck[0] = card
            deck.rotate(-n)
        return deck
    return increment

size = 119315717514047
#size1 = 10007

shuffles = 101741582076661

actions = []
for technique in data.splitlines():
    if technique.endswith('k'):
        actions.append(newstack)
    elif technique.startswith('c'):
        n = int(technique.split()[-1])
        actions.append(cut_n(n, size))
    else:
        n = int(technique.split()[-1])
        actions.append(increment_n(n))

def deal2(deck, actions):
    for action in actions:
        deck = action(deck)
    #print(deck.index(2019))
    return deck

#deck = deque(range(10))
#deal(deck, test4)
#deck = deque(range(10007))
#t = time()
#deal(deck, data)
#print(time() - t)

#deck = deque(range(10007))
#t = time()
#deck = deque(range(size))
#deck = deal2(deck, actions)
#print(list(deck))
#print(time() - t)

'''results = {3}
deck = deque(range(23))
for i in range(25):
    deck = deal(deck, test4)
    card = deck[3]
    print(i, card)
    results.add(card)'''

#results = [2020]
prev = 2020
deck = deque(range(10007))
for i in range(0):
    #print(i)
    deck = deal2(deck, actions)
    card = deck[2020]
    #if card in results:
        #print(f'repeat at {i}')
    #elif not i % 100:
        #print(i)
    #results.append(card)
    print(card, card - prev)
    prev = card
#print()
#print(results)
#print(len(set(results)))

'''deck = deque(range(size))
for i in range(shuffles):
    print(i)
    deck = deal2(deck, actions)
    #print()'''

def newstacker_card(size):
    '''create inverse function (ie what card is in the position, not where is the card) for dealing a new stack'''
    def newstack_card(card):
        return (size - card - 1) % size
    return newstack_card

def cut_n_card(n, size):
    '''create inverse function (ie what card is in the position, not where is the card) for cutting the deck'''
    def cut_card(card):
        return (card + n) % size
    return cut_card

def increment_n_card(n, size):
    '''create inverse function (ie what card is in the position, not where is the card) for dealing with an increment'''
    def increment_card(card):
        '''for i in range(n):
            if not (size * i + card) % n:
                multiplier = i
                break'''
        #multiplier = ((-card) * size ** (n - 2)) % n
        multiplier = -card * pow_mod(size, n-2, n) % n
        return (size * multiplier + card) // n
        #return (size * (-card * size ** (n - 2) % n) + card) // n
    return increment_card

def solve(size, card, actions):
    for action in actions:
        card = action(card)
    return card

#@lru_cache(maxsize=256)
#def pow_mod(x, n, m):
    #return pow(x, n, m)

@lru_cache(maxsize=2048)
def pow_mod(x, n, m):
    ''' Calculate x ** n % m using exponentiation by squaring for when the numbers are too big to use pow()
    
    See https://codeforces.com/blog/entry/72527'''
    
    if not n:
        return 1
    t = pow_mod(x, n//2, m)
    if not n % 2:
        return t * t % m
    return t * t * x % m

card = 2020

def parse_techniques(data, size):
    actions = []
    for technique in data.splitlines():
        if technique.endswith('k'):
            actions.append(newstacker_card(size))
        elif technique.startswith('c'):
            n = int(technique.split()[-1])
            actions.append(cut_n_card(n, size))
        else:
            n = int(technique.split()[-1])
            actions.append(increment_n_card(n, size))
    return actions

def solve2(size, card, techniques, shuffles):
    t = time()
    actions = parse_techniques(techniques, size)
    actions.reverse()
    #seen = {card}
    #seen = {card: 0}
    for i in range(shuffles):
        #if not i % 100000:
            #print(i, time() - t)
        for action in actions:
            card = action(card)
            #print(card)
        #if card == 2020:
            #print(i)
        #if card in seen:
        #print(i, card)
            #print(i, card, seen[card])
        #seen.add(card)
        #seen[card] = i
    return card

#print(solve2(size, card, data, shuffles))

#print(solve2(10, 0, data, 10))

# https://www.reddit.com/r/adventofcode/comments/fgr4ml/2019_day_222_any_kind_soul_willing_to_help_find/

#for card in range(11):
    #print(solve2(11, card, data, 1))

#size = 7
#shuffles = 1
#card = 5

factor = 1
constant = 0
for technique in reversed(data.splitlines()):
    print(technique)
    if technique.endswith('k'):
        factor = -factor % size
        constant = (-constant - 1) % size
    elif technique.startswith('c'):
        n = int(technique.split()[-1])
        constant = (constant + n) % size
    else:
        n = int(technique.split()[-1])
        multiplier = pow_mod(n, size-2, size)
        factor = factor * multiplier % size
        constant = constant * multiplier % size
    #print(f'{factor}x + {constant}')
    #print([((factor * x % size) + (constant % size)) % size for x in range(size)])
print(f'{factor}x + {constant}')

Coefficients = namedtuple('Coefficients', 'factor constant')

cumulative_coefficients = Coefficients(factor, constant)
current_coefficients = cumulative_coefficients
coefficient_multiples = {1: current_coefficients}
accumulated_shuffles = 1
current_multiplier = 1
while accumulated_shuffles < shuffles:
    if accumulated_shuffles + current_multiplier <= shuffles:
        factor = (cumulative_coefficients.factor * current_coefficients.factor) % size
        constant = (cumulative_coefficients.constant * current_coefficients.factor + current_coefficients.constant) % size
        accumulated_shuffles += current_multiplier
        cumulative_coefficients = Coefficients(factor, constant)
        coefficient_multiples[accumulated_shuffles] = cumulative_coefficients
        current_multiplier *= 2
        current_coefficients = cumulative_coefficients
        #print(accumulated_shuffles, current_multiplier)
        #print(cumulative_coefficients)
        print((cumulative_coefficients.factor * card % size + cumulative_coefficients.constant % size) % size)
    else:
        current_multiplier //= 2
        current_coefficients = coefficient_multiples[current_multiplier]
print(cumulative_coefficients)
print((cumulative_coefficients.factor * card % size + cumulative_coefficients.constant % size) % size)


# https://www.reddit.com/r/adventofcode/comments/ee56wh/2019_day_22_part_2_so_whats_the_purpose_of_this/fbr0vjb/?utm_source=share&utm_medium=ios_app&utm_name=ioscss&utm_content=1&utm_term=1&context=3
