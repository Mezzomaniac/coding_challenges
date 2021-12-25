from downloader import download
from collections import Counter, defaultdict, namedtuple
from itertools import combinations, count, permutations, product
from pprint import pprint
import numpy as np

download(2021, 19)
with open('aoc2021_19input.txt') as inputfile:
    data = inputfile.read()

test1 = '''--- scanner 0 ---
0,2
4,1
3,3

--- scanner 1 ---
-1,-1
-5,0
-2,1'''

test2 = '''--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14'''

#data = test2
#print(data)

class Scanner:
    
    def __init__(self, beacons, name):
        self.beacons = beacons
        self.name = name
        self.relative_to = name
    
    def __iter__(self):
        return iter(self.beacons)


class Beacon:
    
    def __init__(self, pos, origin, name=None):
        self.relpos = pos
        self.vectors = set()
        self._abspos = None
        self.name = name
        self.origin = origin
        self.relative_scanner = origin
    
    def __repr__(self):
        return f'Beacon({self.relpos}, {self._abspos}, {self.origin}, {self.relative_scanner}, {self.name})'
    
    @property
    def abspos(self):
        return self._abspos if self._abspos is not None else self.relpos

ConversionVectorGroup = namedtuple('ConversionVectorGroup', 'transformer rotater difference')

scanners = [Scanner([Beacon(np.array([int(axis) for axis in line.split(',')]), i) for line in scanner.splitlines()[1:]], i) for i, scanner in enumerate(data.split('\n\n'))]
for i, scanner in enumerate(scanners):
    scanner.beacons.append(Beacon(np.array([0, 0, 0]), i, 'scanner'))
#print(scanners)
for scanner in scanners:
    #for first, second in permutations(scanner, 2):
    for beacon in scanner:
        for other in scanner:
            if other is beacon:
                continue
            beacon.vectors.add(frozenset(abs(other.relpos - beacon.relpos)))
#print(scanners)

transformers = list(np.array(t) for t in product((-1,1), repeat=len(beacon.relpos)))

rotaters = list(np.array(permutation) for permutation in permutations(range(len(beacon.relpos))))

'''def reversed_conversion_vector_group(conversion):
    return ConversionVectorGroup(
        tuple(conversion.transformer), 
        tuple(np.array(conversion.rotater)[np.array(conversion.rotater)]), 
        tuple(-np.array(conversion.difference))
        )'''

'''names = count(1)
for beacon in scanners[0]:
    beacon.name = next(names)
    beacon._abspos = beacon.relpos'''

#scanner_conversion_table = defaultdict(dict)
while not all(scanner.relative_to == 0 for scanner in scanners):
    for scanner1, scanner2 in combinations(scanners, 2):
        # Only use matches where one scanner has been normalised
        if 0 not in (scanner.relative_to for scanner in (scanner1, scanner2)) or scanner1.relative_to == scanner2.relative_to:
            continue
        if scanner2.relative_to == 0:
            scanner1, scanner2 = scanner2, scanner1
        pair = False
        counter = Counter()
        for beacon1 in scanner1:
            for beacon2 in scanner2:
                overlap = beacon1.vectors & beacon2.vectors
                if len(overlap) >= 11:
                    pair = True
                    for transformer in transformers:
                        for rotater in rotaters:
                            beacon2variant = transformer * beacon2.relpos[rotater]
                            conversion_vector_group = ConversionVectorGroup(tuple(transformer), tuple(rotater), tuple(beacon1.abspos - beacon2variant))
                            counter[conversion_vector_group] += 1
                    #vector = beacon1.relpos - beacon2.relpos
                    #print(vector)
                    #print(vector_variants)
                    '''if beacon1.name:
                        beacon2.name = beacon1.name
                        #beacon2.abspos = beacon1.abspos
                    elif beacon2.name:
                        beacon1.name = beacon2.name
                        #beacon1.abspos = beacon2.abspos
                    else:
                        beacon1.name = next(names)
                        beacon2.name = beacon1.name'''
                    #print(beacon1, beacon2)
        if pair:
            #pprint(counter.most_common())
            conversion = counter.most_common()[0][0]
            #scanner_conversion_table[j][i] = conversion
            #scanner_conversion_table[i][j] = reversed_conversion_vector_group(conversion)
            for beacon in scanner2:
                beacon._abspos = (np.array(conversion.transformer) * beacon.relpos[np.array(conversion.rotater)]) + np.array(conversion.difference)
                beacon.relative_scanner = 0
            scanner2.relative_to = 0

#pprint(scanners)

#pprint(scanner_conversion_table)

"""while sum([0 in tos.keys() for tos in scanner_conversion_table.values()]) < len(scanners) - 1:
    #print('a')
    for first, seconds in scanner_conversion_table.copy().items():
        #print('b')
        #print(first, seconds)
        if first == 0 or 0 in seconds.keys():
            continue
        for second, conversion1 in seconds.copy().items():
            #print('c')
            #print(second, conversion1)
            for third, conversion2 in scanner_conversion_table[second].items():
                #print('d')
                #print(third, conversion2)
                if third == first:
                    continue
                combined = (np.array(conversion1.transformer) * np.array(conversion2.transformer), np.array(conversion1.rotater)[np.array(conversion2.rotater)], np.array(conversion1.difference) + np.array(conversion2.difference))
                existing_combined = scanner_conversion_table[first].get(third, None)
                combined = ConversionVectorGroup(*[tuple(part) for part in combined])
                #print(combined)
                #print(existing_combined)
                reverse = reversed_conversion_vector_group(conversion)
                existing_reverse = scanner_conversion_table[third].get(first, None)
                #if existing_combined is not None:
                    #assert np.all(existing_combined == combined), f'{existing_combined} != {combined}'
                #if existing_reverse is not None:
                    #assert np.all(existing_reverse == reverse), f'{existing_reverse} != {reverse}'
                scanner_conversion_table[first][third] = combined
                scanner_conversion_table[third][first] = reverse
                #pprint(scanner_conversion_table)
                
for item in scanner_conversion_table.items():
    pprint(item)

for scanner in scanners:
    for beacon in scanner:
        if beacon.origin != 0:
            conversion = scanner_conversion_table[beacon.origin][0]
            beacon._abspos = (np.array(conversion.transformer) * beacon.relpos[np.array(conversion.rotater)]) + np.array(conversion.difference)
            beacon.relative_scanner = 0"""

#pprint(scanners)
#print(sum([beacon.name is None for scanner in scanners for beacon in scanner]))

#print(len(set(beacon.name for scanner in scanners for beacon in scanner)))

print(len(set(tuple(beacon.abspos) for scanner in scanners for beacon in scanner)) - len(scanners))


print(max(sum(abs(beacon1.abspos - beacon2.abspos)) for beacon1, beacon2 in combinations((beacon for scanner in scanners for beacon in scanner if beacon.name == 'scanner'), 2)))
