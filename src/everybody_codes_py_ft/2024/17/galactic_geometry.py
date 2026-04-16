# pyright: strict

import functools as ft
import heapq
from typing import TypeAlias

from everybody_codes_py_ft import common as lib

Pos: TypeAlias = tuple[int, int]


def _find_stars(data: str) -> list[Pos]:
    return [
        (x, y)
        for y, line in enumerate(data.splitlines())
        for x, c in enumerate(line)
        if c == "*"
    ]


def _dist(a: Pos, b: Pos):
    ax, ay = a
    bx, by = b
    return abs(ax - bx) + abs(ay - by)


def _constellation(stars: list[Pos]):
    q = [(0, stars[0])]
    remaining = {*stars}
    dist_sum = 0

    while remaining:
        dist, star = heapq.heappop(q)
        if star in remaining:
            remaining.remove(star)
            dist_sum += dist
            for other in remaining:
                heapq.heappush(q, (_dist(star, other), other))
    return dist_sum + len(stars)


def part1():
    stars = _find_stars(lib.get_input(1))
    print(f"Part 1: {_constellation(stars)}")


def part2():
    stars = _find_stars(lib.get_input(2))
    print(f"Part 2: {_constellation(stars)}")


def part3():
    stars = _find_stars(lib.get_input(3))
    groups = dict[int, list[Pos]]()
    star_group = dict[Pos, int]()
    next_group = 0

    for first in stars:
        group_id = star_group.get(first)
        if group_id is None:
            # New group
            group_id = next_group
            next_group += 1
            groups[group_id] = [first]
            star_group[first] = group_id
        for second in stars:
            if second == first or _dist(first, second) >= 6:
                continue
            existing_id = star_group.get(second)
            if existing_id is None:
                # New star, add to group
                star_group[second] = group_id
                groups[group_id].append(second)
            elif existing_id == group_id:
                continue
            else:
                # Merge groups
                groups[group_id].extend(groups[existing_id])
                for other in groups[existing_id]:
                    star_group[other] = group_id
                del groups[existing_id]

    group_constellations = sorted(
        (_constellation(members) for members in groups.values()), reverse=True
    )
    result = ft.reduce(lambda p, g: p * g, group_constellations[0:3], 1)

    print(f"Part 3: {result}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
