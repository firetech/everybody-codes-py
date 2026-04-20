# pyright: strict

import re

from everybody_codes_py_ft import common as lib


def _parse_input(data: str):
    for line in data.splitlines():
        rm = re.match(
            r"^A=(\d+) B=(\d+) C=(\d+) X=(\d+) Y=(\d+) Z=(\d+) M=(\d+)$", line
        )
        if not rm:
            raise Exception(f"Malformed line: {line}")
        yield (int(x) for x in rm.groups())


def part1():
    def _eni(n: int, exp: int, mod: int):
        val = 1
        out = list[int]()
        for _ in range(exp):
            val = (val * n) % mod
            out.append(val)
        return int("".join(str(x) for x in reversed(out)))

    max_val = 0
    for a, b, c, x, y, z, m in _parse_input(lib.get_input(1)):
        max_val = max(
            max_val,
            _eni(a, x, m) + _eni(b, y, m) + _eni(c, z, m),
        )
    print(f"Part 1: {max_val}")


def part2():
    def _pow_mod(n: int, exp: int, mod: int):
        # Calculate (n ** exp) % mod using exponentiation by squaring
        val = 1
        n = n % mod
        while exp > 0:
            if exp % 2 == 1:  # odd exponent, include in result
                val = (val * n) % mod
            exp >>= 1
            n = (n * n) % mod
        return val

    def _eni(n: int, exp: int, mod: int):
        out = list[int]()
        for i in range(5):
            out.append(_pow_mod(n, exp - i, mod))
        return int("".join(str(x) for x in out))

    max_val = 0
    for a, b, c, x, y, z, m in _parse_input(lib.get_input(2)):
        max_val = max(
            max_val,
            _eni(a, x, m) + _eni(b, y, m) + _eni(c, z, m),
        )
    print(f"Part 2: {max_val}")


def part3():
    def _eni(n: int, exp: int, mod: int):
        curr = n % mod
        seen = dict[int, int]()
        order = list[int]()
        index = 0
        while curr not in seen:
            seen[curr] = index
            order.append(curr)
            index += 1
            curr = (curr * n) % mod
        cycle_start = seen[curr]
        cycle_end = index
        cycle_sum = sum(order[cycle_start:])
        cycle_len = cycle_end - cycle_start
        q, r = divmod(exp - cycle_start, cycle_len)
        return (
            sum(order[:cycle_start])
            + q * cycle_sum
            + sum(order[cycle_start : cycle_start + r])
        )

    max_val = 0
    for a, b, c, x, y, z, m in _parse_input(lib.get_input(3)):
        max_val = max(
            max_val,
            _eni(a, x, m) + _eni(b, y, m) + _eni(c, z, m),
        )
    print(f"Part 3: {max_val}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
