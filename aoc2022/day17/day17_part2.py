# Debug logging in part 1 shows cycle repeat every 1755 shapes of height 2768
# To get to 10^12 shapes takes N cycles (of height N*2768) + the height of 10^12-1755*N additional shapes == 2734
# Calculations:

cycle_shapes = 5265 - 3510
cycle_height = 8270 - 5502

print(f"Cycle shapes: {cycle_shapes}")
print(f"Cycle height: {cycle_height}")

N = 10**12//cycle_shapes
print(f"Requires N={N} cycles to reach 10^12 shapes plus some additional shapes")

additional_shapes = 10**12 - cycle_shapes*N
print(f"Requires {additional_shapes} additional shapes")

height_of_N_cycles = N*2768
height_of_additional_shapes = 2194

total_height = height_of_N_cycles + height_of_additional_shapes
print(total_height)
