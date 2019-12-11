sum = 0
for i in range(1, 10551316):
    if 10551315 % i == 0:
        sum = sum + i
        print(i, sum)
