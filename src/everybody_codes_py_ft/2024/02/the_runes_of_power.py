# pyright: strict

import itertools as it

from everybody_codes_py_ft import common as lib


def part1():
    words_txt, text = lib.get_input(1).split("\n\n", 1)
    words = words_txt[6:].split(",")
    matches = 0
    for word in words:
        matches += text.count(word)
    print(f"Part 1: {matches}")


def part2():
    words_txt, text = lib.get_input(2).split("\n\n", 1)
    words = words_txt[6:].split(",")
    symbols = set[int]()
    for word in set(it.chain(words, (w[::-1] for w in words))):
        i = -1
        while (i := text.find(word, i + 1)) >= 0:
            for w in range(len(word)):
                symbols.add(i + w)
    print(f"Part 2: {len(symbols)}")


def part3():
    words_txt, rows_txt = lib.get_input(3).split("\n\n", 1)
    words = words_txt[6:].split(",")
    rows = rows_txt.splitlines()
    cols = list(map("".join, zip(*rows)))
    grid = [[False] * len(row) for row in rows]
    for word in set(it.chain(words, (w[::-1] for w in words))):
        l = len(word)
        for y, row in enumerate(rows):
            x = -1
            l = len(word)
            while (x := row.find(word[0], x + 1)) >= 0:
                if (row * 2)[x : x + l] == word:
                    for i in range(l):
                        grid[y][(x + i) % len(row)] = True
        for x, col in enumerate(cols):
            y = -1
            while (y := col.find(word[0], y + 1)) >= 0:
                if col[y : y + l] == word:
                    for i in range(l):
                        grid[y + i][x] = True
    print(f"Part 3: {sum(row.count(True) for row in grid)}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
