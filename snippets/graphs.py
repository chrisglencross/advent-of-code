import networkx as nx

# Nodes with coordinates
G = nx.Graph()
G.add_node((0, 0), symbol=".")
G.add_node((1, 1), symbol="#")
G.add_node((2, 2), symbol="?")
G.add_edge((0, 0), (1, 1), weight=2)

print(G.nodes.keys())

# List edges of node
print(G[(1, 1)])

# Connected subgraphs e.g. finding constellations
print(list(nx.connected_components(G)))

# Shortest route
print(nx.shortest_path(G, (0, 0), (1, 1), weight="weight"))

# All maximal cliques
print(list(nx.find_cliques(G)))
