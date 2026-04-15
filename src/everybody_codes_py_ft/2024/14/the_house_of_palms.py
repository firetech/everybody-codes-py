# pyright: strict

from collections import defaultdict
from typing import Callable, Final, TypeAlias

from everybody_codes_py_ft import common as lib

Pos: TypeAlias = tuple[int, int, int]
PosCallback: TypeAlias = Callable[[Pos, bool], None]


def _dir_delta(dir_str: str) -> Pos:
    match dir_str:
        case "U":
            return (0, 1, 0)
        case "D":
            return (0, -1, 0)
        case "R":
            return (1, 0, 0)
        case "L":
            return (-1, 0, 0)
        case "F":
            return (0, 0, 1)
        case "B":
            return (0, 0, -1)
        case other:
            raise Exception(f"Unknown direction '{other}'")


NEIGHBOURS: Final = tuple(_dir_delta(s) for s in ("U", "D", "R", "L", "F", "B"))


def _traverse_tree(data: str, cb: PosCallback):
    for line in data.splitlines():
        x, y, z = 0, 0, 0
        ops = line.split(",")
        last_i = len(ops) - 1
        for i, op in enumerate(ops):
            dx, dy, dz = _dir_delta(op[0])
            amount = int(op[1:])
            for s in range(amount):
                x += dx
                y += dy
                z += dz
                cb((x, y, z), i == last_i and s == amount - 1)


def part1():
    ys = list[int]()

    def _tree_cb(pos: Pos, leaf: bool):
        _, y, _ = pos
        ys.append(y)

    _traverse_tree(lib.get_input(1), _tree_cb)
    print(f"Part 1: {max(ys)}")


def part2():
    segments = set[Pos]()

    def _tree_cb(pos: Pos, leaf: bool):
        segments.add(pos)

    _traverse_tree(lib.get_input(2), _tree_cb)
    print(f"Part 2: {len(segments)}")


def part3():
    segments = set[Pos]()
    leaves = set[Pos]()

    def _tree_cb(pos: Pos, leaf: bool):
        segments.add(pos)
        if leaf:
            leaves.add(pos)

    _traverse_tree(lib.get_input(3), _tree_cb)

    murkiness = defaultdict[Pos, int](lambda: 0)
    for leaf in leaves:
        q = [(leaf, 0)]
        seen = {leaf}
        while q:
            segment, dist = q.pop(0)
            x, y, z = segment
            if x == 0 and z == 0:
                murkiness[segment] += dist
            for dx, dy, dz in NEIGHBOURS:
                neighbour = (x + dx, y + dy, z + dz)
                if neighbour in segments and neighbour not in seen:
                    seen.add(neighbour)
                    q.append((neighbour, dist + 1))

    print(f"Part 3: {min(murkiness.values())}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
