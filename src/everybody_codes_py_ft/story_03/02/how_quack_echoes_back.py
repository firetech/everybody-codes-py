# pyright: strict

import itertools as it
from collections import deque
from typing import Callable, TypeAlias

from everybody_codes_py_ft import common as lib

Pos: TypeAlias = tuple[int, int]


def _parse_input(part: int):
    start = None
    ends = set[Pos]()
    for y, line in enumerate(lib.get_input(part).splitlines()):
        for x, c in enumerate(line):
            if c == "@":
                start = (x, y)
            elif c == "#":
                ends.add((x, y))
    return start, ends


MOVES = (
    (0, -1),  # up
    (1, 0),  # right
    (0, 1),  # down
    (-1, 0),  # left
)


def _traverse(
    start: Pos,
    condition: Callable[[Pos, set[Pos]], bool],
    visited_extra: set[Pos] | None = None,
    moves: tuple[Pos, ...] = MOVES,
) -> int:
    visited = {start, *(visited_extra or ())}

    def _is_surrounded(pos: Pos):
        x, y = pos
        return all((x + dx, y + dy) in visited for dx, dy in MOVES)

    pos = start
    steps = 0
    move_cycle = it.cycle(moves)
    while not condition(pos, visited):
        npos = pos
        x, y = pos
        while npos in visited:
            dx, dy = next(move_cycle)
            npos = (x + dx, y + dy)
        visited.add(npos)
        for dx, dy in MOVES:
            nnpos = (npos[0] + dx, npos[1] + dy)
            if nnpos not in visited and _is_surrounded(nnpos):
                visited.add(nnpos)
        pos = npos
        steps += 1
    return steps


def part1():
    start, ends = _parse_input(1)
    assert start and ends
    end = ends.pop()
    print(f"Part 1: {_traverse(start, lambda pos, _: pos == end)}")


def part2():
    start, ends = _parse_input(2)
    assert start and ends
    end_sides = {(x + dx, y + dy) for x, y in ends for dx, dy in MOVES}
    steps = _traverse(
        start,
        lambda _, visited: end_sides.issubset(visited),
        ends,
    )
    print(f"Part 2: {steps}")


def part3():
    start, ends = _parse_input(3)
    assert start and ends

    last_seen = set[Pos]()

    def _flood_void(visited: set[Pos]):
        # Flood fill from outside. If a bone is found, we're not done.
        all_x, all_y = zip(*visited)
        min_x = min(all_x) - 1
        max_x = max(all_x) + 1
        min_y = min(all_y) - 1
        max_y = max(all_y) + 1

        surrounded = True
        seen = visited.copy()
        q = deque([(min_x, min_y)])
        while q:
            x, y = q.popleft()
            for dx, dy in MOVES:
                nx = x + dx
                if nx < min_x or nx > max_x:
                    continue
                ny = y + dy
                if ny < min_y or ny > max_y:
                    continue
                npos = (nx, ny)
                if npos in ends:
                    surrounded = False
                if npos in seen:
                    continue
                seen.add(npos)
                q.append(npos)

        if surrounded:
            return True

        # Add all positions not visited (i.e. surrounded by the wave) to the wave.
        for surrounded_pos in last_seen - seen:
            visited.add(surrounded_pos)
        last_seen.clear()
        last_seen.update(seen)
        return False

    steps = _traverse(
        start,
        lambda _, visited: _flood_void(visited),
        ends,
        tuple(dpos for dpos in MOVES for _ in range(3)),
    )
    print(f"Part 3: {steps}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
