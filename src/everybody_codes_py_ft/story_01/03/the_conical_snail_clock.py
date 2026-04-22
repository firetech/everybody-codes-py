# pyright: strict

import functools as ft
import re

from everybody_codes_py_ft import common as lib


def _parse_input(data: str):
    for line in data.splitlines():
        m = re.match(r"^x=(\d+) y=(\d+)$", line)
        if m:
            yield tuple(int(val) for val in m.groups())
        else:
            raise Exception(f"Malformed line: '{line}'")


def part1():
    def _new_pos(x: int, y: int):
        diagonal = x + y - 1
        move = 100 % diagonal
        nx = x + move
        if nx > diagonal:
            nx -= diagonal
        ny = y - move
        if ny < 1:
            ny += diagonal
        return nx + 100 * ny

    print(f"Part 1: {sum(_new_pos(x, y) for x, y in _parse_input(lib.get_input(1)))}")


def _state(x: int, y: int):
    diagonal = x + y - 1
    # steps from current to y=1
    remaining = (y - 1) % diagonal
    return diagonal, remaining


# Adapted from https://rosettacode.org/wiki/Chinese_remainder_theorem#Python_3.6
def _mul_inv(a: int, b: int):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


def _chinese_remainder(states: list[tuple[int, int]]):
    sum = 0
    prod = ft.reduce(lambda a, b: a * b, (mod for mod, _ in states))
    for mod, remainder in states:
        p = prod // mod
        sum += remainder * _mul_inv(p, mod) * p
    return sum % prod


def part2():
    states = [_state(x, y) for x, y in _parse_input(lib.get_input(2))]
    print(f"Part 2: {_chinese_remainder(states)}")


def part3():
    states = [_state(x, y) for x, y in _parse_input(lib.get_input(3))]
    print(f"Part 3: {_chinese_remainder(states)}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
