# pyright: strict

import functools as ft
import itertools as it
from typing import TypeAlias

from everybody_codes_py_ft import common as lib

Rules: TypeAlias = dict[str, set[str]]


def _parse_input(data: str):
    names_in, rules_in = data.split("\n\n")
    names = names_in.split(",")
    rules = Rules()
    for line in rules_in.splitlines():
        rule_in, rule_out = line.split(" > ")
        rules[rule_in] = set(rule_out.split(","))
    return names, rules


def _match_rule(rules: Rules, name: str):
    for a, b in it.pairwise(name):
        if a not in rules:
            continue
        if b not in rules[a]:
            break
    else:
        return True


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

    @ft.cache
    def _possible_suffixes(letter: str, length: int):
        suffixes = set[str]()
        if length >= 7:
            suffixes.add(letter)
        if length < 11 and letter in rules:
            suffixes.update(
                letter + s
                for c in rules[letter]
                for s in _possible_suffixes(c, length + 1)
            )
        return suffixes

    names = set[str]()
    for prefix in prefixes:
        if not _match_rule(rules, prefix):
            continue
        names.update(
            prefix[:-1] + suffix
            for suffix in _possible_suffixes(prefix[-1], len(prefix))
        )
    print(f"Part 3: {len(names)}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
