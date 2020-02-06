data = '''2 WZMS, 3 NPNFD => 5 SLRGD
4 QTFCJ, 1 RFZF => 1 QFQPN
2 LCDPV => 6 DGPND
1 MVSHM, 3 XSDR, 1 RSJD => 6 GNKB
6 XJRML, 1 LCDPV => 7 HTSJ
3 LQBX => 3 GKNTG
2 NZMLP, 5 FTNZQ => 2 QSLTQ
8 WZMS, 4 XSDR, 2 NPNFD => 9 CJVT
16 HFHB, 1 TRVQG => 8 QTBQ
177 ORE => 7 DNWGS
10 ZJFM, 4 MVSHM => 8 LCDPV
1 LTVKM => 5 ZJFM
5 QFJS => 6 LTVKM
4 CZHM, 12 CJVT => 9 PGMS
104 ORE => 8 QCGM
1 JWLZ, 5 QTFCJ => 4 DHNL
20 VKRBJ => 3 FQCKM
1 FTNZQ, 1 QSLTQ => 4 HFHB
1 JLPVD => 2 JGJFQ
12 PTDL => 1 LVPK
31 JGJFQ, 5 PGMS, 38 PTDL, 1 PGCZ, 3 LVPK, 47 JGHWZ, 21 LVPJ, 27 LTVKM, 5 ZDQD, 5 LCDPV => 1 FUEL
6 WFJT, 2 VKRBJ => 8 NZMLP
21 HNJW, 3 NXTL, 8 WZMS, 5 SLRGD, 2 VZJHN, 6 QFQPN, 5 DHNL, 19 RNXQ => 2 PGCZ
1 QTBQ, 3 MVSHM => 1 XSDR
25 ZKZNB => 9 VZJHN
4 WHLT => 9 PHFKW
29 QPVNV => 9 JGHWZ
13 ZJFM => 2 RNXQ
1 DGPND, 12 PHFKW => 9 BXGXT
25 ZJFM => 6 WHLT
3 QPVNV => 9 BTLH
1 KXQG => 8 TRVQG
2 JWLZ => 8 JLPVD
2 GKNTG => 6 NXTL
28 VKRBJ => 2 DXWSH
126 ORE => 7 VKRBJ
11 WHLT => 8 QTFCJ
1 NZMLP, 1 DNWGS, 8 VKRBJ => 5 XJRML
16 XJRML => 6 SKHJL
3 QTFCJ, 6 ZTHWQ, 15 GKNTG, 1 NXRZL, 1 DGBRZ, 1 SKHJL, 1 VZJHN => 7 LVPJ
1 HFHB, 16 QTBQ, 7 XJRML => 3 NPNFD
2 TRVQG => 4 JWLZ
8 GKNTG, 1 NSVG, 23 RNXQ => 9 NXRZL
3 QTFCJ => 6 CZHM
2 NPNFD => 8 JQSTD
1 DXWSH, 1 DGPND => 4 DGBRZ
3 DXWSH, 24 QFJS, 8 FTNZQ => 8 KXQG
6 FXJQX, 14 ZKZNB, 3 QTFCJ => 2 ZTHWQ
31 NSVG, 1 NXRZL, 3 QPVNV, 2 RNXQ, 17 NXTL, 6 BTLH, 1 HNJW, 2 HTSJ => 1 ZDQD
5 RNXQ, 23 BXGXT, 5 JQSTD => 7 QPVNV
8 NPNFD => 7 WZMS
6 KXQG => 7 ZDZM
129 ORE => 9 WFJT
9 NZMLP, 5 FQCKM, 8 QFJS => 1 LQBX
170 ORE => 9 GDBNV
5 RSJD, 3 CZHM, 1 GNKB => 6 HNJW
14 HTSJ => 7 FXJQX
11 NPNFD, 1 LCDPV, 2 FXJQX => 6 RSJD
9 DGBRZ => 6 ZKZNB
7 GDBNV, 1 QCGM => 8 QFJS
2 QFQPN, 5 JWLZ => 4 NSVG
8 QFJS, 1 ZDZM, 4 QSLTQ => 7 MVSHM
1 LTVKM => 8 RFZF
4 DNWGS => 3 FTNZQ
6 VZJHN => 9 PTDL'''

