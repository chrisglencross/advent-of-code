a = 196
d = 2534 + a
while True:
    a = d
    while a > 0:
        b = a % 2
        a = a // 2
        print(b)
