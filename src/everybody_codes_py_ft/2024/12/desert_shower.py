# pyright: strict

from typing import Final

from everybody_codes_py_ft import common as lib

UNSET_BASE: Final = (-1, -1)


def _total_power(data: str):
    base = UNSET_BASE
    targets = list[tuple[int, int, int]]()
    for y, line in enumerate(reversed(data.splitlines())):
        for x, c in enumerate(line):
            match c:
                case "A":
                    assert base == UNSET_BASE, "Multiple catapults?"
                    base = (x, y)
                case "B" | "C":
                    level = ord(c) - ord("A")
                    assert base == (x, y - level), "Mismatched upper catapult"
                case "T":
                    targets.append((x, y, 1))
                case "H":
                    targets.append((x, y, 2))
                case ".":
                    pass
                case "=":
                    assert y == 0, "Ground not at 0"
                case x:
                    raise Exception(f"Unknown character '{x}'")

    bx, by = base
    return sum(
        (delta := (x - bx) + (y - by)) // 3 * ((delta % 3) + 1) * count
        for x, y, count in targets
    )


def part1():
    print(f"Part 1: {_total_power(lib.get_input(1))}")


def part2():
    print(f"Part 2: {_total_power(lib.get_input(2))}")


def _shoot_meteor(x: int, y: int):
    hit_x = x // 2
    hit_y = y - hit_x - x % 2
    for level in range(3):
        rel_y = hit_y - level
        if hit_x < rel_y:
            continue
        if hit_x <= 2 * rel_y:
            return rel_y * (level + 1)
        else:
            delta = rel_y + hit_x
            if delta % 3 == 0:
                return delta // 3 * (level + 1)
    return float("inf")


def part3():
    total = sum(
        _shoot_meteor(*(int(s) for s in line.split(" ")))
        for line in lib.get_input(3).splitlines()
    )
    print(f"Part 3: {total}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
