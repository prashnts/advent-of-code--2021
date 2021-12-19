# This attempt is a mix of implementation from here:
# https://github.com/kupuguy/aoc2021/blob/main/src/day19.py
# Mostly in similar direction, but I am happy that I came up with my attempt on
# my own, but just couldn't get past the rotation/translation part.
import os
import re

from itertools import combinations
from functools import cached_property, lru_cache


__here__ = os.path.dirname(__file__)

with open(os.path.join(__here__, 'test_data.txt'), 'r') as fp:
    TEST_DATA = fp.read()


class Vector3d:
    __slots__ = ('x', 'y', 'z')

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __sub__(self, other):
        return Vector3d(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other):
        return Vector3d(self.x + other.x, self.y + other.y, self.z + other.z)

    def matrix(self, other: 'Vector3d'):
        # Returns rotation matrix for other.
        # Copied from the implementation mentioned above.
        x = [
            1 if self.x == other.x else -1 if self.x == -other.x else 0,
            1 if self.y == other.x else -1 if self.y == -other.x else 0,
            1 if self.z == other.x else -1 if self.z == -other.x else 0,
        ]
        y = [
            1 if self.x == other.y else -1 if self.x == -other.y else 0,
            1 if self.y == other.y else -1 if self.y == -other.y else 0,
            1 if self.z == other.y else -1 if self.z == -other.y else 0,
        ]
        z = [
            1 if self.x == other.z else -1 if self.x == -other.z else 0,
            1 if self.y == other.z else -1 if self.y == -other.z else 0,
            1 if self.z == other.z else -1 if self.z == -other.z else 0,
        ]
        if sum(map(abs, x + y + z)) == 3:
            return [x, y, z]

    def rotate(self, matrix: list[list[int]]):
        return Vector3d(
            self.x * matrix[0][0] + self.y * matrix[0][1] + self.z * matrix[0][2],
            self.x * matrix[1][0] + self.y * matrix[1][1] + self.z * matrix[1][2],
            self.x * matrix[2][0] + self.y * matrix[2][1] + self.z * matrix[2][2],
        )
    
    def eucledian_distance(self, other: 'Vector3d') -> float:
        dx = (self.x - other.x) ** 2
        dy = (self.y - other.y) ** 2
        dz = (self.z - other.z) ** 2
        return (dx + dy + dz) ** 0.5

    def manhattan_distance(self, other: 'Vector3d') -> float:
        diff = [
            abs(self.x - other.x),
            abs(self.y - other.y),
            abs(self.z - other.z),
        ]
        return sum(diff)

    @lru_cache
    def neighbor_distances(self, neighbors: list['Vector3d']) -> set[int]:
        return {self.eucledian_distance(other) for other in neighbors if other != self}

    def __repr__(self):
        return f'<Vec3d x={self.x} y={self.y} z={self.z}>'


class Scanner:
    def __init__(self, sid, position=None, beacons=None):
        self.sid = sid
        self.position = position
        self.beacons = beacons

    def __repr__(self):
        return f'<Scanner sid={self.sid} position={self.position}>'

    @cached_property
    def distances(self) -> set[int]:
        dists = set()
        s_beacons = frozenset(self.beacons)
        for beacon in self.beacons:
            dists |= beacon.neighbor_distances(s_beacons)
        return dists

    def overlap(self, other: 'Scanner') -> int:
        return len(self.distances & other.distances)

    def shift(self, other: 'Scanner'):
        '''Finds best set of overlapping points and updates self position and beacons.'''
        s_beacons = frozenset(self.beacons)
        o_beacons = frozenset(other.beacons)
        candidates = sorted(
            [(beacon, o_beacons) for beacon in self.beacons for o_beacons in other.beacons],
            key=lambda x: len(
                x[0].neighbor_distances(s_beacons) & x[1].neighbor_distances(o_beacons)
            ),
            reverse=True,
        )
        for p1, p2 in zip(candidates, candidates[1:]):
            matrix = (p1[0] - p2[0]).matrix(p1[1] - p2[1])
            if matrix:
                break
        self.position = candidates[0][1] - candidates[0][0].rotate(matrix)
        self.beacons = {beacon.rotate(matrix) + self.position for beacon in self.beacons}


def decode_input(data: str) -> list[Scanner]:
    lines = data.split('\n')
    header_pattern = r'--- scanner (\d+) ---'

    scanners = []
    current_scanner = None

    for line in lines:
        if line == '':
            continue
        header = re.match(header_pattern, line)
        if header:
            current_scanner = int(header.groups()[0])
            scanners.append(Scanner(current_scanner, None, set()))
            continue
        scanners[-1].beacons.add(Vector3d(*map(int, line.split(','))))

    scanners[0].position = Vector3d(0, 0, 0)
    return scanners


def reduce_scanners(scanners: list[Scanner]) -> list[Scanner]:
    scanner_0 = scanners.pop(0)
    known = [scanner_0]
    while scanners:
        best, other = max(
            [(unknown, other) for unknown in scanners for other in known],
            key=lambda s: s[0].overlap(s[1]),
        )
        known.append(best)
        best.shift(other)
        scanners = [s for s in scanners if s is not best]
    return known


def calculate_1(data: str) -> int:
    scanners = decode_input(data)
    known_scanners = reduce_scanners(scanners)

    beacons = set()
    for scanner in known_scanners:
        beacons |= scanner.beacons

    return len(beacons)


def calculate_2(data: str) -> int:
    scanners = decode_input(data)
    known_scanners = reduce_scanners(scanners)

    return max([
        p.position.manhattan_distance(q.position)
        for p, q in combinations(known_scanners, 2)
    ])


if __name__ == '__main__':
    assert calculate_1(TEST_DATA) == 79
    assert calculate_2(TEST_DATA) == 3621

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answer_1 = calculate_1(data)
    answer_2 = calculate_2(data)

    print(f'{answer_1=}')
    print(f'{answer_2=}')
