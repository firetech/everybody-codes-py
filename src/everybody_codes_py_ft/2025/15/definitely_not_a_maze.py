# pyright: strict

from typing import Final, TypeAlias

from everybody_codes_py_ft import common as lib

DIRS: Final = ((0, -1), (1, 0), (0, 1), (-1, 0))

Pos: TypeAlias = tuple[int, int]
Chart: TypeAlias = set[Pos]
CompressionMap: TypeAlias = list[int]


def _parse_input(part: int) -> tuple[Pos, Pos, Chart, CompressionMap, CompressionMap]:
    current_dir = 0
    x, y = 0, 0
    walls = list[tuple[Pos, Pos]]()
    xs, ys = {-1, 0, 1}, {-1, 0, 1}
    for op in lib.get_input(part).split(","):
        match op[0]:
            case "R":
                current_dir += 1
            case "L":
                current_dir -= 1
            case other:
                raise Exception(f"Unknown direction '{other}'")
        current_dir %= len(DIRS)
        dx, dy = DIRS[current_dir]
        amount = int(op[1:])
        nx, ny = x + dx * amount, y + dy * amount
        walls.append(((x, y), (nx, ny)))
        # Add possible corner positions to list of useful values.
        xs.update((nx - 1, nx, nx + 1))
        ys.update((ny - 1, ny, ny + 1))
        x, y = nx, ny
    end_x, end_y = x, y

    # Compress map, removing all intermediate x and y values (between wall corners).
    sorted_xs = sorted(xs)  # Mapping from compressed X to real X
    x_map = {v: i for i, v in enumerate(sorted_xs)}  # Mapping from real X to comp. X
    sorted_ys = sorted(ys)  # Mapping from compressed Y to real Y
    y_map = {v: i for i, v in enumerate(sorted_ys)}  # Mapping from real Y to comp. Y
    chart = Chart()
    # Build the compressed wall chart.
    for (ax, ay), (bx, by) in walls:
        min_x, max_x = sorted((x_map[ax], x_map[bx]))
        min_y, max_y = sorted((y_map[ay], y_map[by]))
        for cx in range(min_x, max_x + 1):
            for cy in range(min_y, max_y + 1):
                chart.add((cx, cy))

    # Map start and end positions.
    start = (x_map[0], y_map[0])
    end = (x_map[end_x], y_map[end_y])
    chart.remove(end)  # This simplifies the traversal code

    return (
        start,
        end,
        chart,
        sorted_xs,
        sorted_ys,
    )


MAX_COST: Final = 0xFFFFFFFF


def _traverse(part: int):
    start, end, chart, real_x, real_y = _parse_input(part)
    max_x = len(real_x)
    max_y = len(real_y)
    q: list[tuple[int, Pos]] = [(0, start)]
    seen: set[Pos] = {start}
    while q:
        steps, pos = q.pop(0)

        if pos == end:
            return steps

        x, y = pos
        for dx, dy in DIRS:
            nx = x + dx
            if nx < 0 or nx >= max_x:
                continue
            ny = y + dy
            if ny < 0 or ny >= max_y:
                continue
            npos = (nx, ny)
            if npos in seen or npos in chart:
                continue
            seen.add(npos)
            # Calculate actual distance moved in the non-compressed map
            nsteps = steps + abs(real_x[x] - real_x[nx]) + abs(real_y[y] - real_y[ny])
            q.append((nsteps, npos))

    raise Exception("Unable to find exit")


def part1():
    print(f"Part 1: {_traverse(1)}")


def part2():
    # Uses the same example as part 1 (none given)
    print(f"Part 2: {_traverse(2)}")


def part3():
    # Uses the same example as part 1 (none given)
    print(f"Part 3: {_traverse(3)}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
