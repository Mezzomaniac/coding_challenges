from downloader import download

download(2023, 7)
with open('aoc2023_7input.txt') as inputfile:
    data = inputfile.read()
print(data)

from collections import Counter

hands = dict((line.split() for line in data.splitlines()))

card_strengths = 'AKQJT98765432'

def determine_hand_type(hand):
    counts = Counter(hand).values()
    if 5 in counts:
        return 0
    elif 4 in counts:
        return 1
    elif sorted(counts) == [2, 3]:
        return 2
    elif 3 in counts:
        return 3
    elif sorted(counts) == [1, 2, 2]:
        return 4
    elif 2 in counts:
        return 5
    return 6

def key_function(hand):
    return (determine_hand_type(hand), [card_strengths.index(card) for card in hand])

sorted_hands = sorted(hands.keys(), key=key_function, reverse=True)
winnings = sum((sorted_hands.index(hand) + 1) * int(bid) for hand, bid in hands.items())
print(winnings)


card_strengths = 'AKQT98765432J'

def determine_hand_type_with_jokers(hand):
    groups = Counter(hand)
    jokers = groups['J']
    del groups['J']
    counts = groups.values()
    if max(counts, default=0) + jokers == 5:
        return 0
    elif max(counts) + jokers == 4:
        return 1
    elif sorted(counts) in ([2, 3], [2, 2]):
        return 2
    elif max(counts) + jokers == 3:
        return 3
    elif sorted(counts) == [1, 2, 2]:
        return 4
    elif max(counts) + jokers == 2:
        return 5
    return 6

def key_function(hand):
    return (determine_hand_type_with_jokers(hand), [card_strengths.index(card) for card in hand])

sorted_hands = sorted(hands.keys(), key=key_function, reverse=True)
winnings = sum((sorted_hands.index(hand) + 1) * int(bid) for hand, bid in hands.items())
print(winnings)
