data = '''Frosting: capacity 4, durability -2, flavor 0, texture 0, calories 5
Candy: capacity 0, durability 5, flavor -1, texture 0, calories 8
Butterscotch: capacity -1, durability 0, flavor 5, texture 0, calories 6
Sugar: capacity 0, durability 0, flavor -2, texture 2, calories 1'''

test_data = '''Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3'''

#data = test_data

from collections import defaultdict
from itertools import combinations_with_replacement

ingredient_properties = defaultdict(dict)
for line in data.splitlines():
    ingredient, properties = line.split(': ')
    for info in properties.split(', '):
        property, value = info.split()
        ingredient_properties[ingredient][property] = int(value)

highest_score = 0
for recipe in combinations_with_replacement(ingredient_properties, 100):
    score = 1
    for property in ('capacity', 'durability', 'flavor', 'texture'):
        score *= max(0, sum(recipe.count(ingredient) * ingredient_properties[ingredient][property] for ingredient in ingredient_properties))
    calories = sum(recipe.count(ingredient) * ingredient_properties[ingredient]['calories'] for ingredient in ingredient_properties)
    if calories == 500:
        highest_score = max(highest_score, score)
print(highest_score)
