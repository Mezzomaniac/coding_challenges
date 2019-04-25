from hashlib import md5

secret_key = 'yzbqklnj'

n = 0
while not md5(bytes(secret_key + str(n), encoding='utf8')).hexdigest().startswith('000000'):
    n += 1
else:
    print(n)
