import re
def read_input_file(file_name: str) -> list:
    with open(file_name) as f:
        content = f.read().splitlines()

    return content


def process_rotation(rotation: str) -> tuple[str, int]:
    letter, number = re.match(r"([A-Za-z]+)(\d+)", rotation).groups()
    return letter, int(number)


def turn_dial(direction: str, start_position: int, rotation: int) -> int | None:
    if direction == 'L':
        return (start_position - rotation) %100
    elif direction == 'R':
        return (start_position + rotation) %100
    return None

def turn_dial_and_count(direction: str, start_position: int, rotation: int) -> tuple[int, int]:
    pos = start_position
    count = 0

    if direction == 'R':
        step = 1
    elif direction == 'L':
        step = -1
    else:
        raise ValueError(f"Unknown direction: {direction}")

    for _ in range(rotation):
        pos = (pos + step) % 100
        if pos == 0:
            count += 1

    return pos, count

def compute_part_one(file_name: str) -> str:
    rotations = read_input_file(file_name)
    start_position: int = 50
    count_zero = 0
    for rotation in rotations:
        direction, rotation = process_rotation(rotation)
        start_position = turn_dial(direction, start_position, rotation)
        if start_position == 0:
            count_zero += 1

    return f'{count_zero= }'

def compute_part_two(file_name: str) -> str:
    rotations = read_input_file(file_name)
    start_position: int = 50
    total_passing = 0
    for rotation in rotations:
        direction, rotation = process_rotation(rotation)
        start_position, count_zero = turn_dial_and_count(direction, start_position, rotation)
        total_passing += count_zero



    return f'{total_passing= }'





if __name__ == '__main__':
    print(f"Part I: {compute_part_one('input/input1.txt')}")
    print(f"Part II: {compute_part_two('input/input1.txt')}")
