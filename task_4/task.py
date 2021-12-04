import os
import re

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7\
'''

def decode_input(data):
    # begin with splitting data by lines.
    lines = data.split('\n')

    # The first line of the data is our random numbers.
    rand_numbers = lines.pop(0)
    yield [int(x) for x in rand_numbers.split(',')]

    boards_coded = [line for line in lines if line]

    for i in range(len(boards_coded) // 5):
        rows = boards_coded[i * 5:(i + 1) * 5]
        split_nums = lambda row: re.split(r'\s+', row.strip())
        make_cells = lambda row: [[int(x), False] for x in row]

        board = [make_cells(split_nums(row)) for row in rows]
        yield board

def mark_board(board, num):
    # make a copy of the board.
    board = [row[:] for row in board]
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            cell_num, _ = cell
            if cell_num == num:
                board[i][j][1] = True
    return board

def is_winning(board):
    # we need to check if either a row-wise or a column-wise direction is
    # marked true.
    check_line = lambda line: all([x[1] for x in line])

    row_wise = any([check_line(row) for row in board])
    column_wise = any([check_line(col) for col in zip(*board)])

    return row_wise or column_wise

def sum_unmarked(board):
    total = 0
    for row in board:
        for cell_num, state in row:
            if not state:
                total += cell_num
    return total


def calculate_1(data):
    decoder = decode_input(data)
    rands = next(decoder)
    boards = list(decoder)

    for num in rands:
        for i, board in enumerate(boards):
            new_board = mark_board(board, num)
            boards[i] = new_board

        # now check all boards for winner.
        for board in boards:
            if is_winning(board):
                return sum_unmarked(board) * num


def calculate_2(data):
    decoder = decode_input(data)
    rands = next(decoder)
    boards = list(decoder)

    for num in rands:
        for i, board in enumerate(boards):
            new_board = mark_board(board, num)
            boards[i] = new_board

        # Only one board should be left after eliminating winning boards.
        if len(boards) == 1 and is_winning(boards[0]):
            return sum_unmarked(boards[0]) * num

        # Eliminate boards that are winning.
        boards = [board for board in boards if not is_winning(board)]


if __name__ == '__main__':
    assert calculate_1(TEST_DATA) == 4512
    assert calculate_2(TEST_DATA) == 1924

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answer_1 = calculate_1(data)
    answer_2 = calculate_2(data)

    print(f'{answer_1=}')
    print(f'{answer_2=}')
