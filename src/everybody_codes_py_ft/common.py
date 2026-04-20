# pyright: strict

import pathlib as pl
import re
import sys


def get_input(part: int):
    if len(sys.argv) > 1:
        input_folder = pl.Path(sys.argv[1])
    else:
        input_folder = pl.Path("input")

    solution_folder = pl.Path(sys.argv[0]).parent.relative_to(pl.Path())
    quest = solution_folder.name
    event = solution_folder.parent.name
    if m := re.match(r"^story_0*(\d+)$", event):
        event = m.group(1)
    return (
        (input_folder / f"everybody_codes_e{event}_q{quest}_p{part}.txt")
        .read_text()
        .rstrip()
    )
