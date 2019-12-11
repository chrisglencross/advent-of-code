# What is the last value of r5 before loop goes infinite?

last_possible_answer = None
possible_answers = set()

r0 = 8797248
r2 = 0  # 5:  seti 0 3 2  -- R2 = 0  <== PROPER START HERE
while True:
    r5 = 0x10000 | r2  # 6: outer loop starts here
    r2 = 4843319
    while True:

        # bani 5 255 4      #8:  R4 = R5 AND 255 (R4=0) <= inner loop starts here
        # addr 2 4 2        #9:  R2 = R2 + R4 (R2 = 4843319 + 0 = 4843319)
        # bani 2 16777215 2 #10: R2 = R2 AND 16777215 (4843319 AND 16777215 = 4843319) - bottom 24 bits
        # muli 2 65899 2    #11: R2 = R2 * 65899 (319169878781)
        # bani 2 16777215 2 #12: R2 = R2 AND 16777215 = 121597 (bottom 24 bits)
        r4 = r5 & 0xff  # 8: inner loop starts here
        r2 = r2 + r4
        r2 = r2 & 0xffffff
        r2 = r2 * 0x01016B
        r2 = r2 & 0xffffff

        # gtir 256 5 4      #13: R4 = 256 > R5?
        # addr 4 1 1        #14: PC = PC + R4 (GOTO #16 if true)
        # addi 1 1 1        #15: GOTO #17
        # seti 27 4 1       #16: GOTO #28 -- break out of loop?
        # print(r5)
        if 256 > r5:  # 13 ** what is the final value of r5 < 256?
            break

        # inner loop 2
        # seti 0 7 4        #17: R4 = 0 ## else
        # addi 4 1 3        #18: R3 = R4 + 1 (R3 = 1) <= inner loop 2 starts here
        # muli 3 256 3      #19: R3 = R3 * 256 (<<8; R3 = 256)
        # gtrr 3 5 3        #20: R3 = R3 > R5? (256 > 65536?)
        # addr 3 1 1        #21: PC = PC + R3 (GOTO #23 if true)
        # addi 1 1 1        #22: GOTO #24
        # seti 25 0 1       #23: GOTO #26
        # addi 4 1 4        #24: R4 = R4 + 1
        # seti 17 0 1       #25: GOTO #18 <= inner loop 2

        # set r4 to the number of times to shift left until r3 > r5
        r4 = 0  # #17
        while True:
            r3 = r4 + 1  # 18
            r3 = r3 << 8  # 19
            if r3 > r5:  # 20
                break  # 21/23
            r4 = r4 + 1  # 24

        # setr 4 1 5        #26: R5 = R4
        r5 = r4  # 26
        # End loop # seti 7 3 1        #27: GOTO #8 <= inner loop

    # eqrr 2 0 4        #28: -- R4 = R2 == R0?
    # addr 4 1 1        #28: PC = PC + R4 (EXIT IF TRUE)
    # seti 5 3 1        #29: GOTO #6

    if r2 not in possible_answers:
        last_possible_answer = r2
        if len(possible_answers) > 16000:
            print(r2)
        possible_answers.add(r2)
        if len(possible_answers) % 1000 == 0:
            print("..." + str(len(possible_answers)))
        # print(r2)
        # print(f"R2 could be {hex(r2)}")

# if r2 == r0:
#    break
# end outer loop
