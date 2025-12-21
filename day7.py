from collections import deque, defaultdict


def read_and_parse_input_file(file_name: str) -> list:
    with open(file_name) as f:
        content = f.read().splitlines()
    content = [list(row) for row in content]

    return content


def process_manifold_bfs(manifold: list) -> int:
    """
    Traverse the manifold using a breadth‑first search to identify all splitter
    cells that can be reached from the start position.

    Behavior:
        - The start position 'S' is located on the top row.
        - From each cell, the search moves one row downward.
        - A '.' cell continues straight down.
        - Any other character is treated as a splitter: it is recorded, and the
          search branches diagonally left and/or right when those positions are
          within bounds.

    Notes:
        - A `visited` set prevents revisiting coordinates, keeping the BFS
          efficient and avoiding exponential growth.
        - The function does not count paths; it counts how many distinct
          splitter cells are reachable.

    Method:
        1. Initialize BFS from the start coordinate.
        2. For each reachable cell, inspect the cell directly below.
        3. Continue straight or branch depending on the cell type.
        4. Track all splitter coordinates encountered.
        5. Return the number of unique splitter cells reached.

    Args:
        manifold (list): A 2D grid of characters representing the puzzle input.

    Returns:
        int: Number of distinct splitter cells reachable from the start.
    """
    # Find start position
    start_x = manifold[0].index('S')
    start = (start_x, 0)

    height = len(manifold)
    width = len(manifold[0])

    queue = deque([start])
    visited = set()
    splitter = set()

    while queue:
        x, y = queue.popleft()

        if (x, y) in visited:
            continue
        visited.add((x, y))

        ny = y + 1
        if ny >= height:
            continue

        cell = manifold[ny][x]

        if cell == '.':
            queue.append((x, ny))
        else:
            splitter.add((x, ny))

            # Only enqueue valid x positions
            if x > 0:
                queue.append((x - 1, ny))
            if x < width - 1:
                queue.append((x + 1, ny))

    return len(splitter)


def process_manifold_bfs_two(manifold: list) -> int:
    """
    Perform a breadth‑first search over the manifold to count all possible paths.

    Notes:
        - This implementation intentionally skips the usual `is_visited` check.
          As a result, the search space grows exponentially because nodes may be
          revisited many times.
        - It works correctly for small manifolds, but becomes infeasible on
          larger datasets due to the combinatorial explosion.

    Steps:
        1. Locate the start position 'S' on the top row.
        2. Initialize BFS state and counters.
        3. Use manifold dimensions (height/width) to guide traversal.

    Args:
        manifold (list): A 2D grid of characters representing the search space.

    Returns:
        int: The number of valid paths found.
    """


    # Find start position
    start_x = manifold[0].index('S')
    start = (start_x, 0)

    all_paths = 0

    height = len(manifold)
    width = len(manifold[0])

    queue = deque([start])

    splitter = set()

    while queue:
        x, y = queue.popleft()

        ny = y + 1
        if ny >= height:
            all_paths += 1
            continue

        cell = manifold[ny][x]

        if cell == '.':
            queue.append((x, ny))
        else:
            splitter.add((x, ny))

            # Only enqueue valid x positions
            if x > 0:
                queue.append((x - 1, ny))
            if x < width - 1:
                queue.append((x + 1, ny))

    return all_paths


def process_manifold_dp(manifold: list) -> int:
    """
    Compute the total number of valid paths through the manifold using
    dynamic programming.

    This approach avoids the exponential blow‑up of BFS by tracking, for each
    coordinate, how many ways it can be reached. Each row is processed
    top‑down, and only the counts for the current row are kept in memory.

    Rules:
        - The start position 'S' is located on the top row.
        - A '.' cell allows the path to continue straight downward.
        - Any other character acts as a splitter, sending the path diagonally
          left and/or right when those positions are within bounds.

    Method:
        1. Initialize `ways` with the start coordinate having count = 1.
        2. For each row, build a new dictionary `next_ways` containing the
           accumulated number of ways to reach each reachable cell.
        3. Replace `ways` with `next_ways` and continue until the last row.
        4. Sum all counts in the final row to obtain the total number of paths.

    Args:
        manifold (list): A 2D grid of characters representing the puzzle input.

    Returns:
        int: Total number of distinct paths that reach the bottom row.
    """
    height = len(manifold)
    width = len(manifold[0])

    # Find start
    start_x = manifold[0].index('S')

    # ways[(x, y)] = number of ways to reach (x, y)
    ways = {(start_x, 0): 1}

    for y in range(height - 1):
        next_ways = defaultdict(int)

        for (x, cy), count in ways.items():
            ny = cy + 1

            cell = manifold[ny][x]

            if cell == '.':
                # Straight down
                next_ways[(x, ny)] += count
            else:
                # Splitter: go diagonally left/right if valid
                if x > 0:
                    next_ways[(x - 1, ny)] += count
                if x < width - 1:
                    next_ways[(x + 1, ny)] += count

        ways = next_ways

    # All the ways that reached the last row
    return sum(ways.values())


def compute_part_one(file_name: str) -> str:
    manifold = read_and_parse_input_file(file_name)
    total = process_manifold_bfs(manifold)

    return f'{total= }'


def compute_part_two(file_name: str) -> str:
    manifold = read_and_parse_input_file(file_name)
    total = process_manifold_dp(manifold)

    return f'{total= }'


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('input/input7.txt')}")
    print(f"Part II: {compute_part_two('input/input7.txt')}")
