import os

__here__ = os.path.dirname(__file__)

TEST_DATA = [
    '00100',
    '11110',
    '10110',
    '10111',
    '10101',
    '01111',
    '00111',
    '11100',
    '10000',
    '11001',
    '00010',
    '01010',
]


def common_bits(bits):
    '''Returns most and least common bit in bits.

    >>> common_bits(['0', '0', '1'])
    ('0', '1')
    '''
    n_1 = bits.count('1')
    n_0 = bits.count('0')

    if n_1 == n_0:
        return ('1', '0')

    return ('1' if n_1 > n_0 else '0', '0' if n_1 > n_0 else '1')

def calculate_1(data):
    stacked_bits = zip(*data)
    gamma = ''
    epsilon = ''

    for stack in stacked_bits:
        mcb, lcb = common_bits(stack)
        gamma += mcb
        epsilon += lcb

    return int(gamma, base=2) * int(epsilon, base=2)


def calculate_2(data):
    ox_gen_rating, co2_scrub_rating = '', ''
    width = len(data[0])

    measurements_ox = data[:]

    for pos in range(width):
        stack_ox = list(zip(*measurements_ox))[pos]
        mcb, _ = common_bits(stack_ox)

        measurements_ox = [measurements_ox[i] for i, value in enumerate(stack_ox) if value == mcb]

        if len(measurements_ox) == 1:
            ox_gen_rating = measurements_ox[0]
            break

    measurements_co2 = data[:]

    for pos in range(width):
        stack_co2 = list(zip(*measurements_co2))[pos]
        _, lcb = common_bits(stack_co2)

        measurements_co2 = [measurements_co2[i] for i, value in enumerate(stack_co2) if value == lcb]

        if len(measurements_co2) == 1:
            co2_scrub_rating = measurements_co2[0]
            break

    return int(ox_gen_rating, base=2) * int(co2_scrub_rating, base=2)


if __name__ == '__main__':
    assert calculate_1(TEST_DATA) == 198
    assert calculate_2(TEST_DATA) == 230

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read().split('\n')

    answer_1 = calculate_1(data)
    answer_2 = calculate_2(data)

    print(f'{answer_1=}')
    print(f'{answer_2=}')
