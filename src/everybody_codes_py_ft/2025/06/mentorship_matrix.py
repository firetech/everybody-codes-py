# pyright: strict

from everybody_codes_py_ft import common as lib


def part1():
    letters = lib.get_input(1)
    novices = (i for i, c in enumerate(letters) if c == "a")
    pairs = 0
    while (i := next(novices, None)) is not None:
        pairs += letters[:i].count("A")
    print(f"Part 1: {pairs}")


def part2():
    letters = lib.get_input(2)
    pairs = 0
    for cat in ("a", "b", "c"):
        novices = (i for i, c in enumerate(letters) if c == cat)
        while (i := next(novices, None)) is not None:
            pairs += letters[:i].count(cat.upper())
    print(f"Part 2: {pairs}")


def part3():
    letters = lib.get_input(3)
    total_len = len(letters) * 1000
    pairs = 0
    for cat in ("a", "b", "c"):
        novices = [1 if c == cat else 0 for c in letters] * 1000
        knights = [1 if c == cat.upper() else 0 for c in letters] * 1000
        for i, k in enumerate(knights):
            if k == 0:
                continue
            left = max(0, i - 1000)
            right = min(i + 1001, total_len)
            pairs += sum(novices[left:right])

    print(f"Part 3: {pairs}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
