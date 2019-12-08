#!/usr/bin/python3
# Advent of code 2019 day 8

with open("input.txt") as f:
    data = f.readline()

width = 25
height = 6
layer_size = width * height
layer_count = len(data) // layer_size

layers = [data[layer_size * layer:layer_size * (layer + 1)] for layer in range(layer_count)]

# Part 1
min_zero_layer = min(layers, key=lambda layer: layer.count("0"))
print(min_zero_layer.count("1") * min_zero_layer.count("2"))

# Part 2
stacked = list(" " * layer_size)
for layer in layers:
    for i in range(layer_size):
        if stacked[i] == ' ' and layer[i] != '2':
            stacked[i] = layer[i]

for y in range(height):
    print("".join(stacked[width * y:width * (y + 1)]).replace("0", " ").replace("1", "*"))
