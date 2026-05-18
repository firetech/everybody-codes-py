# pyright: strict

import heapq
from typing import Final, TypeAlias

from everybody_codes_py_ft import common as lib

DIRS: Final = ((0, -1), (1, 0), (0, 1), (-1, 0))

Pos: TypeAlias = tuple[int, int]
Chart: TypeAlias = set[Pos]


def _parse_input(part: int) -> tuple[Chart, Pos]:
    current_dir = 0
    x = 0
    y = 0
    chart = Chart()
    for op in lib.get_input(part).split(","):
        match op[0]:
            case "R":
                current_dir += 1
            case "L":
                current_dir -= 1
            case other:
                raise Exception(f"Unknown direction '{other}'")
        current_dir %= len(DIRS)
        dx, dy = DIRS[current_dir]
        for _ in range(int(op[1:])):
            chart.add((x, y))
            x += dx
            y += dy
    return chart, (x, y)


def _traverse(part: int):
    chart, end = _parse_input(part)
    ex, ey = end
    start: Pos = (0, 0)
    q: list[tuple[int, int, Pos]] = [(0, 0, start)]
    seen: set[Pos] = {start}
    while q:
        _, steps, pos = heapq.heappop(q)

        if pos == end:
            return steps

        x, y = pos
        nsteps = steps + 1
        for dx, dy in DIRS:
            nx = x + dx
            ny = y + dy
            npos = (nx, ny)
            if npos in seen or npos in chart:
                continue
            seen.add(npos)
            heapq.heappush(q, (nsteps + (abs(ex - nx) + abs(ey - ny)), nsteps, npos))

    return -1


def part1():
    print(f"Part 1: {_traverse(1)}")


def part2():
    # Uses the same example as part 1 (none given)
    print(f"Part 2: {_traverse(2)}")


def part3():
    # Uses the same example as part 1 (none given)
    print(f"Part 3: {_traverse(3)}")


if __name__ == "__main__":
    part1()
    part2()
    # part3()
