with open("input") as f:
    input = f.readlines()[0]

# part 1
prev = input[-1]
sum = 0
for char in input:
    if char == prev:
        sum = sum + int(char)
    prev = char
print(sum)

# part 2
sum = 0
for i, char in enumerate(input):
    prev_i = (i + (len(input) // 2)) % len(input)
    if char == input[prev_i]:
        sum = sum + int(char)
print(sum)
