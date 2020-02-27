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

test = 'deal with increment 4'

from collections import deque

def deal(deck, techniques):
    techniques = techniques.splitlines()
    for technique in techniques:
        print(technique)
        if technique.endswith('k'):
            deck.reverse()
        elif technique.startswith('c'):
            n = int(technique.split()[-1])
            deck.rotate(-n)
        else:
            n = int(technique.split()[-1])
            '''new = deque()
            while len(new) < len(deck):
                new.append(deck[0])
                deck.rotate(n)
            deck = new'''
            new = {}
            it = iter(deck)
            i = 0
            while len(new) < len(deck):
                new[i] = next(it)
                i = (i + n) % len(deck)
            #print(new)
            deck = deque(value for key, value in sorted(new.items()))
        print(deck)
        #print(deck[2020])
    return deck

deck = deque(range(10))
deal(deck, test4)
#deck = deque(range(10007))
#deck = deal(deck, data)
#print(deck.index(2019))

'''deck = deque(range(119315717514047))
for i in range(101741582076661):
    print(deck[2020])
    deck = deal(deck, data)'''