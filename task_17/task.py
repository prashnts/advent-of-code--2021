import re

from collections import namedtuple
from itertools import zip_longest


TEST_DATA = 'target area: x=20..30, y=-10..-5'
INPUT = 'target area: x=128..160, y=-142..-88'

Velocity = namedtuple('Velocity', ['x', 'y'])
Position = namedtuple('Position', ['x', 'y'])
Target = namedtuple('Target', ['xmin', 'xmax', 'ymin', 'ymax'])

def sum_n(n: int) -> int:
    return n * (n + 1) // 2

def decode_input(data: str) -> Target:
    pattern = r'target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)'
    match_groups = re.match(pattern, data).groups()
    return Target(*map(int, match_groups))

def simulate(init_velocity: Velocity, target: Target) -> bool:
    velocity = init_velocity
    pos = Position(x=0, y=0)

    while pos.x <= target.xmax and pos.y >= target.ymin:
        if pos.x >= target.xmin and pos.y <= target.ymax:
            return True

        pos = Position(
            x=pos.x + velocity.x,
            y=pos.y + velocity.y)
        velocity = Velocity(
            x=velocity.x - 1 if velocity.x > 0 else 0,
            y=velocity.y - 1)


def calculate_1(data: str) -> int:
    target = decode_input(data)
    return sum_n(target.ymin)


def calculate_2(data: str) -> int:
    target = decode_input(data)

    # Minimum x velocity to reach target is sqrt(2xmin)
    v_xmin = int((2 * target.xmin) ** 0.5)

    valid_velocities = 0

    for vx in range(v_xmin, target.xmax + 1):
        for vy in range(target.ymin, -target.ymin):
            if simulate(Velocity(vx, vy), target):
                valid_velocities += 1

    return valid_velocities


if __name__ == '__main__':
    assert calculate_1(TEST_DATA) == 45
    assert calculate_2(TEST_DATA) == 112

    answer_1 = calculate_1(INPUT)
    answer_2 = calculate_2(INPUT)

    print(f'{answer_1=}')
    print(f'{answer_2=}')
