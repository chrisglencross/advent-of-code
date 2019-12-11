import re
from datetime import timedelta

import dateutil.parser

with open("input") as f:
    lines = f.readlines()

lines.sort()

days = dict()
current_guard = None
current_date = None
awake = True
fell_asleep_mins = None
current_shift = None

guard_minutes_asleep = {}

for line in lines:
    # [1518-09-15 00:56] wakes up
    match = re.search("^\\[(.+)\\] (.*)$", line.strip())
    date_string = match.group(1)
    event_time = dateutil.parser.parse(date_string)
    event = match.group(2)
    print(str(event_time.date()) + "T" + str(event_time.time()) + " : " + event)

    guard_match = re.search("Guard #([0-9]+) begins shift", event)
    if guard_match is not None:
        if not awake:
            raise Exception("New guard starts while previous guard asleep")

        if current_shift is not None:
            if current_guard not in days:
                days[current_guard] = []
            days[current_guard].append("".join(current_shift))

        current_guard = guard_match.group(1)
        awake = True
        fell_asleep_mins = None
        current_shift = ['.' for x in range(0, 60)]
        if event_time.hour >= 1:
            current_date = event_time.date() + timedelta(days=1)
            print(current_date)
        else:
            current_date = event_time.date()
    else:
        if event_time.date() != current_date:
            raise Exception("Wrong date")
        if event == "falls asleep":
            asleep = True
            fell_asleep_mins = event_time.time().minute
            print(fell_asleep_mins)
        elif event == "wakes up":
            awake = True
            woke_up_mins = event_time.time().minute
            for minute in range(fell_asleep_mins, woke_up_mins):
                current_shift[minute] = "#"
            fell_asleep_mins = None
        else:
            raise Exception("Unknown event " + event)

if current_shift is not None:
    if current_guard not in days:
        days[current_guard] = []
    days[current_guard].append("".join(current_shift))

guard_minutes = []
for guard, guard_days in days.items():
    minutes = sum([len(day.replace(".", "")) for day in guard_days])
    guard_minutes.append({"guard": guard, "minutes_asleep": minutes})
guard_minutes.sort(key=lambda gm: gm["minutes_asleep"], reverse=True)
sleepy_guard = guard_minutes[0]["guard"]
print(sleepy_guard)

sleepy_guard_shifts = days[sleepy_guard]
print("\n".join(sleepy_guard_shifts))
sleepy_guard_minutes = []
for minute in range(0, 60):
    count = 0
    for shift in sleepy_guard_shifts:
        if shift[minute] == '#':
            count = count + 1
    sleepy_guard_minutes.append({"minute": minute, "count": count})
sleepy_guard_minutes.sort(key=lambda gm: gm["count"], reverse=True)
print(sleepy_guard_minutes)
sleepiest_minute = sleepy_guard_minutes[0]["minute"]

print(sleepiest_minute * int(sleepy_guard))

part2_sleepiest = list()
for guard, guard_days in days.items():
    for minute in range(0, 60):
        count = 0
        for shift in guard_days:
            if shift[minute] == '#':
                count = count + 1
        part2_sleepiest.append({"guard": guard, "minute": minute, "count": count})

part2_sleepiest.sort(key=lambda gm: gm["count"], reverse=True)
print(part2_sleepiest)
sleepiest_guard_2 = part2_sleepiest[0]["guard"]
sleepiest_minute_2 = part2_sleepiest[0]["minute"]
print(int(sleepiest_guard_2) * sleepiest_minute_2)
