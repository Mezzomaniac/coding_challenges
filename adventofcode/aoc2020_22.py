p1 = '''31
33
27
43
29
25
36
11
15
5
14
34
7
18
26
41
19
45
12
1
8
35
44
30
50'''

p2 = '''42
40
6
17
3
16
22
23
32
21
24
46
49
48
38
47
13
9
39
20
10
2
37
28
4'''

p1test = '''9
2
6
3
1'''

p2test = '''5
8
4
7
10'''

#p1, p2 = p1test, p2test

from collections import deque

def parse_deck(data):
    return deque(int(card) for card in data.splitlines())

decks = (parse_deck(p1), parse_deck(p2))

def turn(decks):
    card1 = decks[0].popleft()
    card2 = decks[1].popleft()
    decks[card1 < card2].extend(sorted((card1, card2), reverse=True))
    return decks

while decks[0] and decks[1]:
    decks = turn(decks)
if not decks[0]:
    winner = 1
else:
    winner = 0

def score(decks, winner):
    return sum(pos * card for pos, card in enumerate(reversed(decks[winner]), 1))
print(score(decks, winner))

def round(decks):
    p1, p2 = decks
    card1 = p1.popleft()
    card2 = p2.popleft()
    if len(p1) >= card1 and len(p2) >= card2:
        new_p1 = deque(list(p1)[:card1])
        new_p2 = deque(list(p2)[:card2])
        _, winner = game((new_p1, new_p2))
    else:
        winner = card1 < card2
    if not winner:
        cards = [card1, card2]
    else:
        cards = [card2, card1]
    decks[winner].extend(cards)
    return decks

def game(decks):
    prev_rounds = set()
    winner = None
    while winner is None:
        decks = round(decks)
        if not decks[0]:
            winner = 1
        elif not decks[1]:
            winner = 0
        if tuple(tuple(deck) for deck in decks) in prev_rounds:
            return decks, 0
        prev_rounds.add(tuple(tuple(deck) for deck in decks))
    return decks, winner

def match(decks):
    decks, winner = game(decks)
    return score(decks, winner)

decks = (parse_deck(p1), parse_deck(p2))
print(match(decks))
