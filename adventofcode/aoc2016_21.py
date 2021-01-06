data = '''swap letter e with letter h
swap letter f with letter g
move position 6 to position 3
reverse positions 1 through 6
swap letter b with letter a
swap letter a with letter f
rotate based on position of letter e
swap position 7 with position 2
rotate based on position of letter e
swap letter c with letter e
rotate based on position of letter f
rotate right 6 steps
swap letter c with letter f
reverse positions 3 through 7
swap letter c with letter b
swap position 1 with position 2
reverse positions 3 through 6
swap letter c with letter a
rotate left 0 steps
swap position 3 with position 0
swap letter b with letter e
reverse positions 4 through 7
move position 1 to position 4
swap position 6 with position 3
rotate left 6 steps
rotate right 0 steps
move position 7 to position 3
move position 3 to position 4
swap position 3 with position 2
reverse positions 1 through 6
move position 7 to position 5
reverse positions 4 through 5
rotate based on position of letter g
swap position 4 with position 2
reverse positions 1 through 5
rotate based on position of letter h
rotate based on position of letter f
rotate based on position of letter b
swap position 1 with position 4
swap letter b with letter h
rotate based on position of letter e
swap letter a with letter c
swap position 3 with position 5
rotate right 6 steps
rotate based on position of letter c
move position 2 to position 0
swap letter b with letter e
swap letter g with letter e
rotate based on position of letter d
swap position 6 with position 5
swap letter b with letter c
rotate based on position of letter e
rotate based on position of letter f
rotate based on position of letter f
move position 7 to position 0
rotate right 1 step
rotate right 7 steps
swap position 5 with position 6
move position 6 to position 7
rotate based on position of letter e
swap position 3 with position 1
swap position 4 with position 3
swap letter f with letter a
swap position 5 with position 2
rotate based on position of letter e
rotate left 3 steps
rotate left 1 step
rotate based on position of letter b
rotate left 6 steps
rotate based on position of letter b
rotate right 7 steps
swap position 0 with position 2
swap position 7 with position 5
rotate left 3 steps
reverse positions 4 through 5
move position 2 to position 5
swap letter c with letter f
swap letter g with letter e
rotate left 6 steps
swap position 4 with position 6
rotate based on position of letter h
rotate left 2 steps
swap letter c with letter a
rotate right 3 steps
rotate left 6 steps
swap letter b with letter f
swap position 6 with position 5
reverse positions 3 through 4
reverse positions 2 through 7
swap position 7 with position 4
rotate based on position of letter d
swap position 5 with position 3
swap letter c with letter b
swap position 7 with position 6
rotate based on position of letter c
reverse positions 0 through 7
reverse positions 2 through 4
rotate based on position of letter f
reverse positions 1 through 4
rotate right 7 steps'''

from collections import deque

password = 'abcdefgh'

def swap_pos(password, words):
    positions = list(sorted([int(words[2]), int(words[5])]))
    return f'{password[:positions[0]]}{password[positions[1]]}{password[positions[0]+1:positions[1]]}{password[positions[0]]}{password[positions[1]+1:]}'

def swap_let(password, words):
    letters = (words[2], words[5])
    return password.replace(letters[0], 'X').replace(letters[1], letters[0]).replace('X', letters[1])

def rotate_lr(password, words, unscramble=False):
    index = int(words[2])
    right = words[1] == 'right'
    if unscramble:
        right = not right
    if right:
        return f'{password[-index:]}{password[:-index]}'
    return f'{password[index:]}{password[:index]}'

def rotate_based(password, words, unscramble=False):
    index = password.index(words[-1])
    password = deque(password)
    if not unscramble:
        password.rotate(1 + index + (index > 3))
    elif index % 2:
        password.rotate(-(index//2) - 1)
    elif index == 0:
        password.rotate(-1)
    else:
        password.rotate(-((index+8)//2) - 1)
    return ''.join(password)

def reverse(password, words):
    positions = (int(words[2]), int(words[4]))
    reversing = password[positions[0]: positions[1]+1]
    reversing = reversing[::-1]
    return f'{password[:positions[0]]}{reversing}{password[positions[1]+1:]}'

def move(password, words, unscramble=False):
    positions = [int(words[2]), int(words[-1])]
    if unscramble:
        positions.reverse()
    letter = password[positions[0]]
    password = password.replace(letter, '')
    return f'{password[:positions[1]]}{letter}{password[positions[1]:]}'

def scramble(password, instructions, unscramble=False):
    if unscramble:
        instructions.reverse()
    for line in instructions:
        words = line.split()
        if line.startswith('swap p'):
            password = swap_pos(password, words)
        elif line.startswith('swap l'):
            password = swap_let(password, words)
        elif len(words) == 4:
            password = rotate_lr(password, words, unscramble)
        elif line.startswith('rot'):
            password = rotate_based(password, words, unscramble)
        elif line.startswith('rev'):
            password = reverse(password, words)
        else:
            password = move(password, words, unscramble)
    return password

print(scramble(password, data.splitlines()))

password = 'fbgdceah'
print(scramble(password, data.splitlines(), True))
