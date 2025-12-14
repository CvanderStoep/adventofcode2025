def read_input_file(file_name: str) -> list:
    with open(file_name) as f:
        content = f.read().splitlines()

    # content = list(map(int, content))


    return content

def is_valid_id(id_: int) -> bool:
    s = str(id_)
    mid = len(s) // 2
    return s[:mid] != s[mid:]

def is_valid_two(id_: int) -> bool:
    s = str(id_)
    n = len(s)

    # Single digit is always valid
    if n == 1:
        return True

    # Rule 1: reject if first half == second half
    mid = n // 2
    if n % 2 == 0 and s[:mid] == s[mid:]:
        return False

    # Rule 2: reject if the whole string is made of repeated patterns
    for l in range(1, n):
        if n % l != 0:
            continue  # pattern must divide length

        pattern = s[:l]
        if pattern * (n // l) == s:
            return False

    return True

def compute_part_one(file_name: str) -> str:
    content = read_input_file(file_name)
    sum_invalid_id = 0

    for part in content[0].split(','):
        left, right = map(int, part.split('-'))
        for id_ in range(left, right + 1):
            if not is_valid_id(id_):
                sum_invalid_id += id_

    return f"{sum_invalid_id=}"

def compute_part_two(file_name: str) -> str:
    content = read_input_file(file_name)
    sum_invalid_id = 0

    for part in content[0].split(','):
        left, right = map(int, part.split('-'))
        for id_ in range(left, right + 1):
            if not is_valid_two(id_):
                sum_invalid_id += id_

    return f"{sum_invalid_id=}"


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('input/input2.txt')}")
    print(f"Part II: {compute_part_two('input/input2.txt')}")
