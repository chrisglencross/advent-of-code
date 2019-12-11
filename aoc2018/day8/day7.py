with open("input") as f:
    lines = f.readlines()

records = [int(record) for record in lines[0].split(" ")]


def read_record(records, index):
    child_count = records[index]
    metadata_count = records[index + 1]
    index = index + 2
    children = []
    for i in range(0, child_count):
        (child, index) = read_record(records, index)
        children.append(child)
    metadata = records[index: index + metadata_count]
    index = index + metadata_count
    return {"metadata": metadata, "children": children}, index


def sum_metadata(record):
    metadata = record["metadata"]
    self_total = sum(metadata)
    child_total = sum([sum_metadata(child) for child in record["children"]])
    return self_total + child_total


def part2_sum_metadata(record):
    metadata = record["metadata"]
    children = record["children"]
    if len(children) == 0:
        return sum(metadata)
    total = 0
    for child_index in metadata:
        child_index = child_index - 1
        if 0 <= child_index < len(children):
            total = total + part2_sum_metadata(children[child_index])
    return total


root, index = read_record(records, 0)

print(len(records))
print(index)
print(root)
print(sum_metadata(root))
print(part2_sum_metadata(root))
