# pyright: strict

from typing import Final, Sequence

from everybody_codes_py_ft import common as lib

CARDINAL_NEIGBOURS: Final = (
             (0, -1),
    (-1, 0),          (1, 0),
             (0, 1)
) # fmt: skip

DIAGONAL_NEIGHBOURS: Final = (
    (-1, -1), (0, -1), (1, -1),
    (-1, 0),           (1, 0),
    (-1, 1),  (0, 1),  (1, 1),
) # fmt: skip


def _dig(data: str, neighbours: Sequence[tuple[int, int]] = CARDINAL_NEIGBOURS):
    grid = data.splitlines()
    blocks = set[tuple[int, int]]()
    for y, row in enumerate(grid):
        x = -1
        while (x := row.find("#", x + 1)) >= 0:
            blocks.add((x, y))
    total = len(blocks)
    while blocks:
        new_blocks = set[tuple[int, int]]()
        for x, y in blocks:
            for dx, dy in neighbours:
                if not (x + dx, y + dy) in blocks:
                    break
            else:
                new_blocks.add((x, y))
        total += len(new_blocks)
        blocks = new_blocks
    return total


def part1():
    print(f"Part 1: {_dig(lib.get_input(1))}")


def part2():
    print(f"Part 2: {_dig(lib.get_input(2))}")


def part3():
    print(f"Part 3: {_dig( lib.get_input(3), DIAGONAL_NEIGHBOURS)}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
