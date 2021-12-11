import os

from functools import reduce


__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
2199943210
3987894921
9856789892
8767896789
9899965678\
'''

def gen_neighbors(array, x, y):
    '''Generated points in north, south, east, and west directions.

    On edges only valid points are generated.
    '''
    dirs = [
        (x - 1, y),
        (x + 1, y),
        (x, y - 1),
        (x, y + 1),
    ]

    for x, y in dirs:
        if x >= 0 and y >= 0:
            try:
                yield array[x][y]
            except IndexError:
                continue


def decode_input(data):
    lines = data.split('\n')
    for line in lines:
        yield [int(x) for x in line]


def lowest_points(array, shape):
    '''Generates the points that are lower than all neighbors.'''
    x_max, y_max = shape

    for x in range(0, x_max):
        for y in range(0, y_max):
            current = array[x][y]
            neighborhood = gen_neighbors(array, x, y)

            if current < min(neighborhood):
                yield current, (x, y)


def calculate_1(data):
    array = list(decode_input(data))
    x_max, y_max = len(array), len(array[0])

    lows = [x for x, _ in lowest_points(array, (x_max, y_max))]
    risk_levels = sum([r + 1 for r in lows])
    return risk_levels


def flood_fill(data, origin, shape):
    '''Returns an array filled with `10` starting from origin and bounded by `9`.

    Mostly implmented as stack-based recursive flood-fill implementation given on
    Wikipedia.
    See: https://en.wikipedia.org/wiki/Flood_fill#Stack-based_recursive_implementation_(four-way)

    Things to note:
    - Since we know that boundaries of fill are `9`, we fill the points with `10`
      so that we can distinguish those filled points from unfilled or not-to-be filled
      ones.
    - We use a copy of the data as array which is modified recursively by filler.
    - We move in N, S, E, W directions from origin and fill as many points as we can.
    '''
    x_max, y_max = shape
    array = [d[:] for d in data]

    def filler(x, y):
        if x < 0 or y < 0 or x >= x_max or y >= y_max:
            # Bounds check.
            return

        if array[x][y] >= 9:
            # Boundary check.
            return

        array[x][y] = 10    # use this to distinguish filled points.

        filler(x, y + 1)    # North
        filler(x, y - 1)    # South
        filler(x + 1, y)    # East
        filler(x - 1, y)    # West

    filler(*origin)

    return array


def calculate_2(data):
    array = list(decode_input(data))
    x_max, y_max = len(array), len(array[0])

    low_coords = [coord for _, coord in lowest_points(array, (x_max, y_max))]
    basins = []

    for coord in low_coords:
        filled = flood_fill(array, coord, (x_max, y_max))
        basin_size = sum([row.count(10) for row in filled])
        basins.append(basin_size)

    top_3_basins = sorted(basins)[-3:]

    return reduce(lambda x, y: x * y, top_3_basins, 1)


if __name__ == '__main__':
    assert calculate_1(TEST_DATA) == 15
    assert calculate_2(TEST_DATA) == 1134

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answer_1 = calculate_1(data)
    answer_2 = calculate_2(data)

    print(f'{answer_1=}')
    print(f'{answer_2=}')
