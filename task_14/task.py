import os

from collections import Counter
from itertools import zip_longest


__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C\
'''

def decode_input(data):
    lines = data.split('\n')
    sequence = lines.pop(0)
    lines.pop(0)  # Empty line
    insertion_rules = {}
    for line in lines:
        p, v = line.split(' -> ')
        insertion_rules[p] = v
    return sequence, insertion_rules


def calculate_1(data, iters):
    # Naive approach, but works for ~22-25 (if you wait enough).
    # Basically this one keeps the whole sequence in memory and interleaves
    # the substitutions for each step.
    sequence, insertion_rules = decode_input(data)

    if iters > 22:
        print('Oh no. You\'re gonna have to wait for years. Use second solution.')
        raise RuntimeError('Boop! Saved you from using 10PB of memory.')

    for i in range(iters):
        substitutions = [
            insertion_rules.get(y, '')
            for y in [
                ''.join(x) for x in zip(sequence, sequence[1:])
            ]
        ]

        sequence = ''.join(i + j for i, j in zip_longest(sequence, substitutions, fillvalue=''))

    counts = Counter(sequence)

    return counts.most_common()[0][1] - counts.most_common()[-1][1]


def calculate_2(data, iters):
    # Similar to task 6, this grows exponentially.
    # We just cannot bruteforce our way! So, here we just keep track of
    # the pairs, elements and their corresponding counts.
    # The pairs are counted same number of times as their previous count.
    sequence, insertion_rules = decode_input(data)

    pairs = Counter()
    elements = Counter(sequence)

    for s, t in zip(sequence, sequence[1:]):
        pairs[s + t] += 1

    for i in range(iters):
        new_pairs = Counter()

        for pair, count in pairs.items():
            if pair in insertion_rules:
                char = insertion_rules[pair]
                new_pairs[pair[0] + char] += count
                new_pairs[char + pair[1]] += count
                elements[char] += count

        pairs = new_pairs

    return elements.most_common()[0][1] - elements.most_common()[-1][1]


if __name__ == '__main__':
    assert calculate_1(TEST_DATA, 10) == 1588
    assert calculate_2(TEST_DATA, 10) == 1588
    assert calculate_2(TEST_DATA, 40) == 2188189693529

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answer_1 = calculate_1(data, 10)
    answer_2 = calculate_2(data, 40)

    print(f'{answer_1=}')
    print(f'{answer_2=}')
