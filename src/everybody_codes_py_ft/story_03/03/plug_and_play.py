# pyright: strict

from __future__ import annotations

import dataclasses as dc
import pathlib as pl
import re
from typing import Iterable, Literal, TypeAlias, overload

from everybody_codes_py_ft import common as lib

Connector: TypeAlias = tuple[str, ...]


def _can_connect(plug: Connector, socket: Connector, part: int):
    if part == 1:
        return plug == socket
    else:
        return any(p == s for p, s in zip(plug, socket))


@dc.dataclass(kw_only=True)
class Node:
    id: int
    plug: Connector
    left_socket: Connector
    right_socket: Connector
    data: str
    left: Node | None = None
    right: Node | None = None

    def connect(self, new_node: Node, part: int) -> Node | None:
        if self.left:
            if (
                part == 3
                and self.left.plug != self.left_socket
                and new_node.plug == self.left_socket
            ):
                # Replace weak bond with strong bond, continue with previous left node
                self.left, new_node = new_node, self.left
            else:
                result = self.left.connect(new_node, part)
                if result is None:
                    return None
                else:
                    new_node = result
        elif _can_connect(new_node.plug, self.left_socket, part):
            self.left = new_node
            return None

        if self.right:
            if (
                part == 3
                and self.right.plug != self.right_socket
                and new_node.plug == self.right_socket
            ):
                # Replace weak bond with strong bond, continue with previous right node
                self.right, new_node = new_node, self.right
            else:
                result = self.right.connect(new_node, part)
                if result is None:
                    return None
                else:
                    new_node = result
        elif _can_connect(new_node.plug, self.right_socket, part):
            self.right = new_node
            return None

        # Node not connected, send it on for another lap
        return new_node

    @overload
    def read(self, attr: Literal["id"] = "id") -> Iterable[int]: ...
    @overload
    def read(self, attr: Literal["data"]) -> Iterable[str]: ...

    def read(self, attr: Literal["id", "data"] = "id") -> Iterable[int | str]:
        if self.left:
            yield from self.left.read(attr)
        yield self.data if attr == "data" else self.id
        if self.right:
            yield from self.right.read(attr)


def _parse_node(line: str):
    m = re.match(
        r"^id=(\d+), plug=(.+), leftSocket=(.+), rightSocket=(.+), data=(.+)$", line
    )
    if m is None:
        raise Exception(f"Malformed line: {line}")
    return Node(
        id=int(m[1]),
        plug=tuple(m[2].split(" ")),
        left_socket=tuple(m[3].split(" ")),
        right_socket=tuple(m[4].split(" ")),
        data=m[5],
    )


def _connect_nodes(part: int) -> Node:
    root: Node | None = None
    for node in (_parse_node(line) for line in lib.get_input(part).splitlines()):
        if root is None:
            root = node
        else:
            while node is not None:
                node = root.connect(node, part)
    assert root is not None
    return root


def _checksum(root: Node):
    return sum((i + 1) * node_id for i, node_id in enumerate(root.read()))


def _solve(part: int):
    root = _connect_nodes(part)
    self_dir = pl.Path(__file__).parent
    with open(self_dir / f"data{part}.txt", "w") as f:
        for line in root.read("data"):
            f.write(line)
            f.write("\n")
    return _checksum(root)


def part1():
    print(f"Part 1: {_solve(1)}")


def part2():
    print(f"Part 2: {_solve(2)}")


def part3():
    print(f"Part 3: {_solve(3)}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
