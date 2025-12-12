def read_input_file(file_name: str) -> list:
    with open(file_name) as f:
        content = f.read().splitlines()

    # content = list(map(int, content))


    return content


def compute_part_one(file_name: str) -> int:
    content = read_input_file(file_name)
    print(content)

    return 1


def compute_part_two(file_name: str) -> int:
    content = read_input_file(file_name)
    return 2


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('input/input0.txt')}")
    print(f"Part II: {compute_part_two('input/input0.txt')}")
