# pyright: strict

import re
from typing import Callable, Final, TypeAlias, TypedDict, cast

from everybody_codes_py_ft import common as lib


class Plant(TypedDict):
    id: int
    thickness: int
    branches: list[tuple[int, int]] | None


def _parse_plants(data: str):
    return [_parse_plant(plant) for plant in data.split("\n\n")]


def _parse_plant(data: str) -> Plant:
    plant_def, *branche_input = data.splitlines()
    m = re.match(r"^Plant (\d+) with thickness (-?\d+):$", plant_def)
    if not m:
        raise Exception(f"Malformed plant definition: '{plant_def}'")

    branches = [_parse_branch(line) for line in branche_input]
    if any(branch is None for branch in branches):
        if len(branches) > 1:
            raise Exception("Free branches should be exclusive!")
        branches = None
    else:
        branches = cast(list[tuple[int, int]], branches)

    return {
        "id": int(m[1]),
        "thickness": int(m[2]),
        "branches": branches,
    }


def _parse_branch(line: str):
    m = re.match(r"^- free branch with thickness 1$", line)
    if m:
        return None
    m = re.match(r"^- branch to Plant (\d+) with thickness (-?\d+)$", line)
    if m:
        return (int(m[1]), int(m[2]))
    raise Exception(f"Malformed branch: '{line}'")


BranchEnabled: TypeAlias = Callable[[int], bool]
ALL_ENABLED: Final[BranchEnabled] = lambda _: True


def _calc_energy(plants: list[Plant], branch_enabled: BranchEnabled = ALL_ENABLED):
    energy = dict[int, int]()
    for plant in plants:
        if plant["branches"] is None:
            incoming = 1 if branch_enabled(plant["id"]) else 0
        else:
            incoming = sum(
                energy[dest] * thickness for dest, thickness in plant["branches"]
            )
        energy[plant["id"]] = incoming if incoming >= plant["thickness"] else 0
    return energy[plants[-1]["id"]]


def part1():
    plants = _parse_plants(lib.get_input(1))
    print(f"Part 1: {_calc_energy(plants)}")


def part2():
    plant_input, test_cases = lib.get_input(2).split("\n\n\n")
    plants = _parse_plants(plant_input)
    total_out = 0
    for test_case in test_cases.splitlines():
        branch_enabled = [s == "1" for s in test_case.split(" ")]
        total_out += _calc_energy(plants, lambda i: branch_enabled[i - 1])
    print(f"Part 2: {total_out}")


def part3():
    plant_input, test_cases = lib.get_input(3).split("\n\n\n")
    plants = _parse_plants(plant_input)

    # This doesn't work for the example, but works for the real input.
    good = set[int]()
    bad = set[int]()
    for plant in plants:
        if plant["branches"] is None:
            continue
        for dest, thickness in plant["branches"]:
            if thickness > 0:
                good.add(dest)
                assert dest not in bad
            else:
                bad.add(dest)
                assert dest not in good

    best = _calc_energy(plants, lambda i: i in good)

    total_diff = 0
    for test_case in test_cases.splitlines():
        branch_enabled = [s == "1" for s in test_case.split(" ")]
        result = _calc_energy(plants, lambda i: branch_enabled[i - 1])
        if result:
            total_diff += best - result
    print(f"Part 3: {total_diff}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
