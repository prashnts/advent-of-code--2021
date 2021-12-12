import os

__here__ = os.path.dirname(__file__)

TEST_DATA = [
    199,
    200,
    208,
    210,
    200,
    207,
    240,
    269,
    260,
    263,
]

def n_measurements_increasing(measurements):
    pairs = zip(measurements, measurements[1:])
    is_increasing = lambda x, y: x < y
    return [is_increasing(*p) for p in pairs].count(True)


if __name__ == '__main__':
    assert n_measurements_increasing(TEST_DATA) == 7

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        lines = fp.read().split()
        measurements = [int(x) for x in lines]

    answer_1 = n_measurements_increasing(measurements)

    measurements_2 = [
        sum(x) for x in zip(measurements, measurements[1:], measurements[2:])
    ]

    answer_2 = n_measurements_increasing(measurements_2)

    print(f'{answer_1=}')
    print(f'{answer_2=}')
