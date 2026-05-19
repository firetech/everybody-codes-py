# pyright: strict

import heapq
import math
from typing import Final

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

    def _circle_volcano(min_radius: int):
        q = [(0, sx, sy, False)]
        cost = {(sx, sy, False): 0}

        while q:
            time, x, y, circled = heapq.heappop(q)

            if time > cost[(x, y, circled)]:
                continue

            if x == sx and y == sy and circled:
                return time

            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                nx = x + dx
                if nx < 0 or nx >= width:
                    continue
                ny = y + dy
                if ny < 0 or ny >= height:
                    continue

                if radius_grid[ny][nx] <= min_radius:
                    continue

                # Check if we are circling the volcano or not (winding numbers)
                ncircled = circled
                if ny > vy:
                    if x < vx and nx == vx:
                        ncircled = True
                    elif x >= vx and nx < vx:
                        ncircled = False

                ntime = time + grid[ny][nx]

                nstate = (nx, ny, ncircled)
                if ntime < cost.get(nstate, MAX_COST):
                    cost[nstate] = ntime
                    heapq.heappush(q, (ntime, *nstate))

        return MAX_COST

    for radius in range(1, max(max(line) for line in radius_grid)):
        min_time = _circle_volcano(radius)
        if min_time < (radius + 1) * 30:
            print(f"Part 3: {min_time * radius}")
            return

    raise Exception("Not possible")


if __name__ == "__main__":
    part1()
    part2()
    part3()
