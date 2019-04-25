immune_data = '''76 units each with 3032 hit points with an attack that does 334 radiation damage at initiative 7
4749 units each with 8117 hit points with an attack that does 16 bludgeoning damage at initiative 16
4044 units each with 1287 hit points (immune to radiation, fire) with an attack that does 2 fire damage at initiative 20
1130 units each with 11883 hit points (weak to radiation) with an attack that does 78 radiation damage at initiative 14
1698 units each with 2171 hit points (weak to slashing, fire) with an attack that does 11 bludgeoning damage at initiative 12
527 units each with 1485 hit points with an attack that does 26 bludgeoning damage at initiative 17
2415 units each with 4291 hit points (immune to radiation) with an attack that does 17 cold damage at initiative 5
3266 units each with 6166 hit points (immune to cold, slashing; weak to radiation) with an attack that does 17 bludgeoning damage at initiative 18
34 units each with 8390 hit points (immune to cold, fire, slashing) with an attack that does 2311 cold damage at initiative 10
3592 units each with 5129 hit points (immune to cold, fire; weak to radiation) with an attack that does 14 radiation damage at initiative 11'''

infection_data = '''3748 units each with 11022 hit points (weak to bludgeoning) with an attack that does 4 bludgeoning damage at initiative 6
2026 units each with 11288 hit points (weak to fire, slashing) with an attack that does 10 slashing damage at initiative 13
4076 units each with 23997 hit points (immune to cold) with an attack that does 11 bludgeoning damage at initiative 19
4068 units each with 40237 hit points (immune to cold; weak to slashing) with an attack that does 18 slashing damage at initiative 4
3758 units each with 16737 hit points (weak to slashing) with an attack that does 6 radiation damage at initiative 2
1184 units each with 36234 hit points (weak to bludgeoning, fire; immune to cold) with an attack that does 60 radiation damage at initiative 1
1297 units each with 36710 hit points (immune to cold) with an attack that does 47 fire damage at initiative 3
781 units each with 18035 hit points (immune to bludgeoning, slashing) with an attack that does 36 fire damage at initiative 15
1491 units each with 46329 hit points (immune to slashing, bludgeoning) with an attack that does 56 fire damage at initiative 8
1267 units each with 34832 hit points (immune to cold) with an attack that does 49 radiation damage at initiative 9'''

import copy
import re

class Group:
    
    @classmethod
    def from_string(cls, army, string, boost=0):
        regex_main = '(?P<units>\d+).*?(?P<hp>\d+).*?(?P<dam>\d+) (?P<att>\w+).*?(?P<init>\d+)'
        units, hp, damage, attack, initiative = re.match(regex_main, string).groups()
        weaknesses = (); immunities = ()
        try:
            attrs = re.search('(\(.*\))', string).group()[1:-1].split('; ')
        except AttributeError:
            attrs = ''
        for attr in attrs:
            if attr.startswith('w'):
                weaknesses = attr[re.search('weak to ', attr).end():].split(', ')
            else:
                immunities = attr[re.search('immune to ', attr).end():].split(', ')
        return cls(army, int(units), int(hp), int(damage), attack, int(initiative), weaknesses, immunities, boost)
    
    def __init__(self, army, units, hp, damage, attack, initiative, weaknesses=(), immunities=(), boost=0):
        self.army = army
        self.units = units
        self.hp = hp
        self.damage = damage
        self.attack = attack
        self.initiative = initiative
        self.weaknesses = weaknesses
        self.immunities = immunities
        self.boost = boost
        self.targeting = None
        self.targeted = False
    
    def __repr__(self):
        return f'Group({self.army}, {self.units}, {self.hp}, {self.damage}, {self.attack}, {self.initiative}, weaknesses={self.weaknesses}, immunities={self.immunities})'
    
    def effective_power(self):
        return self.units * (self.damage + self.boost)

#immune_system = {Group.from_string('Immune System', line) for line in immune_data.splitlines()}
#infection = {Group.from_string('Infection', line) for line in infection_data.splitlines()}
#print(immune_system)
#print(infection)
#groups = immune_system | infection
#print(len(groups) == len([group.initiative for group in groups]))

def target_selection(groups):
    #print('ts')
    for attacker in sorted(groups, key=lambda a: (a.effective_power(), a.initiative), reverse=True):
        #print(attacker, attacker.effective_power(), attacket.initiative, '\n')
        target = max((group for group in groups if group.units > 0 and group.army != attacker.army and not group.targeted), key=lambda g: (theoretical_damage(attacker, g), g.effective_power(), g.initiative), default=None)
        if target and theoretical_damage(attacker, target):
            attacker.targeting = target
            target.targeted = True
    #for group in groups:
        #print(group, group.targeting, group.targeted, '\n')
        
def theoretical_damage(attacker, defender):
    if attacker.attack in defender.immunities:
        return 0
    return attacker.effective_power() * (1 + (attacker.attack in defender.weaknesses))

def attacking(groups):
    #print('\n', '*'*30, '\n')
    for attacker in sorted(groups.copy(), key=lambda a: a.initiative, reverse=True):
        if attacker.units <= 0 or not attacker.targeting:
            continue
        defender = attacker.targeting
        #print(attacker, defender, '\n')
        defender.units -= theoretical_damage(attacker, defender) // defender.hp
        if defender.units <= 0:
            groups.remove(defender)
    for group in groups:
        group.targeting = None
        group.targeted = False

immune_system = {Group.from_string('Immune System', line) for line in immune_data.splitlines()}
infection = {Group.from_string('Infection', line) for line in infection_data.splitlines()}
boost = 118  #111-114, 116-118 end in a stalemate
winner = 'Infection'
while winner != 'Immune System':
    boost += 1
    print(boost)
    #print('*'*100)
    immune_system_copy = copy.deepcopy(immune_system)
    for group in immune_system_copy:
        group.boost = boost
    infection_copy = copy.deepcopy(infection)
    groups = immune_system_copy | infection_copy
    while len({group for group in groups if group.army == 'Immune System'}) and len({group for group in groups if group.army == 'Infection'}):
        target_selection(groups)
        attacking(groups)
    winner = groups.copy().pop().army
    print(winner)
    print(sum(group.units for group in groups))
    print()
