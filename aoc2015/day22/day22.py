#!/usr/bin/python3
# Advent of code 2015 day 21
# See https://adventofcode.com/2015/day/21
import dataclasses
from dataclasses import dataclass


@dataclass
class Boss:
    name: str
    hp: int
    damage: int

    def attack(self, other):
        other.hp -= max(1, self.damage - other.armor)


@dataclass
class Wizard:
    name: str
    hp: int
    mana: int
    armor: int = 0

    shield_ticks: int = 0
    poison_ticks: int = 0
    recharge_ticks: int = 0
    mana_spent: int = 0

    def missile(self, other):
        if self.mana < 53:
            return False
        self.mana -= 53
        self.mana_spent += 53
        other.hp -= 4
        return True

    def drain(self, other):
        if self.mana < 73:
            return False
        self.mana -= 73
        self.mana_spent += 73
        other.hp -= 2
        self.hp += 2
        return True

    def shield(self):
        if self.mana < 113 or self.shield_ticks > 0:
            return False
        self.mana -= 113
        self.mana_spent += 113
        self.shield_ticks = 6
        self.armor += 7
        return True

    def poison(self):
        if self.mana < 173 or self.poison_ticks > 0:
            return False
        self.mana -= 173
        self.mana_spent += 173
        self.poison_ticks = 6
        return True

    def recharge(self):
        if self.mana < 229 or self.recharge_ticks > 0:
            return False
        self.mana -= 229
        self.mana_spent += 229
        self.recharge_ticks = 5
        return True

    def tick(self, other):
        if self.recharge_ticks:
            self.recharge_ticks -= 1
            self.mana += 101
        if self.poison_ticks:
            self.poison_ticks -= 1
            other.hp -= 3
        if self.shield_ticks:
            self.shield_ticks -= 1
            if not self.shield_ticks:
                self.armor -= 7


def get_wizard_attack_outcomes(player: Wizard, boss):
    results = []

    new_player = dataclasses.replace(player)
    new_boss = dataclasses.replace(boss)
    if new_player.missile(new_boss):
        results.append((new_player, new_boss))

    new_player = dataclasses.replace(player)
    new_boss = dataclasses.replace(boss)
    if new_player.drain(new_boss):
        results.append((new_player, new_boss))

    new_player = dataclasses.replace(player)
    new_boss = dataclasses.replace(boss)
    if new_player.shield():
        results.append((new_player, new_boss))

    new_player = dataclasses.replace(player)
    new_boss = dataclasses.replace(boss)
    if new_player.poison():
        results.append((new_player, new_boss))

    new_player = dataclasses.replace(player)
    new_boss = dataclasses.replace(boss)
    if new_player.recharge():
        results.append((new_player, new_boss))

    return results


# Perform breadth-first search for best victory
states = [(Wizard(name="player", hp=50, mana=500), Boss(name="boss", hp=55, damage=8))]
min_mana_spent = 10000000
while states:
    next_states = []
    for wizard, boss in states:
        # Part 2 only
        # wizard.hp -= 1
        # if wizard.hp <= 0:
        #     continue

        # Wizard's turn - try all the the different possible spells
        wizard.tick(boss)
        for next_wizard, next_boss in get_wizard_attack_outcomes(wizard, boss):
            if next_boss.hp <= 0:
                # Wizard won: check mana spent
                min_mana_spent = min(min_mana_spent, next_wizard.mana_spent)
                continue
            if next_wizard.mana_spent > min_mana_spent:
                # Used too much mana to improve on best result - ignore this outcome
                continue

            # Boss' retaliation
            next_wizard.tick(next_boss)
            next_boss.attack(next_wizard)
            if next_wizard.hp <= 0:
                # Boss won - ignore this outcome
                continue

            # Battle continue from new states next roundretaliation
            next_states.append((next_wizard, next_boss))

    states = next_states

print(min_mana_spent)
