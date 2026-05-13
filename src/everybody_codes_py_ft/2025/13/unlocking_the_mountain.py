# pyright: strict

import itertools as it
from collections import deque
from typing import TypeVar

from everybody_codes_py_ft import common as lib

T = TypeVar("T")


def _make_wheel(initial: T, rest: list[T]):
    wheel = deque[T]((initial,))
    for right, *left in it.batched(rest, 2):
        wheel.append(right)
        if left:
            wheel.appendleft(left[0])
    while wheel[0] != initial:
        wheel.append(wheel.popleft())
    return wheel


def part1():
    wheel = _make_wheel(1, [int(line) for line in lib.get_input(1).splitlines()])
    print(f"Part 1: {wheel[2025 % len(wheel)]}")


def _range_wheel(part: int, moves: int):
    wheel = _make_wheel(
        range(1, 2),
        [
            (
                range(int(start), int(end) + 1)
                if i % 2 == 0
                else range(int(end), int(start) - 1, -1)
            )
            for i, (start, end) in enumerate(
                line.split("-") for line in lib.get_input(part).splitlines()
            )
        ],
    )
    range_lens = [len(r) for r in wheel]
    positions = sum(range_lens)
    end_pos = moves % positions
    while end_pos >= (pop_len := len(wheel[0])):
        end_pos -= pop_len
        wheel.popleft()
    return wheel[0][end_pos]


def part2():
    print(f"Part 2: {_range_wheel(2, 20252025)}")


def part3():
    print(f"Part 3: {_range_wheel(3, 202520252025)}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
