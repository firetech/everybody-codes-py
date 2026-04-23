# pyright: strict

import re
from typing import TypeAlias

from everybody_codes_py_ft import common as lib


class Die:
    def __init__(self, id_: int, faces: list[int], seed: int):
        self.id = id_
        self.faces = faces
        self.curr_face = 0
        self.seed = seed
        self.pulse = seed
        self.roll_nbr = 1

    def roll(self):
        spin = self.roll_nbr * self.pulse
        self.curr_face = (self.curr_face + spin) % len(self.faces)
        self.pulse = (self.pulse + spin) % self.seed + 1 + self.roll_nbr + self.seed
        self.roll_nbr += 1
        return self.faces[self.curr_face]

    @classmethod
    def parse(cls, line: str):
        m = re.match(r"^(\d+): faces=\[(-?\d+(?:,-?\d+)*)\] seed=(-?\d+)$", line)
        if not m:
            raise Exception(f"Malformed die spec: '{line}'")
        return cls(
            int(m.group(1)), [int(f) for f in m.group(2).split(",")], int(m.group(3))
        )

    def __repr__(self):
        return " ".join(
            (
                f"<Die id={self.id},",
                f"faces={self.faces},",
                f"curr_face={self.curr_face},",
                f"seed={self.seed},",
                f"pulse={self.pulse},",
                f"roll_nbr={self.roll_nbr}>",
            )
        )


def _parse_input(data: str):
    dice_in, *rest = data.split("\n\n", 1)
    if rest:
        grid_in = rest[0].splitlines()
    else:
        grid_in = []
    return (
        [Die.parse(line) for line in dice_in.splitlines()],
        [[int(n) for n in line] for line in grid_in],
    )


def part1():
    dice, _ = _parse_input(lib.get_input(1))
    score = 0
    while score < 10_000:
        score += sum(die.roll() for die in dice)
    print(f"Part 1: {dice[0].roll_nbr-1}")


def part2():
    dice, (track,) = _parse_input(lib.get_input(2))
    n_dice = len(dice)
    track_len = len(track)
    index = [0] * n_dice
    order = list[int]()
    while len(order) < n_dice:
        for d, die in enumerate(dice):
            if index[d] >= track_len:
                continue
            if die.roll() == track[index[d]]:
                index[d] += 1
                if index[d] == track_len:
                    order.append(d + 1)
    print(f"Part 2: {",".join(str(n) for n in order)}")


Pos: TypeAlias = tuple[int, int]


def part3():
    dice, grid = _parse_input(lib.get_input(3))
    height = len(grid)
    width = len(grid[0])
    coins = set[int]()
    for die in dice:
        todo = {y * width + x for y in range(height) for x in range(width)}
        while todo:
            next_todo = set[int]()
            roll = die.roll()
            for p in todo:
                y, x = divmod(p, width)
                if grid[y][x] != roll:
                    continue
                coins.add(p)
                next_todo.add(p)
                for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    nx = x + dx
                    ny = y + dy
                    if nx >= 0 and nx < width and ny >= 0 and ny < height:
                        next_todo.add(ny * width + nx)
            todo = next_todo

    print(f"Part 3: {len(coins)}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
