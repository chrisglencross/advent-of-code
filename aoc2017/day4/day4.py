with open("input") as f:
    lines = f.readlines()

count = 0
print(len(lines))
for line in lines:
    words = line.strip().split(" ")
    sorted_words = ["".join(sorted(word)) for word in words]
    if len(set(sorted_words)) == len(words):
        count = count + 1
print(count)
