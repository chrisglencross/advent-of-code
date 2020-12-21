#!/usr/bin/python3
# Advent of code 2020 day 21
# See https://adventofcode.com/2020/day/21

import re

with open("input.txt") as file:
    lines = file.readlines()


def load():
    result = []
    for line in lines:
        match = re.fullmatch(r"(.*) \(contains (.*)\)", line.strip().replace(",", ""))
        ingredients, allergens = [m.split(" ") for m in match.groups()]
        result.append((ingredients, allergens))
    return result


def get_all_ingredients(file):
    return [ingredient for ingredients, allergens in file for ingredient in ingredients]


def get_possible_allergen_ingredients(file):
    result = {}
    for ingredients, allergens in file:
        for allergen in allergens:
            possible_ingredients = result.get(allergen)
            if possible_ingredients is None:
                result[allergen] = set(ingredients)
            else:
                possible_ingredients.intersection_update(ingredients)
    return result


def part1(data):
    all_ingredients = get_all_ingredients(data)
    possible_allergen_ingredients = get_possible_allergen_ingredients(data)
    no_allergens = [ingredient
                    for ingredient in set(all_ingredients)
                    if not any([a for a, i in possible_allergen_ingredients.items() if ingredient in i])]
    print("Part 1:", len([ingredient for ingredient in all_ingredients if ingredient in no_allergens]))


def part2(data):
    possible_allergen_ingredients = get_possible_allergen_ingredients(data)
    # while any allergen has more than one possible ingredient
    while any([a for a, i in possible_allergen_ingredients.items() if len(i) > 1]):
        for allergen, possible_ingredients in possible_allergen_ingredients.items():
            if len(possible_ingredients) == 1:
                ingredient = list(possible_ingredients)[0]
                # this ingredient is definitely source of allergen, remove possibility from all other ingredients
                for other_allergen, other_ingredients in possible_allergen_ingredients.items():
                    if allergen != other_allergen and ingredient in other_ingredients:
                        other_ingredients.remove(ingredient)

    allergens = [(list(i)[0], f) for f, i in possible_allergen_ingredients.items()]
    print("Part 2:", ",".join([p[0] for p in sorted(allergens, key=lambda p: p[1])]))


data = load()
part1(data)
part2(data)
