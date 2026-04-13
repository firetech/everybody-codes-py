# pyright: strict

from everybody_codes_py_ft import common as lib

# Acolytes and block supply for parts 2 and 3 are manually added to the inputs.


def part1():
    blocks = int(lib.get_input(1))
    target = 1
    base = 1
    while target < blocks:
        base += 2
        target += base
    print(f"Part 1: {(target - blocks) * base}")


def part2():
    priests, acolytes, supply = (int(x) for x in lib.get_input(2).split("\n", 3))
    target = 1
    thickness = 1
    base = 1
    while target < supply:
        thickness = (thickness * priests) % acolytes
        base += 2
        target += base * thickness
    print(f"Part 2: {(target - supply) * base}")


def part3():
    priests, acolytes, supply = (int(x) for x in lib.get_input(3).split("\n", 3))
    target = 1
    thickness = 1
    base = 1
    column_heights = [1]
    while target < supply:
        thickness = (thickness * priests) % acolytes + acolytes
        base += 2
        column_heights = [h + thickness for h in column_heights]
        target = thickness * 2
        for i, h in enumerate(column_heights):
            to_remove = (priests * base * h) % acolytes
            column_blocks = h - to_remove
            target += column_blocks
            if i > 0:
                target += column_blocks
        column_heights.append(thickness)
    print(f"Part 3: {target - supply}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
