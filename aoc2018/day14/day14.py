scores = [3, 7]
current = [0, 1]

# limit = 540391
contents = "540391"
# contents = "51589"

# while len(scores) < limit + 10:
i = 0
while True:
    i = i + 1
    if i % 10000 == 0:
        print(i)
    current_scores = [scores[index] for index in current]
    total = sum(current_scores)
    orig_total = total
    new_scores = []
    while total > 0 or len(new_scores) == 0:
        new_scores.insert(0, total % 10)
        total = total // 10
    scores.extend(new_scores)

    current = [(index + scores[index] + 1) % len(scores) for index in current]

    suffix = "".join([str(score) for score in scores[-10:]])
    if contents in suffix:
        break

text = "".join([str(score) for score in scores])
print(text.find(contents))

# print("".join([str(score) for score in scores[limit:limit+10]]))
# 5941429882
