DEBUG_ENABLED = False

def toBase26(n):
    if n == 0:
        return "0"
    digits = []
    while n:
        digits.append(str(int(n % 26)))
        n //= 26
    return "_".join(digits[::-1])

def debugBase26(n):
    if DEBUG_ENABLED:
        print(toBase26(n))

def evaluate(inp):

    inp_0, inp_1, inp_2, inp_3, inp_4, inp_5, inp_6, inp_7, inp_8, inp_9, inp_10, inp_11, inp_12, inp_13 = inp

    # Annotated and tidied version of the output from the decompiler
    # with some debug print statements to help work out max and min values manually

    z_8 = (((((inp_0 + 1) * 26) + (inp_1 + 9)) * 26) + (inp_2 + 11))
    debugBase26(z_8)

    x_23 = (((z_8 % 26) + -13) != inp_3)
    z_11 = (((z_8 // 26) * ((25 * x_23) + 1)) + ((inp_3 + 6) * x_23))
    debugBase26(z_11)

    x_29 = (((z_11 % 26) + 11) != inp_4)
    z_14 = ((z_11 * ((25 * x_29) + 1)) + ((inp_4 + 6) * x_29))
    debugBase26(z_14)

    x_35 = (((z_14 % 26) + 15) != inp_5)
    z_17 = ((z_14 * ((25 * x_35) + 1)) + ((inp_5 + 13) * x_35))
    debugBase26(z_17)

    x_41 = (((z_17 % 26) + -14) != inp_6)
    z_20 = (((z_17 // 26) * ((25 * x_41) + 1)) + ((inp_6 + 13) * x_41))
    debugBase26(z_20)

    x_47 = (((z_20 % 26) + 12) != inp_7)
    z_23 = ((z_20 * ((25 * x_47) + 1)) + ((inp_7 + 5) * x_47))
    debugBase26(z_23)

    x_53 = (((z_23 % 26) + -8) != inp_8)
    z_26 = (((z_23 // 26) * ((25 * x_53) + 1)) + ((inp_8 + 7) * x_53))
    debugBase26(z_26)

    x_59 = (((z_26 % 26) + 14) != inp_9)
    z_29 = ((z_26 * ((25 * x_59) + 1)) + ((inp_9 + 2) * x_59))
    debugBase26(z_29)

    x_65 = (((z_29 % 26) + -9) != inp_10)
    z_32 = (((z_29 // 26) * ((25 * x_65) + 1)) + ((inp_10 + 10) * x_65))
    debugBase26(z_32)

    x_71 = (((z_32 % 26) + -11) != inp_11)
    z_35 = (((z_32 // 26) * ((25 * x_71) + 1)) + ((inp_11 + 14) * x_71))
    debugBase26(z_35)

    x_77 = (((z_35 % 26) + -6) != inp_12)
    z_38 = (((z_35 // 26) * ((25 * x_77) + 1)) + ((inp_12 + 7) * x_77))
    debugBase26(z_38)

    x_83 = (((z_38 % 26) + -5) != inp_13)
    z_41 = (((z_38 // 26) * ((25 * x_83) + 1)) + ((inp_13 + 1) * x_83))
    debugBase26(z_41)

    return "".join([str(digit) for digit in inp]), z_41


# Numbers worked out manually with paper and debugging through the above code
print(evaluate([9, 6, 9, 7, 9, 9, 8, 9, 6, 9, 2, 4, 9, 5]))
print(evaluate([5, 1, 3, 1, 6, 2, 1, 4, 1, 8, 1, 1, 4, 1]))
