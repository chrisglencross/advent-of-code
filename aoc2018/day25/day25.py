with open("input", "r") as f:
    lines = f.readlines()

stars = []
constellations_by_star = dict()
for line in lines:
    star = tuple([int(n) for n in line.split(",")])
    stars.append(star)
    constellations_by_star[star] = {star}


def is_near(star1, star2):
    return abs(star1[0] - star2[0]) + abs(star1[1] - star2[1]) + abs(star1[2] - star2[2]) + abs(
        star1[3] - star2[3]) <= 3


def combine_constellations(star1, star2):
    c1 = constellations_by_star[star1]
    c2 = constellations_by_star[star2]
    if c1 == c2:
        return False
    c = c1.union(c2)
    for s in c:
        constellations_by_star[s] = c
    return True


modified = True
while modified:
    modified = False
    for star1 in stars:
        for star2 in stars:
            if star1 == star2:
                continue
            if is_near(star1, star2):
                modified = combine_constellations(star1, star2) or modified

# Print distinct constellation count
distinct_constellations = set([tuple(x) for x in constellations_by_star.values()])
print(len(distinct_constellations))
