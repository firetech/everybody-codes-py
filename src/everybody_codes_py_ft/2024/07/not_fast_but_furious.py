# pyright: strict

import itertools as it
import math
from typing import Iterable, Sequence

from everybody_codes_py_ft import common as lib

# For parts 2 and 3, the track is manually appended to the input file


def _parse_player(player_in: str):
    name, ops = player_in.split(":", 1)
    return name, ops.split(",")


def _parse_track(track_in: str):
    map = track_in.splitlines()
    height = len(map)
    x, y = 1, 0
    last = (0, 0)
    track = [map[y][x]]
    while x != 0 or y != 0:
        for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            ny = y + dy
            if ny < 0 or ny >= height:
                continue
            row = map[ny]
            nx = x + dx
            if nx < 0 or nx >= len(row) or (nx, ny) == last:
                continue
            terrain = row[nx]
            if terrain == " ":
                continue
            track.append(terrain)
            last = (x, y)
            x, y = nx, ny
            break
    return track


def _score(strategy: Sequence[str], track: Sequence[str], loops: int = 10):
    ops = zip(it.cycle(strategy), it.cycle(track))
    power = 10
    essence = 0
    for _ in range(loops * len(track)):
        strat_op, terrain_op = next(ops)
        match (strat_op if terrain_op in ("=", "S") else terrain_op):
            case "+":
                power += 1
            case "-":
                if power > 0:
                    power -= 1
            case _:
                pass
        essence += power
    return essence


def _race(players_in: str, track: Sequence[str]):
    scores = dict[str, int]()
    for line in players_in.splitlines():
        name, ops = _parse_player(line)
        scores[name] = _score(ops, track)
    ranking = sorted(scores.keys(), key=lambda n: scores[n], reverse=True)
    return "".join(ranking)


def part1():
    print(f"Part 1: {_race(lib.get_input(1), ["S"])}")


def part2():
    knights, track = lib.get_input(2).split("\n\n")
    print(f"Part 2: {_race(knights, _parse_track(track))}")


def _strat_generator(
    plus: int,
    minus: int,
    equal: int,
    strat: Sequence[str] | None = None,
) -> Iterable[Sequence[str]]:
    if strat is None:
        strat = ()

    if plus == 0 and minus == 0 and equal == 0:
        yield strat
        return

    if plus > 0:
        yield from _strat_generator(plus - 1, minus, equal, (*strat, "+"))
    if minus > 0:
        yield from _strat_generator(plus, minus - 1, equal, (*strat, "-"))
    if equal > 0:
        yield from _strat_generator(plus, minus, equal - 1, (*strat, "="))


def part3():
    opponent_in, track_in = lib.get_input(3).split("\n\n")
    _, opponent_strat = _parse_player(opponent_in)
    track = _parse_track(track_in)

    # Since we don't care about the actual value, we only need to run
    # lcm(5+3+3, len(track)) steps (lcm(5+3+3, len(track)) // len(track) loops).
    # After that point, the cycle of terrain and strategy just repeats, which
    # causes all scores to increase at the same rate.
    track_len = len(track)
    loops = math.lcm(5 + 3 + 3, track_len) // track_len
    print(f"Simulating {loops} loops...")
    opponent_score = _score(opponent_strat, track, loops)
    wins = 0
    for strat in _strat_generator(5, 3, 3):
        if _score(strat, track, loops) > opponent_score:
            wins += 1
    print(f"Part 3: {wins}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
