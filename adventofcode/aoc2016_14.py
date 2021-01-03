salt = 'zpqevtbw'
#salt = 'abc'

from hashlib import md5

keys = set()
pending = {}
index = 0
while len(keys) < 70:
    if not index % 1000:
        print(index)
    hash = md5(f'{salt}{index}'.encode()).hexdigest()
    for _ in range(2016):
        hash = md5(hash.encode()).hexdigest()
    for slider in range(3, len(hash)+1):
        window = hash[slider-3: slider]
        if index not in pending and len(set(window)) == 1:
            pending[index] = window[0]
            #print(index, window, keys)
        window = hash[slider-5: slider]
        if len(set(window)) == 1:
            char = window[0]
            for key, value in pending.copy().items():
                if index == key:
                    continue
                if index - key > 1000:
                    #print(f'del {key}')
                    del pending[key]
                    continue
                if value == char:
                    keys.add(key)
                    #print(index, window, keys)
    index += 1
#print(sorted(keys))
print(sorted(keys)[63])
