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
    valid_prefixes = set(filter(ft.partial(_match_rule, rules), prefixes))

    @ft.cache
    def _possible_names(letter: str, length: int):
        count = 1 if length >= 7 else 0
        if length < 11 and letter in rules:
            count += sum(_possible_names(c, length + 1) for c in rules[letter])
        return count

    count = 0
    for prefix in valid_prefixes:
        count += _possible_names(prefix[-1], len(prefix))
        for other in valid_prefixes:
            if prefix != other and other.startswith(prefix):
                count -= _possible_names(other[-1], len(other))
    print(f"Part 3: {count}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
