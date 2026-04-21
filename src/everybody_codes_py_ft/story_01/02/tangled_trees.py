# pyright: strict

import re
from collections import defaultdict
from typing import Iterable, Literal, TypeAlias

from everybody_codes_py_ft import common as lib

NodeSpec: TypeAlias = tuple[int, str]


class TreeNode:
    def __init__(self, spec: NodeSpec):
        self.rank, self.symbol = spec
        self.parent: tuple[TreeNode | None, Literal["left", "right"]] | None = None
        self.left: TreeNode | None = None
        self.right: TreeNode | None = None

    def __str__(self):
        return f"<TreeNode rank={self.rank}, symbol='{self.symbol}', left={self.left}, right={self.right}>"


def _insert(root: TreeNode | None, node: TreeNode, side: Literal["left", "right"]):
    if root is None:
        node.parent = (None, side)
        return node
    parent: TreeNode | None = root
    current: TreeNode | None = root
    while current is not None:
        parent = current
        if node.rank < parent.rank:
            current = parent.left
        elif node.rank > parent.rank:
            current = parent.right
        else:
            raise Exception("Duplicate rank")
    if node.rank < parent.rank:
        parent.left = node
        node.parent = (parent, "left")
    elif node.rank > parent.rank:
        parent.right = node
        node.parent = (parent, "right")

    return root


def _traverse(node: TreeNode):
    out = defaultdict[int, list[str]](list)
    out[1].append(node.symbol)
    if node.left:
        for sublevel, subsymbols in _traverse(node.left).items():
            out[sublevel + 1].extend(subsymbols)
    if node.right:
        for sublevel, subsymbols in _traverse(node.right).items():
            out[sublevel + 1].extend(subsymbols)

    return out


def _best_level(levels: dict[int, list[str]]):
    best = list[str]()
    for level in range(len(levels)):
        if len(levels[level + 1]) > len(best):
            best = levels[level + 1]
    return best


def _parse_input(
    data: str,
) -> Iterable[
    tuple[Literal["add"], tuple[int, NodeSpec, NodeSpec]] | tuple[Literal["swap"], int]
]:
    for line in data.splitlines():
        m = re.match(r"^ADD id=(\d+) left=\[(\d+),(\S)\] right=\[(\d+),(\S)\]$", line)
        if m:
            yield (
                "add",
                (
                    int(m.group(1)),
                    (int(m.group(2)), str(m.group(3))),
                    (int(m.group(4)), str(m.group(5))),
                ),
            )
            continue
        m = re.match(r"^SWAP (\d+)$", line)
        if m:
            yield ("swap", int(m.group(1)))
            continue
        raise Exception(f"Malformed line: {line}")


def part1():
    left_root = None
    right_root = None
    for op in _parse_input(lib.get_input(1)):
        assert op[0] == "add"
        _, left_spec, right_spec = op[1]
        left_root = _insert(left_root, TreeNode(left_spec), "left")
        right_root = _insert(right_root, TreeNode(right_spec), "right")
    assert left_root is not None and right_root is not None

    left_levels = _traverse(left_root)
    right_levels = _traverse(right_root)
    word = "".join(_best_level(left_levels)) + "".join(_best_level(right_levels))
    print(f"Part 1: {"".join(word)}")


def part2():
    left_root = None
    right_root = None
    id_map = dict[int, tuple[TreeNode, TreeNode]]()
    for op in _parse_input(lib.get_input(2)):
        if op[0] == "add":
            node_id, left_spec, right_spec = op[1]
            left_node = TreeNode(left_spec)
            right_node = TreeNode(right_spec)
            left_root = _insert(left_root, left_node, "left")
            right_root = _insert(right_root, right_node, "right")
            id_map[node_id] = (left_node, right_node)
        elif op[0] == "swap":
            swap_id = op[1]
            left_node, right_node = id_map[swap_id]
            left_node.rank, right_node.rank = right_node.rank, left_node.rank
            left_node.symbol, right_node.symbol = right_node.symbol, left_node.symbol
    assert left_root is not None and right_root is not None

    left_levels = _traverse(left_root)
    right_levels = _traverse(right_root)
    word = "".join(_best_level(left_levels)) + "".join(_best_level(right_levels))
    print(f"Part 2: {"".join(word)}")


def part3():
    left_root = None
    right_root = None
    id_map = dict[int, tuple[TreeNode, TreeNode]]()
    for op in _parse_input(lib.get_input(3)):
        if op[0] == "add":
            node_id, left_spec, right_spec = op[1]
            left_node = TreeNode(left_spec)
            right_node = TreeNode(right_spec)
            left_root = _insert(left_root, left_node, "left")
            right_root = _insert(right_root, right_node, "right")
            id_map[node_id] = (left_node, right_node)
        elif op[0] == "swap":
            swap_id = op[1]
            left_node, right_node = id_map[swap_id]
            for node, other in ((left_node, right_node), (right_node, left_node)):
                assert node.parent
                parent, side = node.parent
                if side == "left":
                    if parent:
                        parent.left = other
                    else:
                        left_root = other
                else:
                    if parent:
                        parent.right = other
                    else:
                        right_root = other
            left_node.parent, right_node.parent = right_node.parent, left_node.parent
    assert left_root is not None and right_root is not None

    left_levels = _traverse(left_root)
    right_levels = _traverse(right_root)
    word = "".join(_best_level(left_levels)) + "".join(_best_level(right_levels))
    print(f"Part 3: {"".join(word)}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
