# pyright: strict

from typing import Final

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


PART3_RANGE: Final = 1000
PART3_REPEATS: Final = 1000


def part3():
    letters = lib.get_input(3)
    input_len = len(letters)
    repeats = PART3_REPEATS
    # Fix for handling example
    while input_len < PART3_RANGE * 2 and repeats > 0:
        # Make sure range doesn't span multiple repeats of the input
        # (simplifies calculations below)
        letters *= 10
        input_len *= 10
        repeats //= 10
    assert repeats > 0, "We're gonna have a problem here"
    pairs = 0
    for cat in ("a", "b", "c"):
        novices = [1 if c == cat else 0 for c in letters]
        for i, c in enumerate(letters):
            if c != cat.upper():
                continue
            left_raw = i - PART3_RANGE
            left = max(0, left_raw)
            right_raw = i + PART3_RANGE + 1
            right = min(right_raw, input_len)

            # The non-wrapping parts are simple
            pairs += sum(novices[left:right]) * repeats

            # Add the wrapping parts (excluding beginning and end of the arrangement)
            pairs += sum(novices[input_len - (left - left_raw) :]) * (repeats - 1)
            pairs += sum(novices[: right_raw - right]) * (repeats - 1)

    print(f"Part 3: {pairs}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
