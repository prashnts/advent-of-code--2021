import os

from collections import Counter

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2\
'''

def decode_input(data):
    lines = data.split('\n')
    for line in lines:
        start, end = line.split(' -> ')
        start_coords = [int(i) for i in start.split(',')]
        end_coords = [int(i) for i in end.split(',')]
        yield [start_coords, end_coords]


def horizontal_or_vertical(segment):
    '''Checks if a segment is horizontal or vertical'''
    [x1, y1], [x2, y2] = segment
    return any([x1 == x2, y1 == y2])


def covered_points(segment):
    '''Returns points covered by a given line segment.

    Assumes either horizontal, vertical, or diagonal segment.

    >>> line = [[0, 0], [2, 0]]
    >>> list(covered_points(line))
    [[0, 0], [1, 0], [2, 0]]
    '''
    [x1, y1], [x2, y2] = segment

    if x1 == x2:
        # Horizontal line needs special attention.
        yield from [[x1, y] for y in range(min(y1, y2), max(y1, y2) + 1)]
    else:
        # We have to use Math. UGH.
        # Equation of a line:
        # y - y1 = ((y2 - y1) / (x2 - x1))(x - x1)
        # => y = ((y2 - y1) / (x2 - x1))(x - x1) + y1
        # We've covered the cases when either of the coordinates are equal above.

        line = lambda x: (((y2 - y1) / (x2 - x1)) * (x - x1)) + y1

        for x in range(min(x1, x2), max(x1, x2) + 1):
            yield [x, int(line(x))]


def coverage(segments):
    '''Generates points that the given line segments cover.'''
    for segment in segments:
        yield from covered_points(segment)


def calculate(segments):
    point_coverage = coverage(segments)
    point_counts = Counter([tuple(p) for p in point_coverage])
    overlaps = [p for p in point_counts.values() if p > 1]
    return len(overlaps)


def calculate_1(data):
    segments = decode_input(data)
    straight_segments = [c for c in segments if horizontal_or_vertical(c)]
    return calculate(straight_segments)


def calculate_2(data):
    segments = decode_input(data)
    return calculate(segments)


if __name__ == '__main__':
    assert calculate_1(TEST_DATA) == 5
    assert calculate_2(TEST_DATA) == 12

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answer_1 = calculate_1(data)
    answer_2 = calculate_2(data)

    print(f'{answer_1=}')
    print(f'{answer_2=}')
