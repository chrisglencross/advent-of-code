# Work out the order of coins to put into the slots

from itertools import permutations

coins = [2, 3, 5, 7, 9]

for a, b, c, d, e in permutations(coins):
    answer = a + (b * pow(c, 2)) + pow(d, 3) - e
    if answer == 399:
        print(a, b, c, d, e)
