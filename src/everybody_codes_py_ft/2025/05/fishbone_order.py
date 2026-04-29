# pyright: strict

from everybody_codes_py_ft import common as lib


def _parse_sword(data: str):
    id_in, qualities_in = data.split(":", 1)
    return int(id_in), [int(s) for s in qualities_in.split(",")]


class _FishboneSegment:
    def __init__(self, value: int):
        self.value = value
        self.left: int | None = None
        self.right: int | None = None

    def add(self, value: int):
        if value < self.value and self.left is None:
            self.left = value
            return True
        if value > self.value and self.right is None:
            self.right = value
            return True
        return False

    def number(self):
        return int(
            "".join(
                str(v) for v in (self.left, self.value, self.right) if v is not None
            )
        )


def _build_fishbone(qualities: list[int]):
    segments = [_FishboneSegment(qualities[0])]
    for quality in qualities[1:]:
        for segment in segments:
            if segment.add(quality):
                break
        else:
            segments.append(_FishboneSegment(quality))
    return segments


def _quality(segments: list[_FishboneSegment]):
    return int("".join(str(s.value) for s in segments))


def part1():
    _, qualities = _parse_sword(lib.get_input(1))
    print(f"Part 1: {_quality(_build_fishbone(qualities))}")


def part2():
    swords = {
        sword_id: _quality(_build_fishbone(qualities))
        for sword_id, qualities in (
            _parse_sword(line) for line in lib.get_input(2).splitlines()
        )
    }
    print(f"Part 2: {max(swords.values()) - min(swords.values())}")


def part3():
    swords = sorted(
        (
            (sword_id, _build_fishbone(qualities))
            for sword_id, qualities in (
                _parse_sword(line) for line in lib.get_input(3).splitlines()
            )
        ),
        key=lambda sword: (
            _quality(sword[1]),
            tuple(s.number() for s in sword[1]),
            sword[0],
        ),
        reverse=True,
    )
    checksum = sum((index + 1) * sword_id for index, (sword_id, _) in enumerate(swords))
    print(f"Part 3: {checksum}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
