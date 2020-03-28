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

test = '''deal with increment 5'''

data = test

from collections import deque
import itertools
from time import time
import more_itertools
import matplotlib
import matplotlib.pyplot as plt

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

'''deck = deque(range(119315717514047))
for i in range(101741582076661):
    print(i)
    deck = deal2(deck, actions)
    #print()'''

def newstacker_card(size):
    def newstack_card(card):
        return (size - card - 1) % size
    return newstack_card

def cut_n_card(n, size):
    def cut_card(card):
        return (card + n) % size
    return cut_card

def increment_n_card(n, size):
    def increment_card(card):
        '''for i in range(n):
            if not (size * i + card) % n:
                multiplier = i
                break'''
        #multiplier = ((-card) * size ** (n - 2)) % n
        #return (size * multiplier + card) // n
        return (size * (-card * size ** (n - 2) % n) + card) // n
    return increment_card

card_actions = []
#card_actions1 = []
for technique in reversed(data.splitlines()):
    if technique.endswith('k'):
        card_actions.append(newstacker_card(size))
        #card_actions1.append(newstacker_card(size1))
    elif technique.startswith('c'):
        n = int(technique.split()[-1])
        card_actions.append(cut_n_card(n, size))
        #card_actions1.append(cut_n_card(n, size1))
    else:
        n = int(technique.split()[-1])
        card_actions.append(increment_n_card(n, size))
        #card_actions1.append(increment_n_card(n, size1))

def solve(size, card, actions):
    for action in actions:
        card = action(card)
    return card

card = 2020
#card1 = 2020
#print(card)
#print(deal2(deque(range(size)), actions)[card])
#print(solve(size, card, card_actions))
#cards = {card}
#last = card
#differences = set()
#last_dif = 0
#differences2 = set()
try:
    for i in range(101741582076661):
    #for i in range(100):
        #if not i % 100000:
            #print(i)
        card = solve(size, card, card_actions)
        #card1 = solve(size1, card1, card_actions1)
        '''difference = last - card
        difference2 = last_dif - difference
        card_repeat = card in cards
        difference_repeat = difference in differences
        difference2_repeat = difference2 in differences2
        if card_repeat or difference_repeat or difference2_repeat:
            print(i, card, difference, difference2, (card_repeat, difference_repeat, difference2_repeat))
        cards.add(card)
        differences.add(difference)
        differences2.add(difference2)
        last = card
        last_dif = difference'''
        print(i, card)#, card1, f'{card / size:.3}, {card1 / size1:.3}')
except KeyboardInterrupt:
    pass
'''#else:
    x, y = zip(*enumerate(cards))
    fig, ax = plt.subplots()
    ax.plot(x, y)
    plt.show()'''

def solve2(s, c):
    
    


# https://www.reddit.com/r/adventofcode/comments/fgr4ml/2019_day_222_any_kind_soul_willing_to_help_find/