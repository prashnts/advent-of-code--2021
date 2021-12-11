import os


__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526\
'''

def gen_neighbors(array, x, y):
    '''Generated value and coordinates in NSWE and diagonal directions.'''
    dirs = [
        (x - 1, y),
        (x + 1, y),
        (x, y - 1),
        (x, y + 1),
        (x + 1, y + 1),
        (x - 1, y - 1),
        (x + 1, y - 1),
        (x - 1, y + 1),
    ]

    for x, y in dirs:
        if x >= 0 and y >= 0:
            try:
                yield array[x][y], (x, y)
            except IndexError:
                continue


# flake8: noqa: C901
def calculate_1(data, strategy):
    board = [list(map(int, row)) for row in data.split('\n')]
    sx, sy = len(board), len(board[0])
    state = [r[:] for r in board]
    iters = 0
    flash_count = 0

    while True:
        # Step 1: Energy level of each octopuses increases by 1.
        iters += 1
        next_state = [[c + 1 for c in row] for row in state]

        prev_flashed = []
        while True:
            flashed = prev_flashed[:]

            # Step 2: Those which haven't flashed before, and can flash
            # are flashed and their neighbors gain 1 energy.
            for x in range(sx):
                for y in range(sy):
                    if next_state[x][y] > 9 and (x, y) not in flashed:
                        flashed.append((x, y))
                        neighbors = gen_neighbors(next_state, x, y)
                        for _, (nx, ny) in neighbors:
                            next_state[nx][ny] += 1

            # This will be true as soon as board is stable. Nothing else can
            # flash.
            if set(prev_flashed) == set(flashed):
                break

            prev_flashed = flashed

        # Keep track of flashing lights.
        flash_count += len(prev_flashed)

        # Step 3: Reset those which flashed to zero
        for x, y in prev_flashed:
            next_state[x][y] = 0

        state = next_state

        if strategy == 1:
            # Part 1.
            if iters == 100:
                break
        elif strategy == 2:
            # Part 2. ALL flashed.
            if all([all([c == 0 for c in row]) for row in next_state]):
                return iters
        else:
            raise ValueError('strategy has to be 1 or 2 corresponding to parts.')

    return flash_count


if __name__ == '__main__':
    assert calculate_1(TEST_DATA, 1) == 1656
    assert calculate_1(TEST_DATA, 2) == 195

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answer_1 = calculate_1(data, 1)
    answer_2 = calculate_1(data, 2)

    print(f'{answer_1=}')
    print(f'{answer_2=}')
