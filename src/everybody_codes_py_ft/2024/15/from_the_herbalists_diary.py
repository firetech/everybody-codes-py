# pyright: strict

from typing import Final, TypeAlias

from everybody_codes_py_ft import common as lib

A: Final = ord("A")
Z: Final = ord("Z")

Pos: TypeAlias = tuple[int, int]


def _char_mask(char: str):
    if char == ".":
        return 0
    else:
        co = ord(char)
        if co >= A and co <= Z:
            return 1 << co - A
    return None


def _parse_map(data: str):
    chart = {
        (x, y): mask
        for y, line in enumerate(data.splitlines())
        for x, c in enumerate(line)
        if (mask := _char_mask(c)) is not None
    }
    starts = [(x, y) for (x, y), mask in chart.items() if mask == 0 and y == 0]
    assert len(starts) == 1, "Not exactly one starting position"
    return chart, starts[0]


DIRS: Final = ((-1, 0), (1, 0), (0, -1), (0, 1))


def _traverse(chart: dict[Pos, int], visited: set[Pos], base: Pos) -> tuple[int, int]:
    # Spit map where a herb blocks the way
    split_queue = [base]
    herb_pos = list[Pos]()
    while split_queue:
        pos = split_queue.pop(0)
        x, y = pos
        for dx, dy in DIRS:
            npos = (x + dx, y + dy)
            if npos in chart and not npos in visited:
                visited.add(npos)
                if chart[npos]:
                    herb_pos.append(npos)
                else:
                    split_queue.append(npos)

    # Process submaps and select herbs to pick
    total_steps = 0
    herbs_to_find = 0
    for herb in herb_pos:
        sub_total, sub_herbs = _traverse(chart, visited, herb)
        total_steps += sub_total
        herbs_to_find |= sub_herbs & ~chart[base]

    # Finally, process own map
    step_queue = [(base, herbs_to_find, 0)]
    seen_states = {(base, herbs_to_find)}
    while step_queue:
        pos, remaining, steps = step_queue.pop(0)
        if pos == base and remaining == 0:
            total_steps += steps
            break

        x, y = pos
        for dx, dy in DIRS:
            npos = (x + dx, y + dy)
            if npos in chart:
                nrem = remaining & ~chart[npos]
                seen_key = (npos, nrem)
                if not seen_key in seen_states:
                    seen_states.add(seen_key)
                    step_queue.append((npos, nrem, steps + 1))

    chart[base] |= herbs_to_find

    return total_steps, chart[base]


def part1():
    chart, start = _parse_map(lib.get_input(1))
    steps, _ = _traverse(chart, {start}, start)
    print(f"Part 1: {steps}")


def part2():
    chart, start = _parse_map(lib.get_input(2))
    steps, _ = _traverse(chart, {start}, start)
    print(f"Part 2: {steps}")


def part3():
    chart, start = _parse_map(lib.get_input(3))
    steps, _ = _traverse(chart, {start}, start)
    print(f"Part 3: {steps}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
