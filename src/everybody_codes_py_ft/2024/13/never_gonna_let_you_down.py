# pyright: strict

import heapq
from collections import defaultdict

from everybody_codes_py_ft import common as lib


def _neighbours(x: int, y: int):
    return (
        (x - 1, y),
        (x + 1, y),
        (x, y - 1),
        (x, y + 1),
    )


def _level(char: str):
    if char in ("S", "E"):
        return 0
    try:
        return int(char)
    except ValueError:
        # Walls
        return None


def _traverse(data: str):
    raw_map = [list(line) for line in data.splitlines()]
    starts = [
        (x, y) for y, row in enumerate(raw_map) for x, c in enumerate(row) if c == "S"
    ]
    assert len(starts) >= 1, "No start?"
    ends = [
        (x, y) for y, row in enumerate(raw_map) for x, c in enumerate(row) if c == "E"
    ]
    assert len(ends) == 1, "No end in sight?"
    end = ends[0]
    level_map = [[_level(c) for c in line] for line in raw_map]

    queue = [(0, *start) for start in starts]
    heapq.heapify(queue)
    dist = defaultdict(lambda: float("inf"), {start: 0 for start in starts})
    while queue:
        time, x, y = heapq.heappop(queue)

        if time > dist[(x, y)]:
            continue

        level_from = level_map[y][x]
        assert level_from is not None
        for nx, ny in _neighbours(x, y):
            try:
                level_to = level_map[ny][nx]
                assert level_to is not None
            except (IndexError, AssertionError):
                # Walls or outside map
                continue
            diff = abs(level_to - level_from)
            target_time = time + min(diff, 10 - diff) + 1
            if target_time < dist[(nx, ny)]:
                dist[(nx, ny)] = target_time
                heapq.heappush(queue, (target_time, nx, ny))

    return dist[end]


def part1():
    print(f"Part 1: {_traverse(lib.get_input(1))}")


def part2():
    print(f"Part 2: {_traverse(lib.get_input(2))}")


def part3():
    print(f"Part 3: {_traverse(lib.get_input(3))}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
