# pyright: strict

import itertools as it

from everybody_codes_py_ft import common as lib


def part1():
    wheel = [1]
    lefts = list[int]()
    for right, *left in it.batched(
        (int(line) for line in lib.get_input(1).splitlines()), 2
    ):
        wheel.append(right)
        if left:
            lefts.extend(left)
    wheel.extend(lefts[::-1])
    print(f"Part 1: {wheel[2025 % len(wheel)]}")


def _range_wheel(part: int, moves: int):
    wheel = [range(1, 2)]
    lefts = list[range]()
    for (right_start, right_end), *left in it.batched(
        (line.split("-") for line in lib.get_input(part).splitlines()), 2
    ):
        wheel.append(range(int(right_start), int(right_end) + 1))
        if left:
            left_start, left_end = left[0]
            lefts.append(range(int(left_end), int(left_start) - 1, -1))
    wheel.extend(lefts[::-1])

    range_lens = [len(r) for r in wheel]
    positions = sum(range_lens)
    end_pos = moves % positions
    i = 0
    while end_pos >= range_lens[i]:
        end_pos -= range_lens[i]
        i += 1
    return wheel[i][end_pos]


def part2():
    print(f"Part 2: {_range_wheel(2, 20252025)}")


def part3():
    print(f"Part 3: {_range_wheel(3, 202520252025)}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
