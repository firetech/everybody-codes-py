# pyright: strict

import functools as ft
import itertools as it
from typing import TypeAlias

from everybody_codes_py_ft import common as lib

Rules: TypeAlias = dict[str, set[str]]


def _parse_input(data: str) -> tuple[list[str], Rules]:
    names_in, rules_in = data.split("\n\n")
    return (
        names_in.split(","),
        {
            rule_in: set(rule_out.split(","))
            for rule_in, rule_out in (
                line.split(" > ") for line in rules_in.splitlines()
            )
        },
    )


def _match_rule(rules: Rules, name: str):
    return all(a not in rules or b in rules[a] for a, b in it.pairwise(name))


def part1():
    names, rules = _parse_input(lib.get_input(1))
    matching = filter(ft.partial(_match_rule, rules), names)
    print(f"Part 1: {",".join(matching)}")


def part2():
    names, rules = _parse_input(lib.get_input(2))
    index_sum = sum(i + 1 for i, name in enumerate(names) if _match_rule(rules, name))
    print(f"Part 2: {index_sum}")


def part3():
    prefixes, rules = _parse_input(lib.get_input(3))
    valid_prefixes = set(filter(ft.partial(_match_rule, rules), prefixes))

    @ft.cache
    def _possible_names(letter: str, length: int):
        count = 1 if length >= 7 else 0
        if length < 11 and letter in rules:
            count += sum(_possible_names(c, length + 1) for c in rules[letter])
        return count

    count = sum(_possible_names(prefix[-1], len(prefix)) for prefix in valid_prefixes)
    # Remove double counted names
    count -= sum(
        _possible_names(b[-1], len(b))
        for a, b in it.permutations(valid_prefixes, 2)
        if b.startswith(a)
    )
    print(f"Part 3: {count}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
