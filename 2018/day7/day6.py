with open("input") as f:
    lines = f.readlines()

all_nodes = set()
dependencies = dict()
for line in lines:
    # Step B must be finished before step E can begin.
    before = line.split(" ")[1]
    after = line.split(" ")[7]
    all_nodes.add(before)
    all_nodes.add(after)
    if after in dependencies:
        dependencies[after].add(before)
    else:
        dependencies[after] = {before}

blocked_nodes = list(all_nodes)
blocked_nodes.sort()

running_nodes = []
complete_nodes = []

task_overhead = 60
workers = 5

current_time = 0
while len(blocked_nodes) > 0 or len(running_nodes) > 0:
    # Remove completed running nodes
    for node in [node["node"] for node in running_nodes if node["end_time"] <= current_time]:
        print(f"Completed node {node} at {current_time} seconds")
        complete_nodes.append(node)
    running_nodes = [node for node in running_nodes if node["end_time"] > current_time]
    for node in blocked_nodes:
        if len(running_nodes) >= workers:
            break
        if node not in dependencies or dependencies[node].issubset(set(complete_nodes)):
            task_time = task_overhead + ord(node) - ord("A") + 1
            print(f"Started node {node} at {current_time} seconds (will take {task_time} seconds")
            running_nodes.append({"node": node, "end_time": current_time + task_time})
            blocked_nodes.remove(node)
    current_time = current_time + 1

print("".join(complete_nodes))
print(current_time - 1)
