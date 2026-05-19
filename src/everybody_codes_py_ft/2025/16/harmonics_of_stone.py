# pyright: strict

import math
from typing import Iterable

from everybody_codes_py_ft import common as lib


def _total_blocks(pattern: Iterable[int], length: int):
    return sum(length // x for x in pattern)


def part1():
    print(f"Part 1: {_total_blocks((int(x) for x in lib.get_input(1).split(",")), 90)}")


def _get_pattern(part: int):
    wall = [int(x) for x in lib.get_input(part).split(",")]
    wall_len = len(wall)
    pattern = list[int]()
    i = 0
    while i < wall_len:
        if wall[i] > 0:
            pattern.append(i + 1)
            wall[i :: i + 1] = [x - 1 for x in wall[i :: i + 1]]
        else:
            i += 1
    return pattern


def part2():
    print(f"Part 2: {math.prod(_get_pattern(2))}")


def part3():
    pattern = _get_pattern(3)
    left, right = 1, 202520252025000 // min(pattern)
    while left < right:
        mid = (left + right + 1) // 2
        if _total_blocks(pattern, mid) <= 202520252025000:
            left = mid
        else:
            right = mid - 1
    print(f"Part 3: {left}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
