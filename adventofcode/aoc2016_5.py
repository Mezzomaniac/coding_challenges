door = 'abbhdwsy'

from hashlib import md5

password = ''
n = 0
for i in range(8):
    while True:
        attempt = door + str(n)
        hash = md5(attempt.encode()).hexdigest()
        n += 1
        if hash.startswith('00000'):
            password += hash[5]
            break
print(password)

password2 = [''] * 8
n = 0
while sum(bool(i) for i in password2) < 8:
    attempt = door + str(n)
    hash = md5(attempt.encode()).hexdigest()
    n += 1
    if hash.startswith('00000'):
        try:
            pos = int(hash[5])
            if not password2[pos]:
                password2[pos] = hash[6]
        except (ValueError, IndexError):
            pass
print(''.join(password2))