from collections import defaultdict
from queue import LifoQueue

accelerator = 10000

reactions = defaultdict(dict)
for line in data.splitlines():
    inputs, output = line.split(' => ')
    inputs = [(int(input.split()[0] ) * accelerator, input.split()[1]) for input in inputs.split(', ')]
    quantity, product = output.split()
    reactions[product]['quantity'] = int(quantity) * accelerator
    reactions[product]['inputs'] = inputs
#print(reactions)

def decelerate():
    for product in reactions:
        reactions[product]['quantity'] //= 10
        reactions[product]['inputs'] = [(quantity // 10, product) for quantity, product in reactions[product]['inputs']]

ore_consumed = 0
available = defaultdict(int)
available['ORE'] = 1_000_000_000_000
fuel_produced = 0
production_queue = LifoQueue()
#production_queue.put((1, 'FUEL'))
#while not available.get('FUEL', 0):
#powersof10 = [10 ** x for x in range(12, 1, -1)]
#decelerated = False
while available['ORE']:
    '''if ore_consumed > powersof10[-1]:
        #print('power')
        print(ore_consumed, available['FUEL'])
        powersof10 = powersof10[:-1]
        #print(available)
        #print(production_queue.queue)
        #print()
    #if not decelerated and available['ORE'] <= 201324 * accelerator * 2:
    if not decelerated and available['FUEL'] >= 6323000:
        for product in reactions:
            reactions[product]['quantity'] //= accelerator
            reactions[product]['inputs'] = [(quantity // accelerator, product) for quantity, product in reactions[product]['inputs']]
        decelerated = True
        print('decelerated')
        print(ore_consumed, available['FUEL'])
        #print(available)
        #print(production_queue.queue)
        #print()
    #if available['FUEL'] > 4967117:
    elif decelerated and not available['FUEL'] % 100 and available['FUEL'] > fuel_produced:
        fuel_produced = available['FUEL']
        #print('fuel')
        print(ore_consumed, available['FUEL'])
        print(available)
        #print(production_queue.queue)
        print()'''
    if available['ORE'] < accelerator * 10_000_000 and accelerator > 1:
        decelerate()
        accelerator //= 10
        print(accelerator)
        print(ore_consumed, available['FUEL'])
        print(available)
        print(production_queue.queue)
        print()
    '''if available['FUEL'] == 1:
        print(available)
        print()
        #if not any(quantity for product, quantity in available.items() if product not in ('ORE', 'FUEL')):
            #print(ore_consumed, available['FUEL'])
        #per_fuel_state = available.copy()
        multiplier = 1_000_000_000_000 // ore_consumed# - 100
        available['ORE'] = 1_000_000_000_000 - ore_consumed * multiplier
        for product in available:
            if product == 'ORE':
                continue
            available[product] *= multiplier
        print(available)
        print()'''
    if production_queue.empty():
        production_queue.put((1, 'FUEL'))
    quantity_needed, current = production_queue.get()
    #print(current)
    if current == 'ORE':
        break
        ore_consumed += quantity_needed
        available['ORE'] += quantity_needed
    elif all(available.get(reagent, 0) >= quantity for quantity, reagent in reactions[current]['inputs']):
        for quantity, reagent in reactions[current]['inputs']:
            available[reagent] -= quantity
        available[current] += reactions[current]['quantity']
        ore_consumed = 1_000_000_000_000 - available['ORE']
    else:
        production_queue.put((quantity_needed, current))
        for quantity, reagent in reactions[current]['inputs']:
            if available.get(reagent, 0) < quantity:
                production_queue.put((quantity - available.get(reagent, 0), reagent))
#print(available['ORE'])
print(available['FUEL'])  # >6326578; != 6326855
#6326832? 6326857?
print(available)

'''177 0
1009 0
10130 0
100162 0
1000053 6
10000045 63
100000016 632
1000000093 6326'''