# pyright: strict

from collections import deque
from typing import TypeAlias

from everybody_codes_py_ft import common as lib

Pos: TypeAlias = tuple[int, int]


def _parse_input(part: int):
    grid = [[int(x) for x in line] for line in lib.get_input(part).splitlines()]
    width = len(grid[0])
    height = len(grid)
    return grid, width, height


def _burn(
    grid: list[list[int]],
    width: int,
    height: int,
    *start: Pos,
    seen: set[Pos] | None = None,
):
    burned = set(start)
    if seen:
        burned |= seen
    q = deque(start)
    while q:
        x, y = q.popleft()
        size = grid[y][x]
        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            nx = x + dx
            if nx < 0 or nx >= width:
                continue
            ny = y + dy
            if ny < 0 or ny >= height:
                continue
            if grid[ny][nx] > size:
                continue
            npos = (nx, ny)
            if npos in burned:
                continue
            burned.add(npos)
            q.append(npos)

    return burned


def part1():
    grid, width, height = _parse_input(1)
    print(f"Part 1: {len(_burn(grid, width, height, (0, 0)))}")


def part2():
    grid, width, height = _parse_input(2)
    print(f"Part 2: {len(_burn(grid, width, height, (0, 0), (width-1, height-1)))}")


def part3():
    grid, width, height = _parse_input(3)

    def _best_burn(burned: set[Pos]):
        seen = burned.copy()
        candidates = sorted(
            ((x, y) for y in range(height) for x in range(width)),
            key=lambda pos: grid[pos[1]][pos[0]],
            reverse=True,
        )
        best = set[Pos]()
        best_len = 0
        for pos in candidates:
            if pos in seen:
                continue
            this_burned = _burn(grid, width, height, pos, seen=burned) - burned
            seen |= this_burned
            this_len = len(this_burned)
            if this_len > best_len:
                best = this_burned
                best_len = this_len

        return best

    burned = set[Pos]()
    for _ in range(3):
        new_burned = _best_burn(burned)
        burned |= new_burned

    print(f"Part 3: {len(burned)}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
