# pyright: strict

import itertools as it
import math
from collections import defaultdict

from everybody_codes_py_ft import common as lib


def _parse_input(part: int):
    return {
        int(scale_id): sequence
        for scale_id, sequence in (
            line.split(":", 1) for line in lib.get_input(part).splitlines()
        )
    }


def _find_parents(scale_id: int, scales: dict[int, str]):
    sequence = scales[scale_id]
    for parent_ids in it.combinations(scales, 2):
        if scale_id in parent_ids:
            continue
        parent_sequences = tuple(scales[parent_id] for parent_id in parent_ids)
        if all(
            any(p[i] == s for p in parent_sequences) for i, s in enumerate(sequence)
        ):
            return parent_ids
    return None


def _similarity(scale_id: int, parents: tuple[int, int], scales: dict[int, str]):
    return math.prod(
        [
            sum(p == s for p, s in zip(scales[parent], scales[scale_id]))
            for parent in parents
        ]
    )


def part1():
    scales = _parse_input(1)
    for scale_id in scales:
        parents = _find_parents(scale_id, scales)
        if parents:
            print(f"Part 1: {_similarity(scale_id, parents, scales)}")
            break
    else:
        raise Exception("No child found?")


def part2():
    scales = _parse_input(2)
    similarity_sum = 0
    for scale_id in scales:
        parents = _find_parents(scale_id, scales)
        if parents:
            similarity_sum += _similarity(scale_id, parents, scales)
    print(f"Part 2: {similarity_sum}")


def part3():
    scales = _parse_input(3)
    parents_of = dict[int, tuple[int, int]]()
    for scale_id in scales:
        parents = _find_parents(scale_id, scales)
        if parents:
            parents_of[scale_id] = parents

    families = defaultdict[int, set[int]](set)
    family_of = dict[int, int]()
    next_id = 1
    for scale_id in scales:
        family_id = family_of.get(scale_id)
        if not family_id:
            family_id = next_id
            family_of[scale_id] = family_id
            families[family_id].add(scale_id)
            next_id += 1
        for parent_id in parents_of.get(scale_id, ()):
            parent_family = family_of.get(parent_id)
            if parent_family:
                sub_family = families.pop(family_id)
                families[parent_family].update(sub_family)
                for member in sub_family:
                    family_of[member] = parent_family
                family_id = parent_family
            else:
                family_of[parent_id] = family_id
                families[family_id].add(parent_id)

    largest_family = max(families.values(), key=lambda f: len(f))

    print(f"Part 3: {sum(largest_family)}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
