a = 0

# Part 2
# a = 1

if a == 1:
    a = 113383
else:
    a = 4591

b = 0
while a != 1:
    b += 1
    if a % 2 == 0:
        a //= 2
    else:
        a = a * 3 + 1

print(b)
