from collections import namedtuple
from itertools import combinations, product

Item = namedtuple('Item', 'cost damage armor')

class Character:
    
    def __init__(self, name, hp=0, damage=0, armor=0):
        self.name = name
        self.hp = hp
        self.damage = damage
        self.armor = armor

    def equip(self, items):
        for item in items:
            self.damage += item.damage
            self.armor += item.armor

def damage(attacker, defender):
    return max(attacker.damage - defender.armor, 1)

def fight(me, boss):
    attacker, defender = boss, me
    while me.hp > 0 and boss.hp > 0:
        attacker, defender = defender, attacker
        defender.hp -= damage(attacker, defender)
    return attacker.name

def total_cost(items):
    #print(items)
    return sum(item.cost for item in items)

weapons = [Item(8, 4, 0), Item(10, 5, 0), Item(25, 6, 0), Item(40, 7, 0), Item(74, 8, 0)]

armors = [Item(0, 0, 0), Item(13, 0, 1), Item(31, 0, 2), Item(53, 0, 3), Item(75, 0, 4), Item(102, 0, 5)]

ring_pairs = [Item(0, 0, 0), Item(25, 1, 0), Item(50, 2, 0), Item(100, 3, 0), Item(20, 0, 1), Item(40, 0, 2), Item(80, 0, 3)]
ring_pairs = list(combinations(ring_pairs, 2)) + [(Item(0, 0, 0), Item(0, 0, 0))]

if __name__ == '__main__':
    item_combos = ((weapon, armor, *rings) for weapon, armor, rings in product(weapons, armors, ring_pairs))
    item_combos = sorted(item_combos, key = total_cost, reverse=True)
    
    for item_combo in item_combos:
        boss = Character('boss', 100, 8, 2)
        me = Character('me', 100, 0, 0)
        me.equip(item_combo)
        winner = fight(me, boss)
        if winner != 'me':
            print(total_cost(item_combo))
            break
