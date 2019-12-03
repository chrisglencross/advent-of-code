import itertools

c = [("a", 1), ("b", 2), ("a", 3)]
s = dict([(key, sum(pair[1] for pair in pairs)) for key, pairs in itertools.groupby(sorted(c), lambda p: p[0])])
print(s)
