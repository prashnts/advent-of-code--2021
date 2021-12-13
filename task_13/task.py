import os

from collections import defaultdict


__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5\
'''


def decode_input(data):
    lines = data.split('\n')
    coords = []
    folds = []

    while True:
        line = lines.pop(0)
        if line == '':
            break
        coords.append(tuple(map(int, line.split(','))))

    for line in lines:
        offset = len('fold along ')
        axis, amount = line[offset:].split('=')
        folds.append((axis, int(amount)))

    return coords, folds


class Paper:
    def __init__(self, dots):
        self.dots = dots

    def fold(self, on, amnt):
        new_points = []

        for pt in self.dots:
            if on == 'x':
                if pt[0] < amnt:
                    new_points.append(pt)
                    continue
                ax = pt[0] - 2 * (pt[0] - amnt)
                new_points.append((ax, pt[1]))
            elif on == 'y':
                if pt[1] < amnt:
                    new_points.append(pt)
                    continue
                ay = pt[1] - 2 * (pt[1] - amnt)
                new_points.append((pt[0], ay))
        return Paper(new_points)

    @property
    def visible(self):
        return len(set(self.dots))

    @property
    def shape(self):
        sx, sy = zip(*self.dots)
        return (max(sx), max(sy))

    def __repr__(self):
        # generates a view of the board, colored wherever dots are.
        # Since it uses ANSI escape sequences, only supported in *nix.
        sx, sy = self.shape
        arr = [['\033[36m░' for _ in range(sx + 1)] for _ in range(sy + 1)]
        for dx, dy in self.dots:
            arr[dy][dx] = '\033[33m█'
        preview = '\n'.join([''.join(row) for row in arr])
        preview = preview + '\033[0m'   # Reset
        return preview


def calculate_1(data):
    coords, folds = decode_input(data)
    return (Paper(coords)
        .fold(*folds[0])
        .visible)

def calculate_2(data):
    coords, folds = decode_input(data)
    paper = Paper(coords)
    for fold in folds:
        paper = paper.fold(*fold)
    return paper


if __name__ == '__main__':
    assert calculate_1(TEST_DATA) == 17

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answer_1 = calculate_1(data)

    print(f'{answer_1=}')

    print('Please read the resulting state from below:')
    print(calculate_2(data))
