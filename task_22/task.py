import os
import re

from collections import namedtuple, defaultdict
from itertools import product
from typing import Iterator


__here__ = os.path.dirname(__file__)

TEST_DATA_1 = '''\
on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10\
'''

with open(os.path.join(__here__, 'test_data.txt'), 'r') as fp:
    TEST_DATA_2 = fp.read()
with open(os.path.join(__here__, 'test_data_2.txt'), 'r') as fp:
    TEST_DATA_3 = fp.read()

Cuboid = namedtuple('Cuboid', ['xmin', 'xmax', 'ymin', 'ymax', 'zmin', 'zmax'])
Point = namedtuple('Point', ['x', 'y', 'z'])
CuboidState = namedtuple('CuboidState', ['cuboid', 'state'])


def decode_input(data: str):
    lines = data.split('\n')
    pattern = r'(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)'

    for line in lines:
        state, *coords = re.match(pattern, line).groups()
        yield state, Cuboid(*map(int, coords))


def do_cuboids_overlap(a: Cuboid, b: Cuboid) -> bool:
    return all([
        a.xmin <= b.xmax,
        a.xmax >= b.xmin,
        a.ymin <= b.ymax,
        a.ymax >= b.ymin,
        a.zmin <= b.zmax,
        a.zmax >= b.zmin,
    ])


def intersect_cuboids(a: Cuboid, b: Cuboid) -> Cuboid:
    return Cuboid(*[
        max(a.xmin, b.xmin), min(a.xmax, b.xmax),
        max(a.ymin, b.ymin), min(a.ymax, b.ymax),
        max(a.zmin, b.zmin), min(a.zmax, b.zmax),
    ])


def gen_points_in_cuboid(c: Cuboid) -> Iterator[Point]:
    gen = product(
        range(c.xmin, c.xmax + 1),
        range(c.ymin, c.ymax + 1),
        range(c.zmin, c.zmax + 1),
    )
    for pt in gen:
        yield Point(*pt)


def nb_cubes_in_cuboid(c: Cuboid) -> int:
    return (
        (c.xmax - c.xmin + 1) *
        (c.ymax - c.ymin + 1) *
        (c.zmax - c.zmin + 1)
    )


def update_cuboids(
    cuboids: list[CuboidState],
    state: bool,
    cuboid: Cuboid
) -> list[CuboidState]:
    # We represent the on off states using 1, -1.
    updates = []
    next_state = 1 if state == 'on' else -1

    for cs in cuboids:
        if do_cuboids_overlap(cs.cuboid, cuboid):
            updates.append(
                CuboidState(
                    cuboid=intersect_cuboids(cs.cuboid, cuboid),
                    state=-cs.state
                )
            )

    if next_state == 1:
        updates.append(CuboidState(cuboid=cuboid, state=1))

    return updates


def calculate_1(data: str) -> int:
    decoded = list(decode_input(data))
    lit_points = defaultdict(bool)

    region = Cuboid(
        xmin=-50, xmax=50,
        ymin=-50, ymax=50,
        zmin=-50, zmax=50,
    )

    for state, cuboid in decoded:
        if not do_cuboids_overlap(cuboid, region):
            continue

        overlap = intersect_cuboids(cuboid, region)

        for pt in gen_points_in_cuboid(overlap):
            lit_points[pt] = state == 'on'

    return len([k for k, v in lit_points.items() if v])


def calculate_2(data: str) -> int:
    decoded = list(decode_input(data))
    cuboids = []

    for state, cuboid in decoded:
        cuboids += update_cuboids(cuboids, state, cuboid)

    return sum(nb_cubes_in_cuboid(c.cuboid) * c.state for c in cuboids)


if __name__ == '__main__':
    assert calculate_1(TEST_DATA_1) == 39
    assert calculate_1(TEST_DATA_2) == 590784
    assert calculate_2(TEST_DATA_3) == 2758514936282235

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answer_1 = calculate_1(data)
    answer_2 = calculate_2(data)

    print(f'{answer_1=}')
    print(f'{answer_2=}')
