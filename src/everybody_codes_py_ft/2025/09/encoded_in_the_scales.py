# pyright: strict

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


def _similarity(a: str, b: str):
    return [ca == cb for ca, cb in zip(a, b)]


def _find_parents(scale_id: int, scales: dict[int, str]):
    sequence = scales[scale_id]
    similarities = {
        other_id: _similarity(sequence, scales[other_id])
        for other_id in scales
        if other_id != scale_id
    }
    similarity_count = {
        other_id: similarity.count(True)
        for other_id, similarity in similarities.items()
    }
    similarity_toplist = sorted(
        similarities,
        key=lambda sim_id: similarity_count[sim_id],
        reverse=True,
    )
    sequence_len = len(sequence)
    for i, parent_a in enumerate(similarity_toplist):
        if (
            similarity_count[parent_a] + similarity_count[similarity_toplist[i + 1]]
            < sequence_len
        ):
            break
        for parent_b in similarity_toplist[i + 1 :]:
            if similarity_count[parent_a] + similarity_count[parent_b] < sequence_len:
                break
            if all(
                sim_a | sim_b
                for sim_a, sim_b in zip(similarities[parent_a], similarities[parent_b])
            ):
                return (parent_a, parent_b)
    return None


def _similarity_score(scale_id: int, parents: tuple[int, int], scales: dict[int, str]):
    return math.prod(
        _similarity(scales[parent], scales[scale_id]).count(True) for parent in parents
    )


def part1():
    scales = _parse_input(1)
    for scale_id in scales:
        parents = _find_parents(scale_id, scales)
        if parents:
            print(f"Part 1: {_similarity_score(scale_id, parents, scales)}")
            break
    else:
        raise Exception("No child found?")


def part2():
    scales = _parse_input(2)
    similarity_sum = 0
    for scale_id in scales:
        parents = _find_parents(scale_id, scales)
        if parents:
            similarity_sum += _similarity_score(scale_id, parents, scales)
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
