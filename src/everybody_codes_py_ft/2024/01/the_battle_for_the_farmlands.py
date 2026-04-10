# pyright: strict

import itertools as it

from everybody_codes_py_ft import common as lib


def _get_potions(enemy: str):
    match enemy:
        case "A":
            return 0
        case "B":
            return 1
        case "C":
            return 3
        case "D":
            return 5
        case "x":
            return None
        case _:
            raise Exception(f"Unknown enemy '{enemy}'")


def part1():
    data = lib.get_input(1)
    potions = 0
    for enemy in data:
        potions += _get_potions(enemy) or 0
    print(f"Part 1: {potions}")


def part2():
    data = lib.get_input(2)
    potions = 0
    for pair in it.batched(data, 2):
        full_pair = True
        for enemy in pair:
            enemy_potions = _get_potions(enemy)
            if enemy_potions is None:
                full_pair = False
            else:
                potions += enemy_potions
        if full_pair:
            potions += 2
    print(f"Part 2: {potions}")


def part3():
    data = lib.get_input(3)
    potions = 0
    for group in it.batched(data, 3):
        group_size = 0
        for enemy in group:
            enemy_potions = _get_potions(enemy)
            if enemy_potions is not None:
                group_size += 1
                potions += enemy_potions
        potions += group_size * group_size - group_size
    print(f"Part 3: {potions}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
