TARGET = 36000000

def calculate_presents(house):
    total = house + 1
    for elf in range(2, int(house ** 0.5) + 1):
        div, mod = divmod(house, elf)
        if not mod:
            total += elf + div
    return total * 10

def calculate_presents2(house):
    total = 0
    for elf in range(1, int(house ** 0.5) + 1):
        div, mod = divmod(house, elf)
        if not mod:
            if div <= 50:
                total += elf
            if elf <= 50:
                total += div
    return total * 11

house = 0
presents = 0
while presents < TARGET:
    house += 1
    presents = calculate_presents2(house)
    if not house % 100000:
        print(house, presents)
print(house)
