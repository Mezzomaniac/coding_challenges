from downloader import download

download(2023, 5)
with open('aoc2023_5input.txt') as inputfile:
    data = inputfile.read()

test_data = '''seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4'''
#data = test_data
print(data)

categories = data.split('\n\n')
seeds = [int(n) for n in categories[0].split()[1:]]
mappings = [[[int(n) for n in line.split()] for line in mapping.splitlines()[1:]] for mapping in categories[1:]]

def lookup_destination(source, mapping):
    for destination_start, source_start, length in mapping:
        if source in range(source_start, source_start + length):
            return destination_start + source - source_start
    return source

min_location = None
for item in seeds:
    for mapping in mappings:
        item = lookup_destination(item, mapping)
    if min_location is None:
        min_location = item
    min_location = min(min_location, item)
print(min_location)
        
seeds = list(zip(seeds[::2], seeds[1::2]))
min_location = 0
humidity_location_mapping = sorted(mappings[-1])
found = False
while humidity_location_mapping:
    if found:
        break
    print(f'{min_location=}')
    destination_start, source_start, length = humidity_location_mapping[0]
    if destination_start == min_location:
        humidity_location_mapping.pop(0)
    else:
        length = destination_start - min_location
        destination_start = min_location
        source_start = destination_start
    next_min_location = destination_start + length
    print(f'{destination_start=}, {source_start=}, {length=}')
    print(f'{next_min_location=}')
    goal_ranges = {range(destination_start, destination_start + length): range(source_start, source_start + length)}
    for mapping in mappings[-2::-1]:
        print(f'{mapping=}')
        source_ranges = {}
        while goal_ranges:
            print(f'{goal_ranges=}')
            print(f'{source_ranges=}')
            location_range, goal_range = goal_ranges.popitem()
            print(f'{location_range=}, {goal_range=}')
            for destination_start, source_start, length in mapping:
                print(f'{destination_start=}, {source_start=}, {length=}')
                destination_stop = destination_start + length
                source_stop = source_start + length
                if goal_range.stop <= destination_start or goal_range.start >= destination_stop:
                    print('a')
                    continue
                if goal_range.start >= destination_start:
                    print('b')
                    selected_source_start = source_start + goal_range.start - destination_start
                    location_start = location_range.start
                else:
                    print('c')
                    selected_source_start = source_start
                    location_start = location_range.start + (destination_start - goal_range.start)
                    goal_ranges[range(location_range.start, location_range.start + destination_start - goal_range.start)] = range(goal_range.start, destination_start)
                if goal_range.stop <= destination_stop:
                    print('d')
                    selected_source_stop = source_stop - (destination_stop - goal_range.stop)
                    location_stop = location_range.stop
                else:
                    print('e')
                    selected_source_stop = source_stop
                    location_stop = location_range.stop - (goal_range.stop - destination_stop)
                    goal_ranges[range(location_stop, location_range.stop)] = range(destination_stop, goal_range.stop)
                print(f'{location_start=}, {location_stop=}, {selected_source_start=}, {selected_source_stop=}')
                source_ranges[range(location_start, location_stop)] = range(selected_source_start, selected_source_stop)
                break
            else:
                print('f')
                source_ranges[location_range] = goal_range
        goal_ranges = source_ranges
    for location_range, destination_seed_range in sorted(goal_ranges.items(), key=lambda item: item[0].start):
        if found:
            break
        print(f'{location_range=}, {destination_seed_range=}')
        for seed_start, length in seeds:
            seed_stop = seed_start + length
            print(f'{seed_start=}, {seed_stop=}')
            if seed_start <= destination_seed_range.start < seed_stop or seed_start < destination_seed_range.stop < seed_stop:
                print('g')
                seed = max(seed_start, destination_seed_range.start)
                print(location_range.start + seed - destination_seed_range.start)
                found = True
                break
    min_location = next_min_location

