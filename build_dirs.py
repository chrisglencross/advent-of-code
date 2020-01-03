import os

year = "2015"
dir = f"aoc{year}"
if not os.path.exists(f"{dir}"):
    os.mkdir(f"{dir}")


def ensure_file(filename, contents):
    if not os.path.exists(filename):
        with open(filename, "w+") as of:
            of.write(contents)


for day in range(1, 26):
    d = f"{dir}/day{day}"
    if not os.path.exists(d):
        print(f"Creating {d}")
        os.mkdir(d)
        ensure_file(f"{d}/input.txt", f"# Download input data from https://adventofcode.com/{year}/day/{day}/input")
        ensure_file(f"{d}/testinput.txt", "# Placeholder for test input data")
        with open("template/dayN.py") as template:
            content = template.read().replace("<YEAR>", str(year)).replace("<DAY>", str(day))
            ensure_file(f"{d}/day{day}.py", content)
