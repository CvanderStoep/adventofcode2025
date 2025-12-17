DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1), (1, 1), (-1, -1)]


def read_input_file(file_name: str) -> list:
    with open(file_name) as f:
        content = f.read().splitlines()
    return content


def find_neighbours(x: int, y: int, grid: list) -> list:
    neighbours = []
    for dx, dy in DIRECTIONS:
        if 0 <= x + dx < len(grid[0]) and 0 <= y + dy < len(grid):
            if grid[y + dy][x + dx] == '@':
                neighbours.append((x + dx, y + dy))

    return neighbours


def compute_part_one(file_name: str) -> str:
    grid = read_input_file(file_name)
    number_accessible_by_forklift = 0
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell != '@':
                continue
            neighbours = find_neighbours(x, y, grid)
            if len(neighbours) < 4:
                number_accessible_by_forklift += 1

    return f'{number_accessible_by_forklift= }'


def compute_part_two(file_name: str) -> str:
    grid = read_input_file(file_name)
    # maze = [list(row) for row in grid]

    height = len(grid)
    width = len(grid[0])

    while True:
        removable = []
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if cell != '@':
                    continue
                neighbours = find_neighbours(x, y, grid)
                if len(neighbours) < 4:
                    removable.append((x, y))
        if not removable:
            break
        grid = [
            ''.join('x' if (x, y) in removable else grid[y][x]
                    for x in range(width))
            for y in range(height)
        ]
    count = sum(row.count('x') for row in grid)

    return f'{count= }'


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('input/input4.txt')}")
    print(f"Part II: {compute_part_two('input/input4.txt')}")
