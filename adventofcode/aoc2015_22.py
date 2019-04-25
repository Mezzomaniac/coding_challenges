from collections import namedtuple
from queue import PriorityQueue

Spell = namedtuple('Spell', 'name cost damage hp armor mana turns')

spells = (Spell('magic missile', 53, 4, 0, 0, 0, 1), Spell('drain', 73, 2, 2, 0, 0, 1), Spell('shield', 113, 0, 0, 7, 0, 6), Spell('poison', 173, 3, 0, 0, 0, 6), Spell('recharge', 229, 0, 0, 0, 101, 5))

hard = True

def fight(game_state, new_spell):
    game_state['mana'] -= new_spell.cost
    game_state[new_spell.name] = new_spell.turns
    for turn in range(2):
        if turn:
            game_state['me'] -= 9 - game_state['armor']
            if game_state['me'] <= 0:
                return game_state
        elif hard:
            game_state['me'] -= 1
        game_state['armor'] = 0
        for spell in spells:
            #print(spell.name)
            if not game_state[spell.name]:
                continue
            game_state['boss'] -= spell.damage
            game_state['me'] += spell.hp
            game_state['armor'] += spell.armor
            game_state['mana'] += spell.mana
            game_state[spell.name] -= 1
    return game_state

wins = set()
frontier = PriorityQueue()
start = ()
game_state = {'boss': 58, 'me': 50, 'armor': 0, 'mana': 500, 'magic missile': 0, 'drain': 0, 'shield': 0, 'poison': 0, 'recharge': 0}
mana_used = 0
game_states = {start: game_state}
cost_so_far = {start: mana_used}
frontier.put((mana_used, start))
done = False
while not frontier.empty() and not done:
    current = frontier.get()[1]
    #print([spell.name for spell in current])
    #print(game_states[current])
    for spell in spells:
        #print(spell.name)
        game_state = game_states[current].copy()
        if game_state[spell.name] or spell.cost > game_state['mana']:
            continue
        cost = cost_so_far[current] + spell.cost
        game_state = fight(game_state, spell)
        if game_state['boss'] <= 0:
            print(cost)
            print(current + (spell,))
            done = True
            break
        elif game_state['me'] <= 0:
            continue
        next = current + (spell,)
        cost_so_far[next] = cost
        game_states[next] = game_state
        frontier.put((cost, next))
    #print()
