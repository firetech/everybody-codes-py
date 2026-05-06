# pyright: strict

import itertools as it

from everybody_codes_py_ft import common as lib


def part1():
    path = [int(x) for x in lib.get_input(1).split(",")]
    total_nails = max(path)  # Fingers crossed this works...
    centers = sum(abs(a - b) == total_nails / 2 for a, b in it.pairwise(path))
    print(f"Part 1: {centers}")


def part2():
    path = [int(x) for x in lib.get_input(2).split(",")]
    visited = list[tuple[int, int]]()
    knots = 0
    for a, b in it.pairwise(path):
        if a > b:
            a, b = b, a
        for va, vb in visited:
            if (a > va and a < vb and b > vb) or (a < va and b < vb and b > va):
                knots += 1
        visited.append((a, b))
    print(f"Part 2: {knots}")


def part3():
    path = [int(x) for x in lib.get_input(3).split(",")]
    total_nails = max(path)  # Fingers crossed this works...
    shield = [tuple(sorted(pair)) for pair in it.pairwise(path)]
    most_cuts = 0
    for a in range(1, total_nails):
        for b in range(a + 1, total_nails + 1):
            cuts = 0
            for sa, sb in shield:
                if (
                    (a > sa and a < sb and b > sb)
                    or (a < sa and b < sb and b > sa)
                    or (a == sa and b == sb)
                ):
                    cuts += 1
            if cuts > most_cuts:
                most_cuts = cuts
    print(f"Part 3: {most_cuts}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
