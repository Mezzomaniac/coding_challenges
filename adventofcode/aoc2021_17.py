from downloader import download

download(2021, 17)
with open('aoc2021_17input.txt') as inputfile:
    input = inputfile.read()

target_area = []
for coord in input.split()[2:]:
    start, end = coord.strip(',').split('=')[1].split('..')
    target_area.append(range(int(start), int(end) + 1))
print(target_area)

def point_add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def update_velocity(vx, vy):
    try:
        vx -= vx // abs(vx)
    except ZeroDivisionError:
        vx = 0
    vy -= 1
    return (vx, vy)

successes = 0
overall_heighest = 0
#for start_vx in range(20, 40):
for start_vx in range(20, max(target_area[0]) + 1):
    #for start_vy in range(0, 200):
    for start_vy in range(min(target_area[1]), 200):
        vx, vy = start_vx, start_vy
        x = y = heighest = 0
        success = False
        while x <= max(target_area[0]) and y >= min(target_area[1]):
            x, y = point_add((x, y), (vx, vy))
            vx, vy = update_velocity(vx, vy)
            heighest = max(heighest, y)
            if x in target_area[0] and y in target_area[1]:
                success = True
        if success:
            successes += 1
            overall_heighest = max(overall_heighest, heighest)
            if heighest == overall_heighest:
                print(start_vx, start_vy)
print(overall_heighest)
print(successes)
