def read_input_file(file_name: str) -> list:
    """
    Read a text file and return its contents as a list of lines.

    Args:
        file_name (str): Path to the input file.

    Returns:
        list: A list where each element is one line from the file.
    """
    with open(file_name) as f:
        content = f.read().splitlines()

    return content


def largest_digit_and_index(s):
    """
    Find the largest digit in a string and return both the digit and its index.

    Args:
        s (str): The string to scan.

    Returns:
        tuple: (largest_digit, index_of_digit)
               If no digit is found, returns (None, None).
    """
    best_digit = None
    best_index = None

    for i, ch in enumerate(s):
        if ch.isdigit():
            # Update if this is the first digit or a larger one
            if best_digit is None or ch > best_digit:
                best_digit = ch
                best_index = i

    return best_digit, best_index


def return_joltage(bank: str) -> int:
    """
    Compute the 'Joltage' of a bank string.
    Joltage is formed by:
      - Finding the largest digit in the string except the last character.
      - Then finding the largest digit *after* that first digit.
      - Combining both digits into a two-digit integer.

    Args:
        bank (str): The bank string to analyze.

    Returns:
        int: The computed Joltage value.
    """
    # Find the largest digit in all but the last character
    digit1, index1 = largest_digit_and_index(bank[:-1])

    # Find the largest digit after the first digit's position
    digit2, _ = largest_digit_and_index(bank[index1 + 1:])

    # Combine digits into a two-digit number
    joltage = int(digit1 + digit2)

    return joltage


def return_joltage_12_digits(bank: str) -> int:
    digits = []

    for i in range(11, 0, -1):
        digit, index = largest_digit_and_index(bank[:-i])
        bank = bank[index + 1:]
        digits.append(digit)
    digit, _ = largest_digit_and_index(bank)
    digits.append(digit)
    joltage = int(''.join(digits))

    return joltage


def compute_part_one(file_name: str) -> str:
    """
    Compute the total joltage for all banks in the input file.

    Args:
        file_name (str): Path to the input file.

    Returns:
        str: A formatted string showing the total joltage.
    """
    banks = read_input_file(file_name)
    total_joltage = 0

    for bank in banks:
        joltage = return_joltage(bank)
        total_joltage += joltage

    return f'{total_joltage= }'


def compute_part_two(file_name: str) -> str:
    """
    Compute the total joltage for all banks in the input file.

    Args:
        file_name (str): Path to the input file.

    Returns:
        str: A formatted string showing the total joltage.
    """
    banks = read_input_file(file_name)
    total_joltage = 0

    for bank in banks:
        joltage = return_joltage_12_digits(bank)
        total_joltage += joltage

    return f'{total_joltage= }'


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('input/input3.txt')}")
    print(f"Part II: {compute_part_two('input/input3.txt')}")
