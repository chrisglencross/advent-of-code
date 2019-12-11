import hashlib


class Options:
    def __init__(self, options):
        self.options = options
        h = hashlib.sha1()
        self.update_hash(h)
        self.hash = h.digest()

    def __str__(self):
        return f"opt:[{', '.join([str(s) for s in self.options])}]"

    def update_hash(self, h):
        h.update("options".encode())
        for s in self.options:
            if type(s) is str:
                h.update(s.encode())
            else:
                s.update_hash(h)


class Sequence:
    def __init__(self, seq):
        self.seq = seq
        h = hashlib.sha1()
        self.update_hash(h)
        self.hash = h.digest()

    def __str__(self):
        return f"seq:[{', '.join([str(s) for s in self.seq])}]"

    def update_hash(self, h):
        h.update("sequence".encode())
        for s in self.seq:
            if type(s) is str:
                h.update(s.encode())
            else:
                s.update_hash(h)


def find_next_matching(s, symbol, start=0, default=None):
    nested_braces = 0
    for i in range(start, len(s)):
        char = s[i]
        if char == "(":
            nested_braces = nested_braces + 1
        elif char == ")":
            nested_braces = nested_braces - 1
        if char == symbol and nested_braces == 0:
            return i
    return default


def read_regex_sequence(regex):
    sequence = []
    # print(f"Calling read_regex_sequence with {regex}")
    i = 0
    while i < len(regex):
        char = regex[i]
        if char == "(":
            end_brace = find_next_matching(regex, ")", i)
            sequence.append(read_regex(regex[i + 1:end_brace]))
            i = end_brace
        else:
            sequence.append(char)
        i = i + 1
    return Sequence(sequence)


def read_regex(regex):
    # print(f"Calling read_regex with {regex}")
    pipe = find_next_matching(regex, "|", start=0)
    if pipe is None:
        return read_regex_sequence(regex)

    option = read_regex(regex[0:pipe])
    options = [option]
    while pipe is not None:
        next_pipe = find_next_matching(regex, "|", start=pipe + 1)
        if next_pipe is None:
            option = read_regex(regex[pipe + 1:])
        else:
            option = read_regex(regex[pipe + 1:next_pipe])
        options.append(option)
        pipe = next_pipe
    return Options(options)


# Global variables
doors = set()
rooms = set()
visited = set()


def walk_sequence(start_room, sequence):
    # Memoise whether we have visited this location already with an equivalent sequence of instructions
    # Required otherwise this does not complete in reasonable time.
    # Use sha1 hash to compare -- could get collisions, but unlikely and only for a quick hack :-)
    args = (start_room, sequence.hash)
    if args in visited:
        print("Visited this room already with this sequence of instructions; ignoring.")
        return
    visited.add(args)

    rooms.add(start_room)
    steps = list(sequence.seq)
    while len(steps) > 0:
        step = steps[0]
        del steps[0]

        if type(step) is Options:
            for opt in step.options:
                next_sequence = [opt]
                next_sequence.extend(steps)
                walk_sequence(start_room, Sequence(next_sequence))

        elif type(step) is Sequence:
            # If sequence embedded in another sequence, flatten
            new_steps = list(step.seq)
            new_steps.extend(steps)
            steps = new_steps

        elif type(step) is str:
            if step == "N":
                doors.add((start_room[0], start_room[1] - 1))
                next_room = (start_room[0], start_room[1] - 2)
            elif step == "E":
                doors.add((start_room[0] + 1, start_room[1]))
                next_room = (start_room[0] + 2, start_room[1])
            elif step == "S":
                doors.add((start_room[0], start_room[1] + 1))
                next_room = (start_room[0], start_room[1] + 2)
            elif step == "W":
                doors.add((start_room[0] - 1, start_room[1]))
                next_room = (start_room[0] - 2, start_room[1])
            else:
                raise Exception("Unknown direction " + step)

            if next_room not in rooms:
                rooms.add(next_room)
                print(f"Total of {len(rooms)} rooms")
            start_room = next_room

        else:
            raise Exception("Unknown step: " + step)


# Load file into a recursive data structure of steps (strings), sequences, and options
with open("input", "r") as f:
    lines = f.readlines()
i = lines[0].replace("\n", "")
i = i.replace("^", "").replace("$", "")
directions = read_regex(i)
if type(directions) is Options:
    directions = Sequence([directions])

# Walk the directions to build the set of rooms and doors
start_room = (0, 0)
walk_sequence(start_room, directions)
print("All rooms:" + str(rooms))
print("All doors:" + str(doors))

# Dijkstra(-ish?) algorithm for finding the shortest distance to every room
# (First wrote one of these for my GCSE computing project on the BBC micro in 1988)
shortest_dist = dict()
shortest_dist[start_room] = 0

directions = [
    (0, -1), (-1, 0), (1, 0), (0, 1)
]

# dirty_rooms is the set of rooms where we need to look for neighbours
dirty_rooms = {start_room}
while len(dirty_rooms) > 0:
    next_dirty_rooms = set()
    for room in dirty_rooms:
        dist = shortest_dist[room]
        for direction in directions:
            direction_has_door = (room[0] + direction[0], room[1] + direction[1]) in doors
            if direction_has_door:
                # Get the neighbour room
                next_room = (room[0] + 2 * direction[0], room[1] + 2 * direction[1])
                next_room_dist = shortest_dist.get(next_room)
                if next_room_dist is None or next_room_dist > dist + 1:
                    # We've found a new shortest route to this neighbour room
                    # Mark the room as dirty so that we recheck its neighbours
                    shortest_dist[next_room] = dist + 1
                    next_dirty_rooms.add(next_room)
    dirty_rooms = next_dirty_rooms

print(max(shortest_dist.values()))
print(len([value for value in shortest_dist.values() if value >= 1000]))
