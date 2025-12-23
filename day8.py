import math
import networkx as nx
from collections import defaultdict
from itertools import combinations


def read_and_parse_input_file(file_name: str) -> list[tuple[int, ...]]:
    with open(file_name) as f:
        return [tuple(map(int, line.split(","))) for line in f]


def distance(a: tuple[int, ...], b: tuple[int, ...]) -> float:
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


def compute_part_one_networkx(file_name: str) -> str:
    points = read_and_parse_input_file(file_name)
    print(points)

    # Build all pairwise distances
    distances = [
        (i, j, distance(p1, p2))
        for (i, p1), (j, p2) in combinations(enumerate(points), 2)
    ]
    distances.sort(key=lambda x: x[2])

    # Build graph using first 1000 smallest edges
    G = nx.Graph()
    G.add_nodes_from(range(len(points)))

    for p1, p2, _ in distances[:1000]:
        G.add_edge(p1, p2)

    # Extract connected components
    components = list(nx.connected_components(G))
    sizes = sorted((len(c) for c in components), reverse=True)

    top_three = sizes[:3]
    print(f"{top_three= }")

    return f"{math.prod(top_three)= }"


def contains_number(clusters, n):
    return any(n in items for items in clusters.values())


def compute_part_one_(file_name: str) -> str:
    # my original code, improved see below.
    points = read_and_parse_input_file(file_name)
    print(points)

    distances = []
    for p1, p2 in combinations(list(enumerate(points)), 2):
        distances.append([p1[0], p2[0], distance(p1[1], p2[1])])
    distances.sort(key=lambda x: x[2])

    clusters = defaultdict(set)
    cluster_id = 0
    n = 0

    for p1, p2, _ in distances:
        if n >= 1000:
            break
        n += 1
        key1 = next((cid for cid, items in clusters.items() if p1 in items), None)
        key2 = next((cid for cid, items in clusters.items() if p2 in items), None)
        if key1 is None and key2 is None:
            cluster_id += 1
            clusters[cluster_id] = {p1, p2}
        elif key1 is None:
            clusters[key2].update([p1, p2])
        elif key2 is None:
            clusters[key1].update([p1, p2])
        elif key1 == key2:
            clusters[key1].update([p1, p2])
        else:  # merge two sets
            clusters[key1].update([p1, p2])  # not really needed as we merge them later.
            clusters[key1].update(clusters[key2])
            clusters[key2] = set()

    all_sizes = [len(s) for s in clusters.values()]
    all_sizes.sort(reverse=True)
    top_three = all_sizes[:3]
    print(f'{top_three= }')
    multiply_sizes = math.prod(top_three)
    return f'{multiply_sizes= }'


def compute_part_one(file_name: str) -> str:
    points = read_and_parse_input_file(file_name)
    print(points)

    # Precompute all pairwise distances
    distances = [
        (i, j, distance(p1, p2))
        for (i, p1), (j, p2) in combinations(enumerate(points), 2)
    ]
    distances.sort(key=lambda x: x[2])

    clusters = defaultdict(set)
    cluster_id = 0

    def find_cluster(point):
        for cid, items in clusters.items():
            if point in items:
                return cid
        return None

    # Process first 1000 closest pairs
    for n, (p1, p2, _) in enumerate(distances[:1000], start=1):
        c1 = find_cluster(p1)
        c2 = find_cluster(p2)

        if c1 is None and c2 is None:
            cluster_id += 1
            clusters[cluster_id] = {p1, p2}
        elif c1 is None:
            clusters[c2].update([p1, p2])
        elif c2 is None:
            clusters[c1].update([p1, p2])
        elif c1 != c2:
            # merge c2 into c1
            clusters[c1].update(clusters[c2])
            clusters[c2].clear()

        else:
            clusters[c1].update([p1, p2])

    # Compute result
    sizes = sorted((len(s) for s in clusters.values()), reverse=True)
    top_three = sizes[:3]
    print(f"{top_three= }")

    return f"{math.prod(top_three)= }"


def compute_part_two(file_name: str) -> str:
    points = read_and_parse_input_file(file_name)

    # Precompute all pairwise distances
    distances = [
        (i, j, distance(p1, p2))
        for (i, p1), (j, p2) in combinations(enumerate(points), 2)
    ]
    distances.sort(key=lambda x: x[2])

    clusters = defaultdict(set)
    cluster_id = 0

    def find_cluster(point):
        for cid, items in clusters.items():
            if point in items:
                return cid
        return None

    # Process first 1000 closest pairs
    for n, (p1, p2, _) in enumerate(distances, start=1):
        c1 = find_cluster(p1)
        c2 = find_cluster(p2)

        if c1 is None and c2 is None:
            cluster_id += 1
            clusters[cluster_id] = {p1, p2}
        elif c1 is None:
            clusters[c2].update([p1, p2])
        elif c2 is None:
            clusters[c1].update([p1, p2])
        elif c1 != c2:
            # merge c2 into c1
            clusters[c1].update(clusters[c2])
            clusters[c2].clear()
        else:
            clusters[c1].update([p1, p2])

        sizes = sorted((len(s) for s in clusters.values()), reverse=True)
        top_two = sizes[:2]
        if sum(top_two) == 1000:
            # print(points[p1], points[p2])
            break
    x_coordinates = points[p1][0] * points[p2][0]

    print(f"{top_two= }")

    return f"{x_coordinates= }"


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('input/input8.txt')}")
    print(f"Part I: {compute_part_one_networkx('input/input8.txt')}")
    print(f"Part II: {compute_part_two('input/input8.txt')}")
