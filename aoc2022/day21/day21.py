import aoc2022.day21.monkeys as monkeys

# Part 1
print(int(monkeys.root()))

# Part 2
# monkey-patch the... erm... monkey, to inject our own input value
monkeys.humn = lambda: yell

# `root` checks if output of function `pnhm` equals constant from function `zvcm`
# Search for the value of yell such that this is true, and observe that pnhm decreases in value with increasing yell.
zvcm = monkeys.zvcm()
yell = 0
min_yell = 0
max_yell = None
while True:
    pnhm = monkeys.pnhm()
    # print(f"When yell={yell}, pnhm={pnhm} (target zvcm={zvcm}) [yell range {min_yell} - {max_yell}]")
    if pnhm == zvcm:
        print(yell)
        break
    elif pnhm > zvcm:
        # pnhm too big: increase yell
        min_yell = yell + 1
        if max_yell is None:
            yell = yell * 2 + 1
        else:
            yell = (max_yell + min_yell) // 2
    elif pnhm < zvcm:
        # pnhm too small: decrease yell
        max_yell = yell - 1
        yell = (min_yell + max_yell) // 2
