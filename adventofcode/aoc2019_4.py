count = 0
for p in range(156218, 652527+1):
    string = str(p)
    if not any(str(n) * 2 in string and str(n) * 3 not in string for n in range(2, 10)):
        continue
    failed = False
    for i, n in enumerate(string[1:]):
        if n < string[i]:
            failed = True
            break
    if failed:
        continue
    count += 1
print(count)