# pyright: strict

from collections import defaultdict

from everybody_codes_py_ft import common as lib


def _parse_rules(data: str):
    return {
        (split := line.split(":", 1))[0]: split[1].split(",")
        for line in data.splitlines()
    }


def _grow(rules: dict[str, list[str]], start: str, days: int):
    pop = {start: 1}
    for _ in range(days):
        new_pop = defaultdict[str, int](lambda: 0)
        for cat, count in pop.items():
            for new_cat in rules[cat]:
                new_pop[new_cat] += count
        pop = new_pop
    return sum(pop.values())


def part1():
    rules = _parse_rules(lib.get_input(1))
    print(f"Part 1: {_grow(rules, "A", 4)}")


def part2():
    rules = _parse_rules(lib.get_input(2))
    print(f"Part 2: {_grow(rules, "Z", 10)}")


def part3():
    rules = _parse_rules(lib.get_input(3))
    counts = {cat: _grow(rules, cat, 20) for cat in rules.keys()}
    print(f"Part 3: {max(counts.values()) - min(counts.values())}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
