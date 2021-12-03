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


if __name__ == '__main__':
    assert calculate_1(TEST_DATA) == 198

    with open('./task_3.input.txt', 'r') as fp:
        data = fp.read().split('\n')

    answer_1 = calculate_1(data)

    print(f'{answer_1=}')
