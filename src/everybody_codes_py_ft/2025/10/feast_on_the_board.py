# pyright: strict

import functools as ft
from typing import Callable, Literal, TypeAlias

from everybody_codes_py_ft import common as lib

Pos: TypeAlias = tuple[int, int]


def _parse_input(part: int):
    lines = lib.get_input(part).splitlines()
    width = len(lines[0])
    height = len(lines)
    sheep = set[Pos]()
    hideouts = set[Pos]()
    dragon: Pos | None = None
    for y, line in enumerate(lib.get_input(part).splitlines()):
        for x, c in enumerate(line):
            pos = (x, y)
            if c == "S":
                sheep.add(pos)
            elif c == "D":
                dragon = pos
            elif c == "#":
                hideouts.add(pos)

    assert dragon

    return width, height, dragon, sheep, hideouts


def _valid_dragon_moves(width: int, height: int, pos: Pos):
    x, y = pos
    for dx, dy in (
        (-2, -1),
        (-2, 1),
        (-1, -2),
        (-1, 2),
        (2, -1),
        (2, 1),
        (1, -2),
        (1, 2),
    ):
        nx = x + dx
        if x < 0 or x >= width:
            continue
        ny = y + dy
        if y < 0 or y >= height:
            continue
        yield (nx, ny)


def _traverse(
    width: int,
    height: int,
    dragon: Pos,
    max_steps: int,
    callback: Callable[[Pos, int], None],
):
    q = [(dragon, 0)]
    visited = {(dragon, 0)}
    while q:
        pos, steps = q.pop(0)

        callback(pos, steps)

        if steps < max_steps:
            for npos in _valid_dragon_moves(width, height, pos):
                nstate = (npos, steps + 1)
                if nstate in visited:
                    continue
                visited.add(nstate)
                q.append(nstate)


def part1():
    width, height, dragon, sheep, _ = _parse_input(1)
    eaten_sheep = set[Pos]()

    def _traverse_cb(pos: Pos, steps: int):
        if pos in sheep:
            eaten_sheep.add(pos)

    _traverse(width, height, dragon, 4, _traverse_cb)

    print(f"Part 1: {len(eaten_sheep)}")


def part2():
    width, height, dragon, sheep, hideouts = _parse_input(2)
    sheep_at = {0: {pos: i for i, pos in enumerate(sheep)}}
    for steps in range(1, 21):
        sheep_at[steps] = {
            (x, y + steps): i for (x, y), i in sheep_at[0].items() if y + steps < height
        }

    eaten_sheep = set[int]()

    def _traverse_cb(pos: Pos, steps: int):
        if not pos in hideouts:
            if steps > 0 and pos in sheep_at[steps - 1]:
                eaten_sheep.add(sheep_at[steps - 1][pos])
            if pos in sheep_at[steps]:
                eaten_sheep.add(sheep_at[steps][pos])

    _traverse(width, height, dragon, 20, _traverse_cb)

    print(f"Part 2: {len(eaten_sheep)}")


def part3():
    width, height, dragon, sheep, hideouts = _parse_input(3)

    @ft.cache
    def _moves(
        dragon: Pos, sheep: frozenset[Pos], turn: Literal["dragon", "sheep"] = "sheep"
    ) -> int:
        if not sheep:
            return 1

        count = 0
        if turn == "sheep":
            can_move = False
            for pos in sheep:
                x, y = pos
                ny = y + 1
                if ny == height:
                    can_move = True
                npos = (x, ny)
                if ny < height and (npos in hideouts or npos != dragon):
                    can_move = True
                    nsheep = (sheep - {pos}) | {npos}
                    count += _moves(dragon, nsheep, "dragon")
            if not can_move:
                count += _moves(dragon, sheep, "dragon")
        else:
            x, y = dragon
            for ndragon in _valid_dragon_moves(width, height, dragon):
                if ndragon in hideouts:
                    nsheep = sheep
                else:
                    nsheep = sheep - {ndragon}
                count += _moves(ndragon, nsheep, "sheep")

        return count

    print(f"Part 3: {_moves(dragon, frozenset(sheep))}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
