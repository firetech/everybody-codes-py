# pyright: strict

import itertools as it
from collections import deque

from everybody_codes_py_ft import common as lib


def part1():
    balloons = lib.get_input(1).strip()
    bolts = it.cycle("RGB")
    bolt = next(bolts)
    used = 1
    last_b = len(balloons) - 1
    for b, balloon in enumerate(balloons):
        if bolt != balloon and b < last_b:
            bolt = next(bolts)
            used += 1

    print(f"Part 1: {used}")


def _circle_pop(data: str, repeats: int = 100):
    fragment = list(data.strip())
    circle = fragment * repeats
    half = len(circle) // 2
    circle1 = deque(circle[:half])
    circle2 = deque(circle[half:])
    bolts = it.cycle("RGB")
    used = 0
    while circle1 or circle2:
        bolt = next(bolts)
        used += 1
        while len(circle2) > len(circle1):
            circle1.append(circle2.popleft())
        even = len(circle1) == len(circle2)
        balloon = circle1.popleft()
        if balloon == bolt and even:
            circle2.popleft()
    return used


def part2():
    print(f"Part 2: {_circle_pop(lib.get_input(2))}")


def part3():
    print(f"Part 3: {_circle_pop(lib.get_input(3), 100_000)}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
