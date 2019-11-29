import re
from dataclasses import dataclass

with open("input", "r") as f:
    lines = f.readlines()


@dataclass
class Group:
    id: str
    kind: str
    units: int
    hp: int
    attack_damage: int
    attack_type: str
    weak_to: set
    immune_to: set
    initiative: int


def load_groups(boost):
    groups = []
    type = None
    counts = {"immune": 0, "infection": 0}
    for line in lines:
        line = line.strip()
        if line == "Immune System:":
            type = "immune"
        elif line == "Infection:":
            type = "infection"
        elif line == "":
            pass
        else:
            match = re.search(
                "([0-9]+) units each with ([0-9]+) hit points (\(.*\) )?with an attack that does ([0-9]+) (.+) damage at initiative ([0-9]+)",
                line)
            if match:
                counts[type] = counts[type] + 1
                group_id = type + "-" + str(counts[type])
                weak_to = []
                immune_to = []
                if match.group(3):
                    weak_or_immune = match.group(3).replace("(", "").replace(")", "").split(";")
                    for phrase in weak_or_immune:
                        phrase = phrase.strip()
                        if phrase.startswith("weak to "):
                            weak_to.extend(phrase.replace(",", "").split(" ")[2:])
                        elif phrase.startswith("immune to "):
                            immune_to.extend(phrase.replace(",", "").split(" ")[2:])
                        else:
                            raise Exception("Unparseable phrase: " + phrase)

                attack_damage = int(match.group(4))
                if type == "immune":
                    attack_damage = attack_damage + boost
                groups.append(Group(id=group_id,
                                    kind=type,
                                    units=int(match.group(1)),
                                    hp=int(match.group(2)),
                                    attack_damage=attack_damage,
                                    attack_type=match.group(5),
                                    weak_to=set(weak_to),
                                    immune_to=set(immune_to),
                                    initiative=int(match.group(6))))
            else:
                raise Exception("Cannot parse line: " + line)

    # for group in groups:
    #     print(group)
    return groups


def effective_power(group: Group):
    return group.units * group.attack_damage


def get_attack_damage(attacker: Group, defender: Group):
    if attacker.attack_type in defender.immune_to:
        return 0
    attack_damage = effective_power(attacker)
    if attacker.attack_type in defender.weak_to:
        attack_damage = attack_damage * 2
    return attack_damage


def select_targets(groups: list):
    groups.sort(key=lambda group: effective_power(group) * 1000 + group.initiative, reverse=True)
    result = []
    targeted_defenders = []
    for attacker in groups:

        # Find enemies
        targets = [defender for defender in groups if defender.kind != attacker.kind]
        if not targets:
            continue

        # Remove the targets which have already been targeted
        targets = [defender for defender in targets if defender not in targeted_defenders]
        if not targets:
            continue

        # for target in targets:
        #    print(f"{attacker.id} would deal {target.id} {get_attack_damage(attacker, target)} damage")

        # Find the target to which we can do most damage
        max_attack_damage = max([get_attack_damage(attacker, target) for target in targets])
        targets = [target for target in targets if get_attack_damage(attacker, target) == max_attack_damage]
        if not targets:
            continue

        # In case of a tie, pick the target with the largest effective power
        max_effective_power = max([effective_power(target) for target in targets])
        targets = [target for target in targets if effective_power(target) == max_effective_power]
        if not targets:
            continue

        # In case of a tie, pick the target with the largest initiative
        max_initiative = max([target.initiative for target in targets])
        targets = [target for target in targets if target.initiative == max_initiative]
        if not targets:
            continue

        if len(targets) > 1:
            raise Exception("Ambiguous target")
        else:
            defender = targets[0]
            if get_attack_damage(attacker, defender) > 0:
                targeted_defenders.append(defender)
                result.append((attacker, defender))

    # print()
    return result


def attack(attacker, defender):
    damage = get_attack_damage(attacker, defender)
    units_destroyed = damage // defender.hp
    if units_destroyed > defender.units:
        units_destroyed = defender.units
    defender.units = defender.units - units_destroyed
    print(f"{attacker.id} attacks {defender.id}, killing {units_destroyed} units, leaving {defender.units}")
    return units_destroyed


def play_game(boost):
    g = load_groups(boost)
    while True:
        target_pairs = select_targets(g)
        if not target_pairs:
            break
        target_pairs.sort(key=lambda pair: pair[0].initiative, reverse=True)
        total_units_destroyed = 0
        for target_pair in target_pairs:
            if target_pair[0].units > 0:
                total_units_destroyed = total_units_destroyed + attack(target_pair[0], target_pair[1])
        g = [group for group in g if group.units > 0]
        if total_units_destroyed == 0:
            print("Stalemate")
            break
        print()
    return g


for boost in range(70, 1570):
    print(f"Boost: {boost}")
    g = play_game(boost)
    print("Survivors:")
    for group in g:
        print(group)
    if len([group for group in g if group.kind == "infection"]) == 0:
        break

print(sum([group.units for group in g]))
