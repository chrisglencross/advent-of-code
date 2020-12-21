#!/usr/bin/python3
# Advent of code 2020 day 21
# See https://adventofcode.com/2020/day/21

import re

with open("input.txt") as f:
    lines = f.readlines()

all_ingredients = []
possible_allergen_foods = {}
for line in lines:
    match = re.fullmatch(r"(.*) \(contains (.*)\)", line.strip().replace(",", ""))
    food_ingredients, food_allergens = [m.split(" ") for m in match.groups()]
    all_ingredients.extend(food_ingredients)
    for food_allergen in food_allergens:
        possible_foods = possible_allergen_foods.get(food_allergen)
        if possible_foods is None:
            possible_allergen_foods[food_allergen] = set(food_ingredients)
        else:
            possible_foods.intersection_update(food_ingredients)

no_allergens = set()
for ingredient in set(all_ingredients):
    if not any([a for a, i in possible_allergen_foods.items() if ingredient in i]):
        no_allergens.add(ingredient)

print("Part 1:", len([ingredient for ingredient in all_ingredients if ingredient in no_allergens]))

modified = True
while modified:
    modified = False
    for food, possible_allergens in possible_allergen_foods.items():
        if len(possible_allergens) == 1:
            allergen = list(possible_allergens)[0]
            # allergen definitely in this food, remove possibility of this allergen from all other foods
            for other_food, other_food_allergens in possible_allergen_foods.items():
                if food != other_food and allergen in other_food_allergens:
                    other_food_allergens.remove(allergen)
                    modified = True

food_allergens = [(list(i)[0], f) for f, i in possible_allergen_foods.items()]
print("Part 2:", ",".join([p[0] for p in sorted(food_allergens, key=lambda p: p[1])]))
