from collections import deque
from typing import Any


def read_and_parse_input_file(file_name: str) -> dict[Any, Any]:
    mapping = {}
    with open(file_name, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            key, values = line.split(":", 1)
            key = key.strip()
            values = values.strip().split()

            mapping[key] = values
    mapping['out'] = []
    return mapping


def calculate_all_paths(start: str, finish: str, devices: dict) -> list:
    all_paths = []
    queue = deque([(start, [start])])  # (current_node, path_so_far)

    while queue:
        current, path_so_far = queue.popleft()

        if current == finish:
            # print(path_so_far)
            all_paths.append(path_so_far)
            continue

        for nxt in devices[current]:
            # Avoid cycles: don't revisit nodes already in the path
            if nxt in path_so_far:
                continue

            new_path = path_so_far + [nxt]
            queue.append((nxt, new_path))
    return all_paths


def compute_part_one(file_name: str) -> int:
    devices = read_and_parse_input_file(file_name)
    print(devices)

    start = 'you'
    finish = 'out'

    all_paths = calculate_all_paths(start, finish, devices)

    return len(all_paths)


def compute_part_two(file_name: str) -> int:
    """works only for small graphs"""
    devices = read_and_parse_input_file(file_name)
    print(devices)


    a1 = len(calculate_all_paths("svr", "fft", devices))
    a2 = len(calculate_all_paths("fft", "dac", devices))
    a3 = len(calculate_all_paths("dac", "out", devices))

    b1 = len(calculate_all_paths("svr", "dac", devices))
    b2 = len(calculate_all_paths("dac", "fft", devices))
    b3 = len(calculate_all_paths("fft", "out", devices))

    valid_paths = (a1 * a2 * a3 + b1 * b2 * b3)

    return valid_paths


if __name__ == '__main__':
    # print(f"Part I: {compute_part_one('input/input11.txt')}")
    print(f"Part II: {compute_part_two('input/input11.txt')}")
