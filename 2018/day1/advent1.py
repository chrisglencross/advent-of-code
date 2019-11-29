with open("advent1.input") as f:
    lines = f.readlines()
values = [int(line) for line in lines if len(line.strip()) > 0]

frequencies = set()
frequency = 0
index = 0

while True:
    change = values[index % len(values)]
    frequency = frequency + change
    if frequency in frequencies:
        print(frequency)
        break
    frequencies.add(frequency)
    index = index + 1
