from typing import Any
from math import prod


def read_and_parse_input_file(file_name: str) -> tuple[list[list[int]], list[str]]:
    with open(file_name) as f:
        content = f.read().splitlines()

    *number_lines, operator_line = content
    numbers = [list(map(int, line.split())) for line in number_lines]
    operators = operator_line.split()

    return numbers, operators


def read_and_parse_input_file_two(file_name: str):
    with open(file_name) as f:
        rows = [line.rstrip("\n") for line in f]

    width = max(len(r) for r in rows)

    # Pad rows with spaces so all have equal length
    padded_rows = [r.ljust(width) for r in rows]

    columns = []
    for col in range(width):
        column_chars = [row[col] for row in padded_rows]
        columns.append(column_chars)

    return columns


def parse_math(numbers: list[list[int]], operators: list[str]) -> int:
    total_sum = 0

    # Transpose columns using zip(*numbers)
    for op, column in zip(operators, zip(*numbers)):
        if op == '+':
            total_sum += sum(column)
        else:
            total_sum += prod(column)

    return total_sum


def parse_math_two(rows: list) -> int:
    blocks = []
    current_block = []

    for row in rows:
        last = row[-1]

        if last != " ":
            # Start of a new block
            if current_block:
                blocks.append(current_block)
            current_block = [row]  # this row belongs to the new block
        else:
            # Inside a block → just collect rows
            current_block.append(row)

    # Add final block if needed
    if current_block:
        blocks.append(current_block)

    total_sum = 0
    for block in blocks:
        column = []
        operator = block[0][-1]
        for b in block:
            n = "".join(b[:-1]).strip()
            # if any(ch.isdigit() for ch in n):
            if n.isdigit():
                column.append(int(n))
        if operator == '+':
            total_sum += sum(column)
        else:
            total_sum += prod(column)

    return total_sum


def compute_part_one(file_name: str) -> str:
    numbers, operators = read_and_parse_input_file(file_name)
    total = parse_math(numbers, operators)
    return f'{total= }'


def compute_part_two(file_name: str) -> str:
    columns = read_and_parse_input_file_two(file_name)
    total = parse_math_two(columns)

    return f'{total= }'


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('input/input6.txt')}")
    print(f"Part II: {compute_part_two('input/input6.txt')}")
