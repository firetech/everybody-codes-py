# pyright: strict

import dataclasses as dc

from everybody_codes_py_ft import common as lib


@dc.dataclass(kw_only=True)
class Machine:
    max_x: int
    max_y: int
    slots: int
    nails: set[tuple[int, int]]


def _parse_input(data: str) -> tuple[Machine, list[str]]:
    chart_in, tokens_in = data.split("\n\n")
    chart_lines = chart_in.splitlines()
    max_x = len(chart_lines[0]) - 1
    machine = Machine(
        max_x=max_x,
        max_y=len(chart_lines) - 1,
        slots=max_x // 2 + 1,
        nails={
            (x, y)
            for y, line in enumerate(chart_lines)
            for x, c in enumerate(line)
            if c == "*"
        },
    )
    return machine, tokens_in.splitlines()


def _play(toss_slot: int, path: str, machine: Machine):
    x = (toss_slot - 1) * 2
    y = 0
    path_iter = iter(path)
    while y <= machine.max_y:
        if (x, y) in machine.nails:
            match next(path_iter):
                case "L":
                    if x > 0:
                        x -= 1
                    else:
                        x += 1
                case "R":
                    if x < machine.max_x:
                        x += 1
                    else:
                        x -= 1
                case other:
                    raise Exception(f"Unknown direction '{other}'")
        y += 1
    final_slot = x // 2 + 1
    coins = max(final_slot * 2 - toss_slot, 0)
    return coins


def part1():
    machine, tokens = _parse_input(lib.get_input(1))

    total = sum(_play(n + 1, path, machine) for n, path in enumerate(tokens))

    print(f"Part 1: {total}")


def part2():
    machine, tokens = _parse_input(lib.get_input(2))

    total = sum(
        max(_play(n + 1, path, machine) for n in range(machine.slots))
        for path in tokens
    )

    print(f"Part 2: {total}")


def part3():
    machine, tokens = _parse_input(lib.get_input(3))

    results = [
        [_play(n + 1, path, machine) for n in range(machine.slots)] for path in tokens
    ]
    dp_min = [0] + [1 << 31] * ((1 << machine.slots) - 1)
    dp_max = [0] * (1 << machine.slots)
    active_masks = {0}
    for t in range(len(tokens)):
        next_masks = set[int]()
        for s in range(machine.slots):
            for mask in active_masks:
                smask = mask | (1 << s)
                if smask == mask:
                    # Slot already used in this mask
                    continue
                dp_min[smask] = min(dp_min[smask], dp_min[mask] + results[t][s])
                dp_max[smask] = max(dp_max[smask], dp_max[mask] + results[t][s])
                next_masks.add(smask)
        active_masks = next_masks

    min_coins = min(dp_min[mask] for mask in active_masks)
    max_coins = max(dp_max[mask] for mask in active_masks)

    print(f"Part 3: {min_coins} {max_coins}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
