#from itertools import cycle
from string import ascii_lowercase as abc

current = 'cqjxjnds'

def straight(password):
    for pos in range(len(password) - 2):
        sub = password[pos:pos+3]
        if sub in abc:
            return True
    return False

def unambiguous(password):
    return set(password).isdisjoint(set('iol'))

def two_pair(password):
    pairs = 0
    skip = False
    for letter1, letter2 in zip(password, password[1:]):
        if skip:
            skip = False
            continue
        if letter1 == letter2:
            pairs += 1
            if pairs >= 2:
                return True
            skip = True
    return False

def increment_letter(letter):
    return abc[abc.index(letter)+1]

def increment_word(word):
    if word[-1] != 'z':
        return word[:-1] + increment_letter(word[-1])
    return increment_word(word[:-1]) + 'a'

def increment_password(password):
    valid = False
    while not valid:
        password = increment_word(password)
        valid = straight(password) and unambiguous(password) and two_pair(password)
    return password

next_pass = increment_password(current)
print(next_pass)
print(increment_password(next_pass))
