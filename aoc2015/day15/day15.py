#!/usr/bin/python3
# Advent of code 2015 day 15
# See https://adventofcode.com/2015/day/15

from dataclasses import dataclass


@dataclass
class Ingredient:
    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int


ingredients = [
    Ingredient(name="Frosting", capacity=4, durability=-2, flavor=0, texture=0, calories=5),
    Ingredient(name="Candy", capacity=0, durability=5, flavor=-1, texture=0, calories=8),
    Ingredient(name="Butterscotch", capacity=-1, durability=0, flavor=5, texture=0, calories=6),
    Ingredient(name="Sugar", capacity=0, durability=0, flavor=-2, texture=2, calories=1)
]


def get_mix(i):
    i1 = i // (101 * 101)
    i2 = i // 101 % 101
    i3 = i % 101
    if i1 + i2 + i3 > 100:
        return None
    else:
        return (i1, i2, i3, 100 - (i1 + i2 + i3))


best_recipe = None
best_score = 0
for i in range(101 * 101 * 101):
    if (mix := get_mix(i)) is not None:
        recipe = Ingredient(name=f"{mix}", capacity=0, durability=0, flavor=0, texture=0, calories=0)
        for qty, ingredient in zip(mix, ingredients):
            recipe.capacity += qty * ingredient.capacity
            recipe.durability += qty * ingredient.durability
            recipe.flavor += qty * ingredient.flavor
            recipe.texture += qty * ingredient.texture
            recipe.calories += qty * ingredient.calories
        score = max(0, recipe.capacity) * max(0, recipe.durability) * max(0, recipe.flavor) * max(0, recipe.texture)
        if score > best_score and recipe.calories == 500:
            best_score = score
            best_recipe = recipe
print(best_score)
