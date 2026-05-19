# pyright: strict

import heapq
import math
from typing import Final, cast

from everybody_codes_py_ft import common as lib


def _parse_input(part: int):
    lines = lib.get_input(part).splitlines()
    grid = [[int(x) if x not in ("@", "S") else 0 for x in line] for line in lines]
    specials = {
        c: (x, y)
        for y, line in enumerate(lines)
        for x, c in enumerate(line)
        if grid[y][x] == 0
    }
    return grid, specials


def part1():
    grid, specials = _parse_input(1)
    vx, vy = specials["@"]
    destroyed_total = sum(
        value
        for y, line in enumerate(grid)
        for x, value in enumerate(line)
        if (vx - x) * (vx - x) + (vy - y) * (vy - y) <= 100
    )
    print(f"Part 1: {destroyed_total}")


def part2():
    grid, specials = _parse_input(2)
    vx, vy = specials["@"]
    destroyed_totals = [
        sum(
            value
            for y, line in enumerate(grid)
            for x, value in enumerate(line)
            if (vx - x) * (vx - x) + (vy - y) * (vy - y) <= r * r
        )
        for r in range(1, math.ceil(math.sqrt(vx * vx + vy * vy)))
    ]
    worst_increase = max(
        range(0, len(destroyed_totals)),
        key=lambda i: destroyed_totals[i] - (destroyed_totals[i - 1] if i > 0 else 0),
    )
    print(
        f"Part 2: {(worst_increase+1)*(destroyed_totals[worst_increase] - destroyed_totals[worst_increase-1])}"
    )


MAX_COST: Final = 0xFFFFFFFF


def part3():
    grid, specials = _parse_input(3)
    vx, vy = specials["@"]
    sx, sy = specials["S"]
    width = len(grid[0])
    height = len(grid)

    radius_grid = [
        [
            math.ceil(math.sqrt((vx - x) * (vx - x) + (vy - y) * (vy - y)))
            for x in range(width)
        ]
        for y in range(height)
    ]

    start = (sx, sy)
    start_state = (start, cast(bool, False), radius_grid[sy][sx])
    q = [(0, *start_state)]
    cost = {start_state: 0}
    result = -1
    while q:
        time, pos, circled, min_radius = heapq.heappop(q)

        if time > cost[(pos, circled, min_radius)]:
            continue

        if pos == start and circled:
            result = time * (time // 30)
            break

        x, y = pos
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nx = x + dx
            if nx < 0 or nx >= width:
                continue
            ny = y + dy
            if ny < 0 or ny >= height:
                continue

            # Check if we are circling the volcano or not (winding numbers)
            ncircled = circled
            if ny > vy:
                if x < vx and nx == vx:
                    ncircled = True
                elif x >= vx and nx < vx:
                    ncircled = False

            # Don't allow destroyed positions
            ntime = time + grid[ny][nx]
            nradius = min(radius_grid[ny][nx], min_radius)
            if nradius <= ntime // 30:
                continue

            npos = (nx, ny)
            nstate = (npos, ncircled, nradius)
            if ntime < cost.get(nstate, MAX_COST):
                cost[nstate] = ntime
                heapq.heappush(q, (ntime, *nstate))

    print(f"Part 3: {result}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
