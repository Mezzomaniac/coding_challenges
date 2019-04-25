target = 293801

recipes = [3, 7]
elf1 = 0
elf2 = 1
#while len(recipes) < target + 10:
while True:
    new = recipes[elf1] + recipes[elf2]
    recipes.extend(divmod(new, 10)) if new > 9 else recipes.append(new)
    elf1 = (elf1 + recipes[elf1] + 1) % len(recipes)
    elf2 = (elf2 + recipes[elf2] + 1) % len(recipes)
    #if len(recipes) in (19, 15, 28, 2028, target + 10):
        #print(*recipes[-10:], sep='')
    if list(int(digit) for digit in str(target)) == recipes[-6:]
        print(len(recipes) - 6)
        break
    if list(int(digit) for digit in str(target)) == recipes[-7:-1]:
        print(len(recipes) - 7)
        break
#print(*recipes[-10:], sep='')
