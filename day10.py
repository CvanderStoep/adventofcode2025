import itertools
from ast import literal_eval
from typing import Any
from z3 import *


def read_and_parse_input_file(file_name: str) -> list:
    with open(file_name) as f:
        content = f.read().splitlines()

    return content


def parse_machine(machine: str) -> tuple:
    parts = machine.split()
    lights = [c == "#" for c in parts[0][1:-1]]
    buttons = [literal_eval(p) for p in parts[1:-1]]
    joltage = list(map(int, parts[-1][1:-1].split(",")))
    return lights, buttons, joltage


def apply_button(lights: list, button: tuple, joltage=None) -> tuple[list, Any | None]:
    for b in (button if isinstance(button, tuple) else [button]):
        lights[b] = not lights[b]
        if joltage is not None:
            joltage[b] += 1
    return lights, joltage


def find_minimum_presses(machine) -> int | None:
    target, buttons, _ = parse_machine(machine)

    length = 1
    while True:
        for sequence in itertools.product(buttons, repeat=length):
            lights = [False] * len(target)

            for button in sequence:
                lights, _ = apply_button(lights, button)
                if lights == target:
                    # print(f'{sequence= }')
                    return len(sequence)
        length += 1


def find_minimum_presses_two(machine) -> int | None:
    # it works, but it is way too slow

    target_lights, buttons, target_joltage = parse_machine(machine)
    print(target_lights, buttons, target_joltage)

    length = 1
    while True:
        # print(f'{length= }')
        for sequence in itertools.product(buttons, repeat=length):
            lights = [False] * len(target_lights)
            joltage = [0] * len(target_joltage)

            for button in sequence:
                lights, joltage = apply_button(lights, button, joltage)
                if joltage == target_joltage:
                    print(f'{sequence= }')
                    print(f'{joltage= }')
                    return len(sequence)
        length += 1


def compute_part_one(file_name: str) -> str:
    machines = read_and_parse_input_file(file_name)
    print(machines)
    total_presses = 0
    for machine in machines:
        total_presses += find_minimum_presses(machine)

    return f'{total_presses= }'


def compute_part_two(file_name: str) -> str:
    machines = read_and_parse_input_file(file_name)
    # print(machines)
    total_presses = 0
    for machine in machines:
        _, buttons, targets = parse_machine(machine)

        n = len(buttons)
        m = len(targets)
        # print(buttons, targets)

        x = [Int(f'x{i}') for i in range(n)]

        # s = Solver()
        s = Optimize()

        for i in range(n):
            s.add(x[i] >= 0)  # or >= 0 if zero is allowed

        for i in range(m):
            terms = []
            for j, g in enumerate(buttons):
                # print(g, list(g))
                if isinstance(g, int):
                    g = [g]
                if i in g:
                    terms.append(x[j])

            s.add(sum(terms) == targets[i])

        # print(x)
        s.minimize(sum(x))
        # print(s)

        # Solve
        if s.check() == sat:
            m = s.model()
            solution = [m[x[i]] for i in range(n)]
            total = sum(v.as_long() for v in solution)
            total_presses += total
        #
        #     print("solution:", solution)
        #     print(f'{total= }')
        # else:
        #     print("no solution")

    return f'{total_presses= }'


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('input/input10.txt')}")
    print(f"Part II: {compute_part_two('input/input10.txt')}")
