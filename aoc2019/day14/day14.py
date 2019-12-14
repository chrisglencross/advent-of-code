#!/usr/bin/python3
# Advent of code 2019 day 14

import re
from dataclasses import dataclass
from typing import List


@dataclass
class Recipe:
    name: str
    product: str
    product_quantity: int
    requires: dict


def load_recipes():
    with open("input.txt") as f:
        lines = f.readlines()
    recipes = {}
    for line in lines:
        match = re.search("^(.*) => ([0-9]+) ([A-Z]+)$", line.strip())
        if match:
            ingredients = match.group(1)
            requires = {}
            for ingredient in ingredients.split(", "):
                parts = ingredient.split(" ")
                requires[parts[1]] = int(parts[0])
            produces_qty = int(match.group(2))
            produces = match.group(3)
            recipes[produces] = Recipe(line.strip(), produces, produces_qty, requires)
    return recipes


def build_dependencies(recipes: List[Recipe]):
    result = {}

    for receipe in recipes:
        result[receipe.product] = set([dependency for dependency in receipe.requires.keys()])

    modified = True
    while modified:
        modified = False
        for p, ds in result.items():
            for d in list(ds):
                add = result.get(d, set())
                if not add.issubset(ds):
                    modified = True
                    ds.update(add)

    return result


def get_sorted_products(dependencies):
    sorted_products = ["ORE"]
    remaining = dict(dependencies)
    while remaining:
        for p, ds in dict(remaining).items():
            if set(ds).issubset(sorted_products):
                sorted_products.append(p)
                del remaining[p]
    return sorted_products


def ore_required(fuel_count):
    requirements = {"FUEL": fuel_count}

    for product in sorted_products:

        if product == "ORE":
            continue

        recipe = recipes[product]
        requirement = requirements.get(product, 0)
        use_recipe_times = requirement // recipe.product_quantity
        if (requirement % recipe.product_quantity) > 0:
            use_recipe_times = use_recipe_times + 1  # with a surplus, discarded
        debug_text = []
        for recipe_product, recipe_quantity in recipe.requires.items():
            requirements[recipe_product] = requirements.get(recipe_product, 0) + (recipe_quantity * use_recipe_times)
            debug_text.append(f"{recipe_quantity * use_recipe_times} {recipe_product}")
        # print(f"Consume {', '.join(debug_text)} to produce {requirement} {product}")

    return requirements["ORE"]


# Finds the amount of fuel that can be produced by max_ore using a binary search
def binary_search(max_ore, lo=1, hi=None):
    while hi is None or lo < hi:
        if hi is None:
            # No upper limit yet; try guessing double the previous value
            fuel_guess = lo * 2
        else:
            # Try the mid-point of the lo/hi range
            fuel_guess = (lo + hi) // 2
        ore = ore_required(fuel_guess)
        if ore < max_ore:
            lo = fuel_guess + 1
        elif ore > max_ore:
            hi = fuel_guess
        else:
            return fuel_guess

    # No exact solution, but lo ends up just above the closest match
    return lo - 1


if __name__ == "__main__":
    recipes = load_recipes()
    dependencies = build_dependencies(recipes.values())

    sorted_products = get_sorted_products(dependencies)
    sorted_products.reverse()

    # Part 1
    ore_required_for_one_fuel = ore_required(1)
    print(ore_required_for_one_fuel)

    # Part 2
    print(binary_search(1000000000000))
