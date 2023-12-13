import os
import requests


def download_input(year, day):

    if os.path.exists("input.txt"):
        with open("input.txt") as f:
            data = f.read()
            if data and not data.startswith("# Download input data"):
                return  # already downloaded

    url = f"https://adventofcode.com/{year}/day/{day}/input"
    aoc_token = os.environ.get("AOC_TOKEN")
    if not aoc_token:
        print(f"WARNING: AOC_TOKEN environment variable not set. Will not download input from {url}")
        return

    r = requests.get(url, cookies={"session": aoc_token})
    with open("input.txt", "w") as f:
        f.write(r.text)

