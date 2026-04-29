# pyright: strict

import itertools as it
import math

from everybody_codes_py_ft import common as lib


def _simple_gear_ratio(data: str):
    # Only the first and last gears actually matter. Mathematically:
    #   ratio = (gear1 / gear2) * (gear2 / gear3) * (gear3 / gear4) = gear1 / gear4
    lines = data.splitlines()
    return int(lines[0]) / int(lines[-1])


def part1():
    ratio = _simple_gear_ratio(lib.get_input(1))
    print(f"Part 1: {math.floor(2025 * ratio)}")


def part2():
    ratio = _simple_gear_ratio(lib.get_input(2))
    print(f"Part 2: {math.ceil(10_000_000_000_000 / ratio)}")


def part3():
    gears = [
        (
            tuple(int(g) for g in line.split("|"))
            if "|" in line
            else (int(line), int(line))
        )
        for line in lib.get_input(3).splitlines()
    ]
    ratio = 1.0
    for (_, out1), (in2, _) in it.pairwise(gears):
        ratio *= out1 / in2
    print(f"Part 3: {math.floor(100 * ratio)}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
