seq = '1113222113'

from itertools import groupby

def look_and_say(seq):
    return ''.join(str(len(list(group))) + number for number, group in groupby(seq))

def recurse(func, arg, times):
    for _ in range(times):
        arg = func(arg)
    return arg

print(len(recurse(look_and_say, seq, 40)))
print(len(recurse(look_and_say, seq, 50)))
