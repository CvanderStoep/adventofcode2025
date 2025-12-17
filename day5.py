def read_input_file(file_name: str) -> tuple[list[tuple[int, ...]], list[int]]:
    with open(file_name) as f:
        ranges_block, ids_block = f.read().strip().split("\n\n")

    ranges = [tuple(map(int, r.split("-"))) for r in ranges_block.splitlines()]
    ids = list(map(int, ids_block.splitlines()))
    return ranges, ids


def is_fresh_ingredient(ranges: list, id_: int) -> bool:
    return any(left <= id_ <= right for left, right in ranges)


def count_range_values(ranges: list) -> int:
    return sum(end - start + 1 for start, end in ranges)


def merge_ranges(ranges):
    # Sort by start value
    ranges = sorted(ranges, key=lambda x: x[0])
    merged = []

    for start, end in ranges:
        if not merged or start > merged[-1][1]:
            # No overlap → new range
            merged.append([start, end])
        else:
            # Overlap → extend the last range
            merged[-1][1] = max(merged[-1][1], end)

    return merged


def compute_part_one(file_name: str) -> str:
    ranges, ids = read_input_file(file_name)
    number_fresh_ingredients = sum(is_fresh_ingredient(ranges, id_) for id_ in ids)
    return f"{number_fresh_ingredients= }"


def compute_part_two(file_name: str) -> str:
    ranges, _ = read_input_file(file_name)
    merged = merge_ranges(ranges)
    total = count_range_values(merged)
    return f'{total = }'


if __name__ == "__main__":
    print(f"Part I: {compute_part_one('input/input5.txt')}")
    print(f"Part II: {compute_part_two('input/input5.txt')}")
