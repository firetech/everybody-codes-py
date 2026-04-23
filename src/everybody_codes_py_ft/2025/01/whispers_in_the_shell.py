# pyright: strict

from everybody_codes_py_ft import common as lib


def _parse_input(data: str):
    names_in, ops_in = data.split("\n\n", 1)
    return (
        names_in.split(","),
        [int(op[1:]) * (-1 if op[0] == "L" else 1) for op in ops_in.split(",")],
    )


def part1():
    names, ops = _parse_input(lib.get_input(1))
    i = 0
    for diff in ops:
        i += diff
        if i < 0:
            i = 0
        if i >= len(names):
            i = len(names) - 1
    print(f"Part 1: {names[i]}")


def part2():
    names, ops = _parse_input(lib.get_input(2))
    i = 0
    for diff in ops:
        i = (i + diff) % len(names)
    print(f"Part 2: {names[i]}")


def part3():
    names, ops = _parse_input(lib.get_input(3))
    for op in ops:
        i = op % len(names)
        names[0], names[i] = names[i], names[0]
    print(f"Part 3: {names[0]}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
