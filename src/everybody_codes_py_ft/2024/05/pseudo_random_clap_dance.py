# pyright: strict

import math
from collections import defaultdict
from typing import TypeAlias

from everybody_codes_py_ft import common as lib

Columns: TypeAlias = list[list[int]]


def _columns(data: str):
    grid = [[int(n) for n in line.split(" ")] for line in data.splitlines()]
    return [list(col) for col in zip(*grid)]


def _round(columns: Columns, round_: int):
    clapper = columns[round_ % len(columns)].pop(0)
    target = (round_ + 1) % len(columns)
    lap = 2 * len(columns[target])
    rem = (clapper - 1) % lap
    columns[target].insert(min(rem, lap - rem), clapper)


def _value(columns: Columns):
    return int("".join(str(col[0]) for col in columns))


def _key(columns: Columns):
    k = 0
    for col in columns:
        for val in col:
            exp = math.floor(math.log2(val)) + 1 if val != 0 else 1

            k = k << exp | val
    return k


def part1():
    columns = _columns(lib.get_input(1))
    for r in range(10):
        _round(columns, r)
    print(f"Part 1: {_value(columns)}")


def part2():
    columns = _columns(lib.get_input(2))
    counts = defaultdict[int, int](lambda: 0)
    r = 0

    while True:
        _round(columns, r)
        r += 1

        val = _value(columns)
        counts[val] += 1
        if counts[val] == 2024:
            print(f"Part 2: {val * r}")
            break


def part3():
    columns = _columns(lib.get_input(3))
    key = _key(columns)
    seen = dict[int, int]()
    r = 0

    while key not in seen:
        seen[key] = _value(columns)
        _round(columns, r)
        key = _key(columns)
        r += 1

    max_key = max(seen, key=lambda k: seen[k])

    print(f"Part 3: {seen[max_key]}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
