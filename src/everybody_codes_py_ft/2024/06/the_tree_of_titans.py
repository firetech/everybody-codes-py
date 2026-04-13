# pyright: strict

from collections import defaultdict

from everybody_codes_py_ft import common as lib


def _strongest_fruit_path(data: str) -> list[str]:
    apples = list[str]()
    parents = dict[str, str]()
    for line in data.splitlines():
        (parent, children) = line.split(":", 1)
        if parent in ("BUG", "ANT"):
            continue
        for child in children.split(","):
            if child == "@":
                apples.append(parent)
            elif child not in ("BUG", "ANT"):
                parents[child] = parent

    paths = defaultdict[int, list[list[str]]](list)

    for parent in apples:
        node = parent
        path = ["@", parent]
        while node in parents:
            node = parents[node]
            path.append(node)
        paths[len(path)].append(path)

    (_, (unique_path, *_)) = next(filter(lambda i: len(i[1]) == 1, paths.items()))

    unique_path.reverse()

    return unique_path


def part1():
    path = _strongest_fruit_path(lib.get_input(1))
    print(f"Part 1: {"".join(path)}")


def part2():
    path = _strongest_fruit_path(lib.get_input(2))
    print(f"Part 2: {"".join(node[0] for node in path)}")


def part3():
    path = _strongest_fruit_path(lib.get_input(3))
    print(f"Part 3: {"".join(node[0] for node in path)}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
