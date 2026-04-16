# pyright: strict

import functools as ft
import itertools as it
import math
from typing import Final, TypeAlias

from everybody_codes_py_ft import common as lib

Wheel: TypeAlias = tuple[int, list[str]]


def _parse_wheels(data: str) -> list[Wheel]:
    steps_in, wheels_in = data.split("\n\n")

    wheels = [(int(steps), list[str]()) for steps in steps_in.split(",")]

    for line in wheels_in.splitlines():
        for w, i in enumerate(range(0, len(line), 4)):
            content = line[i : i + 3]
            if content.strip():
                wheels[w][1].append(content)

    return wheels


def part1():
    wheels = _parse_wheels(lib.get_input(1))
    line = " ".join(values[steps * 100 % len(values)] for steps, values in wheels)
    print(f"Part 1: {line}")


def _score(wheels: list[Wheel], pull: int, offset: int):
    if pull < 1:
        return 0
    line = [values[(offset + steps * pull) % len(values)] for steps, values in wheels]
    eyes = [eye for face in line for eye in (face[0], face[-1])]
    counts = {eye: eyes.count(eye) for eye in set(eyes)}
    return sum(count - 2 for count in counts.values() if count >= 3)


PART2_TARGET: Final = 202420242024


def part2():
    wheels = _parse_wheels(lib.get_input(2))

    lcm = math.lcm(*(len(values) for _, values in wheels))
    q = PART2_TARGET // lcm
    r = PART2_TARGET % lcm

    coins_at = list(it.accumulate(_score(wheels, p + 1, 0) for p in range(lcm)))

    print(f"Part 2: {coins_at[r-1] + q * coins_at[lcm-1]}")


def part3():
    wheels = _parse_wheels(lib.get_input(3))

    @ft.cache
    def _minmax_score(pull: int = 0, offset: int = 0) -> tuple[int, int]:
        score = _score(wheels, pull, offset)
        if pull < 256:
            sub_results = [_minmax_score(pull + 1, offset + o) for o in (-1, 0, 1)]
            return (
                score + min(sub_min for sub_min, _ in sub_results),
                score + max(sub_max for _, sub_max in sub_results),
            )
        return (score, score)

    min_score, max_score = _minmax_score()

    print(f"Part 3: {max_score} {min_score}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
