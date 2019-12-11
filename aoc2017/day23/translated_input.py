# Manually translated to Python from annotated-input.txt
# Took about an hour to convert, through manual inspection and using day23.py as a debugger to confirm register values
# at the end of each loop iteration.
#
# Program counts prime numbers between 16700 and 123716

h = 0
for b in range(106700, 123717, 17):  # originally had an off-by-one error here

    # Detect if b has any factors other than 1 and b
    f = False
    for d in range(2, b):
        if b % d == 0:
            f = True

    if f:
        h = h + 1

print(h)
