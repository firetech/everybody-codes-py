# pyright: strict

from collections import Counter

from everybody_codes_py_ft import common as lib


def _parse_crates(data: str):
    return [int(c) for c in data.strip().split(",")]


def part1():
    largest_sum = sum(set(_parse_crates(lib.get_input(1))))
    print(f"Part 1: {largest_sum}")


def part2():
    smallest_sum = sum(sorted(set(_parse_crates(lib.get_input(2))))[:20])
    print(f"Part 2: {smallest_sum}")


def part3():
    _, min_groups = Counter(_parse_crates(lib.get_input(3))).most_common(1)[0]
    print(f"Part 3: {min_groups}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
