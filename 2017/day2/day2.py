with open("input") as f:
    lines = f.readlines()

total = 0
for line in lines:
    line = line.replace("\t", " ")
    nums = [int(num.strip()) for num in line.split(" ") if num.strip()]
    total = total + max(nums) - min(nums)
print(total)

total = 0
for line in lines:
    line = line.replace("\t", " ")
    nums = [int(num.strip()) for num in line.split(" ") if num.strip()]
    for num in nums:
        total = total + sum([m for m in nums if m > num and m % num == 0]) / num
print(total)
