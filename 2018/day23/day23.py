import re
import sys

sys.setrecursionlimit(2000)

with open("input") as f:
    lines = f.readlines()

bots = []

for id, line in enumerate(lines):
    match = re.search("^pos=<([-0-9]+),([-0-9]+),([-0-9]+)>, r=([0-9]+)$", line.strip())
    p = (int(match.group(1)), int(match.group(2)), int(match.group(3)))
    r = int(match.group(4))
    bots.append((p, r, id))

print(bots)

# Part 1

max_r = max([bot[1] for bot in bots])
strong_bot = [bot for bot in bots if bot[1] == max_r][0]
print(strong_bot)
print(max_r)


def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + abs(p1[2] - p2[2])


def bots_in_range(from_bot):
    return [bot for bot in bots if distance(bot[0], from_bot[0]) <= max_r]


print(len(bots_in_range(strong_bot)))


# Part 2

def intersect(bot1, bot2):
    return distance(bot1[0], bot2[0]) <= bot1[1] + bot2[1]


def get_intersection_count(x, y, z):
    return len([bot for bot in bots if distance(bot[0], (x, y, z)) <= bot[1]])


bot_intersections = dict()
for from_bot in bots:
    intersections = set()
    for to_bot in bots:
        if from_bot != to_bot and intersect(from_bot, to_bot):
            intersections.add(to_bot)
    bot_intersections[from_bot] = intersections


# create list of intersections with the bots they contain
def get_neighbours(node):
    return bot_intersections[node]


# Finds maximal cliques - these are the bots that we should be in range of
def bronk(clique, remaining_vertices, ignore_vertices):
    if not any((remaining_vertices, ignore_vertices)):
        yield clique
    for v in remaining_vertices[:]:
        new_vertices = clique + [v]
        new_remaining_vertices = [v1 for v1 in remaining_vertices if v1 in get_neighbours(v)]
        new_ignore_vertices = [v1 for v1 in ignore_vertices if v1 in get_neighbours(v)]
        for max_clique in bronk(new_vertices, new_remaining_vertices, new_ignore_vertices):
            yield max_clique
        remaining_vertices.remove(v)
        ignore_vertices.append(v)


results = bronk([], bots, [])

# Get the first result - maximal clique.
for result in results:
    break

# Search to find the coordinates where we are in the maximal clique
min_x = max([node[0][0] - node[1] for node in result])
max_x = min([node[0][0] + node[1] for node in result])
min_y = max([node[0][1] - node[1] for node in result])
max_y = min([node[0][1] + node[1] for node in result])
min_z = max([node[0][2] - node[1] for node in result])
max_z = min([node[0][2] + node[1] for node in result])

# Start somewhere near the middle of the spheres we are interested in
start_x = (max_x + min_x) // 2
start_y = (max_y + min_y) // 2
start_z = (max_z + min_z) // 2


def get_mismatches(coords):
    return [bot for bot in result if distance(bot[0], coords) > bot[1]]


# Find the spheres which we are expected to be within but are not, and move towards their centres. Distance
# to move should take us approximately to the outer radius of the sphere.
coords = (start_x, start_y, start_z)
visited_already = set([])
while True:
    mismatched_bots = get_mismatches(coords)
    if len(mismatched_bots) == 0:
        break
    for head_towards in mismatched_bots:
        print(coords)
        print(len(get_mismatches(coords)))
        delta_x = head_towards[0][0] - coords[0]
        delta_y = head_towards[0][1] - coords[1]
        delta_z = head_towards[0][2] - coords[2]
        total_distance = abs(delta_x) + abs(delta_y) + abs(delta_z)
        # Distance to move to reach edge
        distance_to_move = total_distance - head_towards[1] + 1
        # print(distance_to_move)
        fraction_to_move = (distance_to_move / total_distance)  # float
        old_coords = coords
        coords = (
            coords[0] + int(round(delta_x * fraction_to_move)), coords[1] + int(round(delta_y * fraction_to_move)),
            coords[2] + int(round(delta_z * fraction_to_move)))
        print(f"Heading from {old_coords} to {coords} to get closer to {head_towards}")
    if coords in visited_already:
        break  # Bouncing around in the local neighbourhood because of float rounding errors
    visited_already.add(coords)


def get_move_dir(x, distance):
    if x < 0:
        return x + distance
    if x == 0:
        return x
    return x - distance


# We're pretty close - now scan the local 20x20x20 neighbourhood
approx = coords
print(len(get_mismatches(approx)))
best_match = None
for x in range(-10, 10):
    for y in range(-10, 10):
        for z in range(-10, 10):
            coords = (x + approx[0], y + approx[1], z + approx[2])
            if len(get_mismatches(coords)) == 0:
                print("Found match")
                if best_match is None or distance((0, 0, 0), coords) < distance((0, 0, 0), best_match):
                    print(x, y, x)
                    best_match = coords
                    print("Best Match: " + str(best_match))
                    print("Distance: " + distance((0, 0, 0), best_match))
