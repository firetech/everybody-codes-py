# pyright: strict

import itertools as it
from collections import defaultdict

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
    delta = defaultdict[int, int](lambda: 0)
    strings = defaultdict[int, list[int]](list)
    for a, b in it.pairwise(path):
        if a > b:
            a, b = b, a
        strings[a].append(b)
        delta[a + 1] += 1
        delta[b] -= 1

    most_cuts = 0
    for a in range(1, total_nails):
        # Alter delta for strings starting from this nail.
        for b in strings[a]:
            delta[b] += 2  # Collinear if cut goes a->b, change delta from -1 to +1.
            delta[b + 1] -= 1  # Account for the extra +1 above.

        # Alter delta for strings starting from previous nail.
        for b in strings[a - 1]:
            delta[b] -= 1  # Previously collinear, should no longer affect count at b.
            delta[b + 1] += 2  # Switch from -1 to +1, include in cuts a->(>=b+1).

        cuts = 0

        # Count cuts going from a to >=a+2.
        # (a->a+1 is not a meaningful cut, and would break the encoding used for delta)
        for b in range(a + 2, total_nails + 1):
            cuts += delta[b]
            if cuts > most_cuts:
                most_cuts = cuts
    print(f"Part 3: {most_cuts}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
