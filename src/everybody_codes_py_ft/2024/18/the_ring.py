# pyright: strict

from typing import Final, TypeAlias

from everybody_codes_py_ft import common as lib

DIRS: Final = ((-1, 0), (1, 0), (0, -1), (0, 1))

Pos: TypeAlias = tuple[int, int]


def _parse_map(data: str) -> tuple[set[Pos], set[Pos], set[Pos]]:
    lines = data.splitlines()
    width = len(lines[0])
    height = len(lines)
    chart = {
        (x, y): c == "P"
        for y, line in enumerate(lines)
        for x, c in enumerate(line)
        if c != "#"
    }
    palms = {pos for pos in chart if chart[pos]}
    starts = {
        (x, y)
        for x, y in chart
        if x == 0 or y == 0 or x == width - 1 or y == height - 1
    }
    return set(chart.keys()), starts, palms


def _traverse_map(data: str):
    chart, visited, remaining = _parse_map(data)
    q = [(pos, 0) for pos in visited]

    while remaining and q:
        pos, time = q.pop(0)

        if pos in remaining:
            remaining.remove(pos)
            if not remaining:
                return time

        x, y = pos
        ntime = time + 1
        for dx, dy in DIRS:
            npos = (x + dx, y + dy)
            if npos in chart and npos not in visited:
                visited.add(npos)
                q.append((npos, ntime))

    return -1


def part1():
    print(f"Part 1: {_traverse_map(lib.get_input(1))}")


def part2():
    print(f"Part 2: {_traverse_map(lib.get_input(2))}")


def _fill_from(chart: set[Pos], start: Pos, dist: dict[Pos, int]):
    q = [(start, 0)]
    visited = {start}
    while q:
        pos, time = q.pop(0)
        dist[pos] = dist.get(pos, 0) + time

        x, y = pos
        ntime = time + 1
        for dx, dy in DIRS:
            npos = (x + dx, y + dy)
            if npos in chart and npos not in visited:
                visited.add(npos)
                q.append((npos, ntime))


def part3():
    chart, _, palms = _parse_map(lib.get_input(3))
    dist = dict[Pos, int]()
    # Fill dist with the total distance to all palms from each point
    for palm in palms:
        _fill_from(chart, palm, dist)
    # Find point with minimum distance that isn't a palm itself.
    min_dist = min(total for pos, total in dist.items() if pos not in palms)
    print(f"Part 3: {min_dist}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
