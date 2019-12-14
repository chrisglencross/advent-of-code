#!/usr/bin/python3
# Advent of code 2019 day 14

import re
from dataclasses import dataclass
from typing import List


@dataclass
class Recipe:
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
            recipes[produces] = Recipe(produces, produces_qty, requires)
    return recipes


def calc_transitive_dependencies(recipes: List[Recipe]):
    """Returns a dict: product -> set of transitive dependency products required to create this product."""
    result = {}

    # Populate result with direct dependencies
    for receipe in recipes:
        result[receipe.product] = set([dependency for dependency in receipe.requires.keys()])

    # Iteratively add missing transitive dependencies to each set of dependencies until no more changes
    # Could be more efficient, but does not need to be.
    modified = True
    while modified:
        modified = False
        for product, dependencies in result.items():
            for dependency in list(dependencies):
                transitive_dependencies = result.get(dependency, set())
                if not transitive_dependencies.issubset(dependencies):
                    modified = True
                    dependencies.update(transitive_dependencies)

    return result


def get_sorted_products(recipes):
    """Returns products in reverse order of manufacture, with ORE at the end and FUEL at the start."""
    sorted_products = ["ORE"]

    dependencies = calc_transitive_dependencies(recipes.values())
    products_to_insert = set(dependencies.keys())

    # Iteratively appends product to the sorted list if all dependencies are already in the list
    while products_to_insert:
        for product in set(products_to_insert):
            if dependencies[product].issubset(sorted_products):
                sorted_products.insert(0, product)
                products_to_insert.remove(product)

    return sorted_products


def ore_required(fuel_count):
    # dictionary of product quantities that we need to produce
    requirements = {"FUEL": fuel_count}

    # produce dependencies in order
    for product in sorted_products:

        # ignore ORE, it has no dependencies
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

        del requirements[product]
        # print(f"Consume {', '.join(debug_text)} to produce {requirement} {product}")

    return requirements["ORE"]


def binary_search(max_ore, lo=1, hi=None):
    """Finds the amount of fuel that can be produced using max_ore with a binary search."""
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
    # Init global variables
    recipes = load_recipes()
    sorted_products = get_sorted_products(recipes)

    # Part 1
    ore_required_for_one_fuel = ore_required(1)
    print(ore_required_for_one_fuel)

    # Part 2
    print(binary_search(1000000000000))
