# pyright: strict

import re
from typing import TypeAlias

from everybody_codes_py_ft import common as lib

Complex: TypeAlias = tuple[int, int]


def _add(a: Complex, b: Complex) -> Complex:
    ax, ay = a
    bx, by = b
    return (ax + bx, ay + by)


def _mul(a: Complex, b: Complex) -> Complex:
    ax, ay = a
    bx, by = b
    return (ax * bx - ay * by, ax * by + ay * bx)


def _div(a: Complex, b: Complex) -> Complex:
    ax, ay = a
    bx, by = b
    return (
        ax // bx if ax >= 0 else -(-ax // bx),
        ay // by if ay >= 0 else -(-ay // by),
    )


def _parse_input(data: str) -> Complex:
    m = re.match(r"^A=\[(-?\d+),(-?\d+)\]$", data)
    if not m:
        raise Exception(f"Malformed input: '{data}'")
    return (int(m.group(1)), int(m.group(2)))


def part1():
    a = _parse_input(lib.get_input(1))
    res: Complex = (0, 0)
    for _ in range(3):
        res = _mul(res, res)
        res = _div(res, (10, 10))
        res = _add(res, a)

    print(f"Part 1: [{",".join(str(x) for x in res)}]")


def _engrave(a: Complex, width: int, height: int, size: int):
    count = 0
    for x in range(a[0], a[0] + width + 1, width // (size - 1)):
        for y in range(a[1], a[1] + height + 1, height // (size - 1)):
            p = (x, y)
            res = (0, 0)
            engrave = True
            for _ in range(100):
                res = _mul(res, res)
                res = _div(res, (100_000, 100_000))
                res = _add(res, p)
                if any(abs(r) > 1_000_000 for r in res):
                    engrave = False
                    break
            if engrave:
                count += 1
    return count


def part2():
    a = _parse_input(lib.get_input(2))
    print(f"Part 2: {_engrave(a, 1000, 1000, 101)}")


def part3():
    a = _parse_input(lib.get_input(3))
    print(f"Part 2: {_engrave(a, 1000, 1000, 1001)}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
