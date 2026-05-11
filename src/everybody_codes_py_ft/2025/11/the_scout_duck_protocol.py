# pyright: strict

from everybody_codes_py_ft import common as lib


def _parse_input(part: int):
    return [int(x) for x in lib.get_input(part).splitlines()]


def _rearrange(columns: list[int], max_rounds: int = -1):
    column_count = len(columns)

    rounds = 0

    # Phase 1
    moved = True  # To enter loop first time
    while moved and (max_rounds < 0 or rounds < max_rounds):
        moved = False
        for i in range(column_count - 1):
            if columns[i + 1] < columns[i]:
                columns[i] -= 1
                columns[i + 1] += 1
                moved = True
        rounds += 1 if moved else 0

    if max_rounds < 0:
        # Number of rounds for phase 2 is easily calculated after phase 1
        avg = sum(columns) // column_count
        rounds_left = sum(avg - c for c in columns if avg > c)
        for i in range(column_count):
            columns[i] = avg
        return rounds + rounds_left

    else:
        # Phase 2
        moved = True  # To enter loop first time
        while moved and rounds < max_rounds:
            moved = False
            for i in range(column_count - 1):
                if columns[i + 1] > columns[i]:
                    columns[i + 1] -= 1
                    columns[i] += 1
                    moved = True
            rounds += 1 if moved else 0

    return rounds


def part1():
    columns = _parse_input(1)

    rounds = _rearrange(columns, 10)
    assert rounds == 10

    print(f"Part 1: {sum((i+1) * c for i, c in enumerate(columns))}")


def part2():
    columns = _parse_input(2)

    rounds = _rearrange(columns)
    print(f"Part 2: {rounds}")


def part3():
    columns = _parse_input(3)

    rounds = _rearrange(columns)
    print(f"Part 3: {rounds}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
