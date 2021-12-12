import os

__here__ = os.path.dirname(__file__)

TEST_DATA = '16,1,2,0,4,2,7,1,2,14'

def calculate_1(data, strategy=0):
    hpos = list(map(int, data.split(',')))

    def cost(target):
        if strategy == 0:
            mapper = lambda pos: abs(pos - target)
        elif strategy == 1:
            sum_first_n = lambda n: (n * (n - 1)) // 2
            mapper = lambda pos: sum_first_n(abs(pos - target) + 1)
        else:
            raise ValueError('strategy should be either 0 or 1.')
        return sum([mapper(pos) for pos in hpos])

    extents = min(hpos), max(hpos)
    costs = [(target, cost(target)) for target in range(*extents)]
    return min(costs, key=lambda x: x[1])[1]


if __name__ == '__main__':
    assert calculate_1(TEST_DATA) == 37
    assert calculate_1(TEST_DATA, 1) == 168

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answer_1 = calculate_1(data)
    answer_2 = calculate_1(data, 1)

    print(f'{answer_1=}')
    print(f'{answer_2=}')
