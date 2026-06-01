# pyright: strict

import heapq
from collections import defaultdict

from everybody_codes_py_ft import common as lib


def _parse_input(part: int):
    walls = defaultdict[int, list[tuple[int, int]]](list)
    for line in lib.get_input(part).splitlines():
        x, start, height = (int(n) for n in line.split(","))
        walls[x].append((start, start + height - 1))
    return dict(walls)


def _traverse(part: int):
    walls = _parse_input(part)
    wall_xs = [0] + sorted(walls.keys())
    end_i = len(wall_xs) - 1
    q = [(0, 0, 0)]
    dist = {(0, 0): 0}

    def _neighbours(i: int, y: int):
        x = wall_xs[i]
        ni = i + 1
        nx = wall_xs[ni]
        gap = nx - x
        y_parity = (y + gap) & 1
        result = list[tuple[int, int, int]]()
        for low, high in walls[nx]:
            low = max(low, y - gap)
            high = min(high, y + gap)
            if high < low:
                continue

            low_y = low if low & 1 == y_parity else low + 1
            if low_y <= high:
                cost = (gap + (low_y - y)) // 2
                if cost >= 0 and cost <= gap:
                    result.append((cost, ni, low_y))

            high_y = high if (high & 1) == y_parity else high - 1
            if high >= low and high_y != low_y:
                cost = (gap + (high_y - y)) // 2
                if cost >= 0 and cost <= gap:
                    result.append((cost, ni, high_y))

        return result

    while q:
        flaps, i, y = heapq.heappop(q)

        if flaps > dist[(i, y)]:
            # Old entry
            continue

        if i == end_i:
            return flaps

        for cost, ni, ny in _neighbours(i, y):
            nflaps = flaps + cost
            if nflaps >= dist.get((ni, ny), 0xFFFFFFFF):
                continue
            dist[(ni, ny)] = nflaps

            heapq.heappush(q, (nflaps, ni, ny))


def part1():
    print(f"Part 1: {_traverse(1)}")


def part2():
    print(f"Part 2: {_traverse(2)}")


def part3():
    print(f"Part 3: {_traverse(3)}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
