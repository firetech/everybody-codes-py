# pyright: strict

from typing import Sequence, cast

from everybody_codes_py_ft import common as lib


def _precompute(max_val: int, stamps: tuple[int, ...]) -> Sequence[int]:
    index = [float("inf")] * (max_val + 1)
    index[0] = 0
    for target in range(1, max_val + 1):
        index[target] = int(
            min(
                index[target],
                *(
                    index[target - stamp] + 1
                    for stamp in reversed(stamps)
                    if target >= stamp
                ),
            )
        )
    return cast(list[int], index)


def part1():
    balls = [int(line) for line in lib.get_input(1).splitlines()]
    index = _precompute(max(balls), (1, 3, 5, 10))
    beetles = sum(index[ball] for ball in balls)
    print(f"Part 1: {beetles}")


def part2():
    balls = [int(line) for line in lib.get_input(2).splitlines()]
    index = _precompute(max(balls), (1, 3, 5, 10, 15, 16, 20, 24, 25, 30))
    beetles = sum(index[ball] for ball in balls)
    print(f"Part 2: {beetles}")


def part3():
    balls = [int(line) for line in lib.get_input(3).splitlines()]
    index = _precompute(
        max(balls) // 2 + 50,
        (1, 3, 5, 10, 15, 16, 20, 24, 25, 30, 37, 38, 49, 50, 74, 75, 100, 101),
    )
    beetles = sum(
        min(
            index[first] + index[ball - first]
            for first in range(ball // 2, ball // 2 + 51)
        )
        for ball in balls
    )
    print(f"Part 3: {beetles}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
