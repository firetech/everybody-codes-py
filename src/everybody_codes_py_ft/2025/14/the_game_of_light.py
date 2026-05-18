# pyright: strict

from typing import Callable, TypeAlias

from everybody_codes_py_ft import common as lib

Grid: TypeAlias = tuple[tuple[bool, ...], ...]
CenterChecker: TypeAlias = Callable[[Grid], bool]


def _input_grid(part: int) -> Grid:
    return tuple(
        tuple(c == "#" for c in line) for line in lib.get_input(part).splitlines()
    )


def _debug(grid: Grid):  # pyright: ignore[reportUnusedFunction]
    print("\n".join("".join("#" if cell else "." for cell in line) for line in grid))
    print()


def _sum_active(grid: Grid, rounds: int, match_input: Grid | None = None):
    width = len(grid[0])
    height = len(grid)

    def _active(current_grid: Grid, x: int, y: int):
        neighbours = sum(
            current_grid[ny][nx]
            for nx, ny in (
                (x - 1, y - 1),
                (x + 1, y - 1),
                (x - 1, y + 1),
                (x + 1, y + 1),
            )
            if 0 <= nx < width and 0 <= ny < height
        )
        return (neighbours & 1) == current_grid[y][x]

    grid_matches_input: CenterChecker

    if match_input is None:
        grid_matches_input = lambda _: True
    else:
        center_width = len(match_input[0])
        center_height = len(match_input)
        start_x = width // 2 - center_width // 2
        end_x = width // 2 + center_width // 2
        start_y = height // 2 - center_height // 2
        end_y = height // 2 + center_height // 2

        grid_matches_input = (
            lambda a_grid: tuple(
                a_grid[y][start_x:end_x] for y in range(start_y, end_y)
            )
            == match_input
        )

    seen = dict[Grid, int]()
    active = dict[int, int]()
    current_grid = grid
    total_active = 0
    for i in range(rounds):
        next_grid = tuple(
            tuple(_active(current_grid, x, y) for x in range(width))
            for y in range(height)
        )
        # _debug(next_grid)
        if grid_matches_input(next_grid):
            total_active += sum(sum(line) for line in next_grid)
        seen_at = seen.get(next_grid)
        if seen_at is None:
            seen[next_grid] = i
            active[i] = total_active
        else:
            cycle_len = i - seen_at
            remaining = rounds - i - 1
            full_cycles, extra_steps = divmod(remaining, cycle_len)
            total_active += full_cycles * (total_active - active[seen_at])
            total_active += active[seen_at + extra_steps] - active[seen_at]
            break
        current_grid = next_grid
    return total_active


def part1():
    print(f"Part 1: {_sum_active(_input_grid(1), 10)}")


def part2():
    # Using example from part 1 (none given), answer should be 39349
    print(f"Part 2: {_sum_active(_input_grid(2), 2025)}")


def part3():
    start_grid: Grid = tuple(tuple(False for _ in range(34)) for _ in range(34))
    print(f"Part 3: {_sum_active(start_grid, 1000000000, _input_grid(3))}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
