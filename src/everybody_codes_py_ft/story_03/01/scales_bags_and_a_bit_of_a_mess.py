# pyright: strict

from collections import defaultdict

from everybody_codes_py_ft import common as lib


def _parse_color(color: str) -> int:
    val = 0
    for c in color:
        val <<= 1
        if c.isupper():
            val |= 1
    return val


def _parse_input(part: int):
    return {
        int(scale_id): tuple(_parse_color(color) for color in colors.split(" "))
        for scale_id, colors in (
            line.split(":") for line in lib.get_input(part).splitlines()
        )
    }


def part1():
    scales = _parse_input(1)
    green_scales = {
        scale_id
        for scale_id, (red, green, blue) in scales.items()
        if green > red and green > blue
    }
    print(f"Part 1: {sum(green_scales)}")


def part2():
    scales = _parse_input(2)
    max_shine = max(shine for (_, _, _, shine) in scales.values())
    max_shine_scales = {
        scale_id for scale_id, (_, _, _, shine) in scales.items() if shine == max_shine
    }
    darkest_scale = min(
        max_shine_scales, key=lambda scale_id: sum(scales[scale_id][0:3])
    )
    print(f"Part 2: {darkest_scale}")


def _classify_scale(red: int, green: int, blue: int, shine: int) -> str | None:
    suffix = ""
    if shine <= 30:
        suffix = "matte"
    elif shine >= 33:
        suffix = "shiny"
    else:
        return None
    prefix = ""
    if red > green and red > blue:
        prefix = "red"
    elif green > red and green > blue:
        prefix = "green"
    elif blue > red and blue > green:
        prefix = "blue"
    else:
        return None
    return prefix + suffix


def part3():
    scales = _parse_input(3)
    groups = defaultdict[str, set[int]](set)
    for scale_id, color in scales.items():
        group = _classify_scale(*color)
        if group is not None:
            groups[group].add(scale_id)
    largest_group = max(groups, key=lambda group: len(groups[group]))
    print(f"Part 3: {sum(groups[largest_group])}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
