# pyright: strict

from everybody_codes_py_ft import common as lib


def part1():
    wheel = [1]
    lefts = list[int]()
    for i, line in enumerate(lib.get_input(1).splitlines()):
        num = int(line)
        if i & 1 == 0:
            wheel.append(num)
        else:
            lefts.append(num)
    wheel.extend(lefts[::-1])
    print(f"Part 1: {wheel[2025 % len(wheel)]}")


def _range_wheel(part: int, moves: int):
    wheel = [range(1, 2)]
    lefts = list[range]()
    for i, line in enumerate(lib.get_input(part).splitlines()):
        start, end = line.split("-", 2)
        if i & 1 == 0:
            wheel.append(range(int(start), int(end) + 1))
        else:
            lefts.append(range(int(end), int(start) - 1, -1))
    wheel.extend(lefts[::-1])

    range_lens = [len(r) for r in wheel]
    positions = sum(range_lens)
    end_pos = moves % positions
    i = 0
    while end_pos >= range_lens[i]:
        end_pos -= range_lens[i]
        i += 1
    return wheel[i][end_pos]


def part2():
    print(f"Part 2: {_range_wheel(2, 20252025)}")


def part3():
    print(f"Part 3: {_range_wheel(3, 202520252025)}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
