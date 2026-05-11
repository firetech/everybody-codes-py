# pyright: strict

import itertools as it

from everybody_codes_py_ft import common as lib


def _parse_input(part: int):
    return [int(x) for x in lib.get_input(part).splitlines()]


def part1():
    columns = _parse_input(1)
    column_count = len(columns)
    rounds = 0

    # Phase 1
    moved = True  # To enter loop first time
    while moved and rounds < 10:
        moved = False
        for i in range(column_count - 1):
            if columns[i + 1] < columns[i]:
                columns[i] -= 1
                columns[i + 1] += 1
                moved = True
        rounds += 1 if moved else 0
    # Phase 2
    moved = True  # To enter loop first time
    while moved and rounds < 10:
        moved = False
        for i in range(column_count - 1):
            if columns[i + 1] > columns[i]:
                columns[i + 1] -= 1
                columns[i] += 1
                moved = True
        rounds += 1 if moved else 0

    assert rounds == 10

    print(f"Part 1: {sum((i+1) * c for i, c in enumerate(columns))}")


def _count_rounds(columns: list[int]):
    column_count = len(columns)
    rounds = 0

    # Phase 1 is only needed if columns are not in increasing order already
    if any(a > b for a, b in it.pairwise(columns)):
        segments = list[tuple[int, int]]()
        start = 0
        while start < column_count:
            end = start
            # Group with all following columns of decreasing value, creating a segment
            # of columns of equal value.
            segment_sum = columns[start]
            while end < column_count - 1 and columns[end + 1] <= columns[end]:
                end += 1
                segment_sum += columns[end]
            segment_len = end - start + 1
            while segments and segment_sum // segment_len <= segments[-1][0]:
                # Still decreasing, merge with previous segment
                prev_val, prev_count = segments.pop()
                segment_sum += prev_val * prev_count
                segment_len += prev_count
            # Add new segment(s) to list
            segment_val, remainder = divmod(segment_sum, segment_len)
            count = segment_len - remainder
            segments.append((segment_val, count))
            if remainder > 0:
                # Can't be split evenly.
                # Remainder ends up split between the rightmost columns of the segment.
                segments.append((segment_val + 1, remainder))
            start = end + 1

        assert sum(count for _, count in segments) == column_count
        after_phase1 = list(it.chain(*([val] * count for val, count in segments)))

        # Calculate rounds needed for phase 1
        last_diff = 0
        for i in range(column_count):
            diff = columns[i] - after_phase1[i] + last_diff
            rounds = max(rounds, diff)
            last_diff = diff

        columns = after_phase1

    # Calculate rounds needed for phase 2 (all that's needed for part 3)
    avg = sum(columns) // column_count
    rounds += sum(avg - c for c in columns if avg > c)

    return rounds


def part2():
    columns = _parse_input(2)

    rounds = _count_rounds(columns)
    print(f"Part 2: {rounds}")


def part3():
    # Custom example (none given), based on part 2 example. Answer should be 718.
    columns = _parse_input(3)

    rounds = _count_rounds(columns)
    print(f"Part 3: {rounds}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
