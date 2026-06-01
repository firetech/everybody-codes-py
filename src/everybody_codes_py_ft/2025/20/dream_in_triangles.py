# pyright: strict

import itertools as it
from collections import deque
from typing import TypeAlias

from everybody_codes_py_ft import common as lib

Pos: TypeAlias = tuple[int, int]
Chart: TypeAlias = dict[Pos, str]


def _parse_input(part: int) -> Chart:
    return {
        (x, y): c
        for y, line in enumerate(lib.get_input(part).splitlines())
        for x, c in enumerate(line)
        if c != "."
    }


def _neighbours(x: int, y: int, chart: Chart):
    return {
        (nx, ny)
        for nx, ny in (
            (x - 1, y),
            (x + 1, y),
            (x, y + (1 if (x + y) & 1 else -1)),
        )
        if (nx, ny) in chart
    }


def part1():
    chart = _parse_input(1)
    pairs = set[tuple[Pos, Pos]]()
    for (x, y), c in chart.items():
        if c != "T":
            continue
        pos = (x, y)
        for nx, ny in _neighbours(x, y, chart):
            if chart[(nx, ny)] == "T":
                npos = (nx, ny)
                if pos > npos:
                    pairs.add((npos, pos))
                else:
                    pairs.add((pos, npos))

    print(f"Part 1: {len(pairs)}")


def part2():
    chart = _parse_input(2)
    visited = {pos for pos, c in chart.items() if c == "S"}
    q = deque((*start, 0) for start in visited)
    while q:
        x, y, jumps = q.popleft()

        if chart[(x, y)] == "E":
            print(f"Part 2: {jumps}")
            break

        for npos in _neighbours(x, y, chart):
            if npos in visited:
                continue
            if chart[npos] != "#":
                visited.add(npos)
                q.append((*npos, jumps + 1))


def _rotate(chart: Chart):
    side = max(x for (x, _) in chart)
    return {
        ((side + (x - y) // 2 - y - x), (x - y) // 2): c for (x, y), c in chart.items()
    }


def part3():
    base_chart = _parse_input(3)
    charts = (
        base_chart,
        (rot_once := _rotate(base_chart)),
        _rotate(rot_once),
    )
    visited = {(*pos, 0) for pos, c in base_chart.items() if c == "S"}
    q = deque((*start, 0) for start in visited)
    while q:
        x, y, r, jumps = q.popleft()

        if charts[r][(x, y)] == "E":
            print(f"Part 3: {jumps}")
            break

        nr = (r + 1) % 3
        for nxy in it.chain(((x, y),), _neighbours(x, y, charts[nr])):
            npos = (*nxy, nr)
            if npos in visited:
                continue
            if charts[nr][nxy] != "#":
                visited.add(npos)
                q.append((*npos, jumps + 1))


if __name__ == "__main__":
    part1()
    part2()
    part3()
