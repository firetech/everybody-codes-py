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
    input_len = len(letters)
    repeats = 1000
    # Fix for handling example
    while input_len < 2000:
        # Make sure range doesn't span multiple repeats of the input
        # (simplifies calculation below)
        letters *= 10
        input_len *= 10
        repeats //= 10
    assert repeats >= 2, "We're gonna have a problem here"
    mid_count = repeats - 2
    pairs = 0
    for cat in ("a", "b", "c"):
        novices = [1 if c == cat else 0 for c in letters] * 3
        knights = [1 if c == cat.upper() else 0 for c in letters]
        for i, k in enumerate(knights):
            if k == 0:
                continue
            left = max(0, i - 1000)
            right = min(i + 1001, input_len)
            # Start of arrangement (non-wrapping)
            pairs += sum(novices[left + input_len : i + input_len + 1001])
            # Middle repeats of arrangement (wrapping)
            pairs += (
                sum(novices[i + input_len - 1000 : i + input_len + 1001]) * mid_count
            )
            # End of arrangement (non-wrapping)
            pairs += sum(novices[i + input_len - 1000 : right + input_len])

    print(f"Part 3: {pairs}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
