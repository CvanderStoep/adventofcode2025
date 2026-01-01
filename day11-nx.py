import networkx as nx

from functools import lru_cache


def count_paths(G, source, target):
    @lru_cache(None)
    def dfs(node):
        if node == target:
            return 1
        return sum(dfs(nbr) for nbr in G.successors(node))

    return dfs(source)


def load_adjlist(path):
    G = nx.DiGraph()

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            node, rhs = line.split(":")
            node = node.strip()

            # Split targets and strip each one
            targets = [t.strip() for t in rhs.split()]

            # Always add the source node
            G.add_node(node)

            # Add edges for all targets
            for t in targets:
                G.add_edge(node, t)

    return G


G = load_adjlist('input/input11.txt')
print(G.edges())
print(G.nodes())

a1 = count_paths(G, "svr", "fft")
a2 = count_paths(G, "fft", "dac")
a3 = count_paths(G, "dac", "out")

b1 = count_paths(G, "svr", "dac")
b2 = count_paths(G, "dac", "fft")
b3 = count_paths(G, "fft", "out")

print(a1 * a2 * a3 + b1 * b2 * b3)
