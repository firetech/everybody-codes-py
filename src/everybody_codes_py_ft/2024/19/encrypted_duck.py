# pyright: strict

import itertools as it
from typing import Final, TypeAlias, TypeVar

from everybody_codes_py_ft import common as lib

NEIGHBOURS: Final = (
    (-1, -1),
    (0, -1),
    (1, -1),
    (1, 0),
    (1, 1),
    (0, 1),
    (-1, 1),
    (-1, 0),
)

Pos: TypeAlias = tuple[int, int]
T = TypeVar("T", str, Pos)
Grid: TypeAlias = list[list[T]]


def _apply_mapping(grid: Grid[T], mapping: Grid[Pos]) -> Grid[T]:
    return [[grid[ny][nx] for nx, ny in row] for row in mapping]


def _decode(data: str, rounds: int):
    ops_in, grid_in = data.split("\n\n", 1)
    ops = it.cycle(ops_in)
    grid = [list(line) for line in grid_in.splitlines()]
    height = len(grid)
    width = len(grid[0])
    # Initialize map of grid position to rotated grid position
    mapping = [[(x, y) for x in range(width)] for y in range(height)]
    # Do one round of rotations on the mapping table
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            seq = [mapping[y + dy][x + dx] for dx, dy in NEIGHBOURS]
            match next(ops):
                case "R":
                    seq.insert(0, seq.pop())
                case "L":
                    seq.append(seq.pop(0))
                case other:
                    raise Exception(f"Unknown op '{other}'")
            for i, (dx, dy) in enumerate(NEIGHBOURS):
                mapping[y + dy][x + dx] = seq[i]

    # Exponentiation by squaring
    exp = 1
    while exp <= rounds:
        if exp & rounds:
            grid = _apply_mapping(grid, mapping)
        mapping = _apply_mapping(mapping, mapping)
        exp <<= 1

    # print("\n".join("".join(line) for line in grid))

    # Find resulting message
    for line in grid:
        try:
            start = line.index(">")
        except ValueError:
            continue
        end = line.index("<")
        return "".join(line[start + 1 : end])

    raise Exception("???")


def part1():
    print(f"Part 1: {_decode(lib.get_input(1), 1)}")


def part2():
    print(f"Part 2: {_decode(lib.get_input(2), 100)}")


def part3():
    print(f"Part 3: {_decode(lib.get_input(3), 1048576000)}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
