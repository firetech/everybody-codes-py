# pyright: strict

import statistics
from typing import Sequence

from everybody_codes_py_ft import common as lib


def _hammer_to(nails: Sequence[int], target: int):
    return sum(abs(nail - target) for nail in nails)


def _hammer_min(nails: Sequence[int]):
    return _hammer_to(nails, min(nails))


def part1():
    nails = [int(i) for i in lib.get_input(1).splitlines()]
    print(f"Part 1: {_hammer_min(nails)}")


def part2():
    nails = [int(i) for i in lib.get_input(2).splitlines()]
    print(f"Part 2: {_hammer_min(nails)}")


def part3():
    nails = [int(i) for i in lib.get_input(3).splitlines()]
    print(f"Part 3: {_hammer_to(nails, int(statistics.median(nails)))}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
