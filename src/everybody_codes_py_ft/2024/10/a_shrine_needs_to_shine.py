# pyright: strict

from typing import Final

from everybody_codes_py_ft import common as lib

LEGEND_INDEXES: Final = (0, 1, 6, 7)


def _to_chart(data: str):
    return [list(line) for line in data.splitlines()]


def _solve(chart: list[list[str]], offset: tuple[int, int] = (0, 0)):
    ox, oy = offset
    h_sets = [
        set(c for x in LEGEND_INDEXES if (c := chart[y + 2 + oy][x + ox]) != "?")
        for y in range(4)
    ]
    v_sets = [
        set(c for y in LEGEND_INDEXES if (c := chart[y + oy][x + 2 + ox]) != "?")
        for x in range(4)
    ]
    word = ["?"] * 16
    unsolved = list[tuple[int, int]]()
    for y in range(4):
        for x in range(4):
            candidates = h_sets[y] & v_sets[x]
            if len(candidates) == 1:
                chart[y + 2 + oy][x + 2 + ox] = word[y * 4 + x] = candidates.pop()
            else:
                unsolved.append((x, y))

    solved = True
    for x, y in unsolved:
        candidates = h_sets[y] | v_sets[x]
        this_i = y * 4 + x
        for n in range(4):
            for i in (y * 4 + n, n * 4 + x):
                if i == this_i:
                    continue
                if word[i] == "?":
                    # Other unsolved
                    candidates.clear()
                    break
                elif word[i] in candidates:
                    candidates.remove(word[i])
            if not candidates:
                break
        if len(candidates) == 1:
            c = candidates.pop()
            word[this_i] = c
            for i in LEGEND_INDEXES:
                if chart[oy + i][x + ox + 2] == "?":
                    chart[oy + i][x + ox + 2] = c
                if chart[y + oy + 2][ox + i] == "?":
                    chart[y + oy + 2][ox + i] = c
        else:
            solved = False

    if solved:
        return word
    else:
        return None


def part1():
    print(f"Part 1: {"".join(_solve(_to_chart(lib.get_input(1))) or "???")}")


def _power(word: list[str] | None):
    if word is None:
        return -1
    return sum((i + 1) * (ord(char) - ord("A") + 1) for i, char in enumerate(word))


def part2():
    chart = _to_chart(lib.get_input(2))
    power = sum(
        _power(_solve(chart, (x, y)))
        for y in range(0, len(chart), 9)
        for x in range(0, len(chart[0]), 9)
    )
    print(f"Part 2: {power}")


def part3():
    chart = _to_chart(lib.get_input(3))
    todo = set(
        (x, y)
        for y in range(0, len(chart) - 2, 6)
        for x in range(0, len(chart[0]) - 2, 6)
    )
    last = -1
    words = list[list[str]]()

    def _todo_filter(offset: tuple[int, int]):
        word = _solve(chart, offset)
        if word is None:
            return True
        else:
            words.append(word)

    while len(words) != last and todo:
        last = len(words)
        todo = set[tuple[int, int]](filter(_todo_filter, todo))

    print(f"Part 3: {sum(_power(word) for word in words)}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
