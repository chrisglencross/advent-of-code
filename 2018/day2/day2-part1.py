import itertools

with open("input") as f:
    lines = f.readlines()
values = [sorted(line.strip()) for line in lines if len(line.strip()) > 0]

two_count = 0
three_count = 0
for value in values:
    has_two = False
    has_three = False
    for k, v in itertools.groupby(value):
        count = 0
        for i in v:
            count = count + 1
        if count == 2:
            has_two = True
        if count == 3:
            has_three = True
    if has_two:
        two_count = two_count + 1
    if has_three:
        three_count = three_count + 1

print(two_count * three_count)
