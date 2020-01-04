#!/usr/bin/python3
# Advent of code 2015 day 21
# See https://adventofcode.com/2015/day/21

from dataclasses import dataclass


@dataclass
class Character:
    name: str
    hp: int
    damage: int
    armor: int

    def attack(self, other):
        other.hp -= max(1, self.damage - other.armor)


@dataclass
class Item:
    name: str
    cost: int = 0
    damage: int = 0
    armor: int = 0


weapons = [
    Item(name="Dagger", cost=8, damage=4),
    Item(name="Shortsword", cost=10, damage=5),
    Item(name="Warhammer", cost=25, damage=6),
    Item(name="Longsword", cost=40, damage=7),
    Item(name="Greataxe", cost=74, damage=7)
]

armor_items = [
    Item(name="No armor", cost=0, armor=0),
    Item(name="Leather", cost=14, armor=1),
    Item(name="Chainmail", cost=31, armor=2),
    Item(name="Splintmail", cost=53, armor=3),
    Item(name="Bandedmail", cost=75, armor=4),
    Item(name="Platemail", cost=102, armor=5),
]

rings = [
    Item(name="No Ring 1", cost=0),
    Item(name="No Ring 2", cost=0),
    Item(name="Damage +1", cost=25, damage=1),
    Item(name="Damage +2", cost=50, damage=2),
    Item(name="Damage +3", cost=100, damage=3),
    Item(name="Defense +1", cost=20, armor=1),
    Item(name="Defense +2", cost=40, armor=2),
    Item(name="Defense +3", cost=80, armor=3),
]


def fight(player, boss):
    while True:
        player.attack(boss)
        if boss.hp <= 0:
            return True
        boss.attack(player)
        if player.hp <= 0:
            return False


max_cost = -1
min_cost = 100000

for weapon in weapons:
    for armor in armor_items:
        for ring1 in rings:
            for ring2 in rings:
                if ring1 == ring2:
                    continue
                items = [weapon, armor, ring1, ring2]
                cost = sum([item.cost for item in items])
                if min_cost < cost < max_cost:
                    # Not interesting - cannot affect min cost or max cost
                    continue
                player_damage = sum([item.damage for item in items])
                player_armor = sum([item.armor for item in items])
                boss = Character(name="boss", hp=109, damage=8, armor=2)
                player = Character(name="player", hp=100, damage=player_damage, armor=player_armor)
                if fight(player, boss):
                    min_cost = min(min_cost, cost)
                else:
                    max_cost = max(max_cost, cost)

print("Part 1:", min_cost)
print("Part 2:", max_cost)
