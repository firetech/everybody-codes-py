# pyright: strict

from typing import Callable, Final, TypeAlias

from everybody_codes_py_ft import common as lib

Pos: TypeAlias = tuple[int, int]
Chart: TypeAlias = dict[Pos, int]
POIs: TypeAlias = dict[str, Pos]

A: Final = ord("A")
Z: Final = ord("Z")


def _parse_input(data: str) -> tuple[Chart, POIs, int, int]:
    chart = Chart()
    pois = POIs()
    lines = data.splitlines()
    height = len(lines)
    width = len(lines[0])
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            pos = (x, y)
            match c:
                case ".":
                    chart[pos] = -1
                case "-":
                    chart[pos] = -2
                case "+":
                    chart[pos] = 1
                case _:
                    oc = ord(c)
                    if oc >= A and oc <= Z:
                        assert c not in pois, f"Duplicate POI '{c}'"
                        chart[pos] = -1
                        pois[c] = pos
    return chart, pois, width, height


MOVE: Final = ((0, 1), (0, -1), (1, 0), (-1, 0))
TURN: Final = (
    (0, 2, 3),
    (1, 2, 3),
    (2, 0, 1),
    (3, 0, 1),
)
UNSET_ALT: Final = -0x80000000  # minimum 32-bit int

SeenMap: TypeAlias = dict[tuple[Pos, int], int]


def part1():
    chart, pois, *_ = _parse_input(lib.get_input(1))
    seen = SeenMap()
    max_end = 0
    q = [(pois["S"], 0, 1000, 0)]
    while q:
        pos, time, altitude, direction = q.pop(0)
        if time == 100:
            max_end = max(max_end, altitude)
            continue
        x, y = pos
        for ndir in TURN[direction]:
            dx, dy = MOVE[ndir]
            npos = (x + dx, y + dy)
            if npos not in chart:
                continue
            nalt = altitude + chart[npos]
            seen_key = (npos, ndir)
            if seen.get(seen_key, float("-inf")) >= nalt:
                continue
            seen[seen_key] = nalt
            q.append((npos, time + 1, nalt, ndir))

    print(f"Part 1: {max_end}")


Part2States: TypeAlias = dict[tuple[Pos, int, int], int]


def part2():
    chart, pois, *_ = _parse_input(lib.get_input(2))
    targets = [pois[t] for t in "ABCS"]

    start = pois["S"]
    states: Part2States = {(start, 0, 0): 10000}
    time = 0
    total = 0
    while total == 0 and states:
        nstates = Part2States()

        for (pos, target, dir), altitude in states.items():
            ntarget = target
            if pos == targets[target]:
                if target == 3:
                    if altitude >= 10000:
                        total = time
                        break
                    continue
                ntarget += 1
            x, y = pos
            for ndir in TURN[dir]:
                dx, dy = MOVE[ndir]
                npos = (x + dx, y + dy)
                if npos not in chart:
                    continue
                nalt = altitude + chart[npos]
                state_key = (npos, ntarget, ndir)
                if nstates.get(state_key, float("-inf")) >= nalt:
                    continue
                nstates[state_key] = nalt
        states = nstates
        time += 1

    print(f"Part 2: {total}")


def part3():
    chart, pois, width, height = _parse_input(lib.get_input(3))
    start_x, start_y = pois["S"]
    assert start_y == 0, "Start not at top?"

    def _traverse(start_pos: Pos, start_alt: int, cb: Callable[[Pos, int], bool]):
        q = [(start_pos, start_alt, 0)]
        seen = SeenMap()
        while q:
            pos, altitude, direction = q.pop(0)
            if cb(pos, altitude):
                continue

            x, y = pos
            for ndir in TURN[direction]:
                dx, dy = MOVE[ndir]
                nx = x + dx
                ny = y + dy
                if ny < 0:
                    continue
                npos = (nx, ny)
                chart_pos = (nx, ny % height)
                if chart_pos not in chart:
                    continue
                nalt = altitude + chart[chart_pos]
                seen_key = (npos, ndir)
                if seen.get(seen_key, UNSET_ALT) >= nalt:
                    continue
                seen[seen_key] = nalt
                q.append((npos, nalt, ndir))

    # Find optimal paths from the top position of each column to every column it can reach.
    best = [[UNSET_ALT for _ in range(width)] for _ in range(width)]
    precalc_height = height * 2
    for x in range(width):
        start_pos = (x, 0)
        if start_pos not in chart:
            continue
        this_best = best[x]

        def _opt_path_cb(pos: Pos, altitude: int):
            px, py = pos
            if py == precalc_height:
                this_best[px] = max(this_best[px], altitude)
                return True
            return False

        _traverse((x, 0), 0, _opt_path_cb)

    # Fly through complete map in optimal paths until all results have landed.
    current = {start_x: 384400}
    in_air = True
    y = 0
    while in_air:
        next_alts = dict[int, int]()
        in_air = False
        max_alt = max(current.values())
        for from_x, from_alt in current.items():
            if from_alt < max_alt:  # Keep only the top altitudes.
                continue
            for to_x, diff in enumerate(best[from_x]):
                nalt = from_alt + diff
                if nalt <= 0:
                    continue
                in_air = True
                next_alts[to_x] = max(
                    nalt,
                    next_alts[to_x] if to_x in next_alts else UNSET_ALT,
                )
        if in_air:
            current = next_alts
            y += precalc_height

    # Find the best possible positions from the remaining altitudes.
    best_y = [y]
    max_alt = max(current.values())
    for x, altitude in current.items():
        if altitude < max_alt:  # Keep only the top altitudes.
            continue

        def _opt_pos_cb(pos: Pos, altitude: int):
            _, py = pos
            if altitude == 0:
                best_y[0] = max(best_y[0], py)
                return True
            return False

        _traverse((x, y), altitude, _opt_pos_cb)

    print(f"Part 3: {best_y[0]}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
