import os

from collections import Counter


__here__ = os.path.dirname(__file__)

TEST_DATA = '3,4,3,1,2'

def calculate_1(data, days):
    # Slow solution. Does not work for days > 150.
    initial_state = list(map(int, data.split(',')))
    state = initial_state[:]

    def next_gen(timer):
        next_timer = timer - 1
        if next_timer == -1:
            next_timer = 6
        return next_timer

    for gen in range(days):
        next_state = [next_gen(t) for t in state]
        next_state.extend([8] * state.count(0))
        state = next_state

    return len(state)


def calculate_2(data, days):
    initial_state = list(map(int, data.split(',')))
    state = Counter(initial_state)

    for gen in range(days):
        next_state = Counter()
        for key, count in state.items():
            if key == 0:
                next_state[6] += count
                next_state[8] += count
            else:
                next_state[key - 1] += count
        state = next_state
    return sum(state.values())


if __name__ == '__main__':
    assert calculate_1(TEST_DATA, 18) == 26
    assert calculate_2(TEST_DATA, 18) == 26
    assert calculate_1(TEST_DATA, 80) == 5934
    assert calculate_2(TEST_DATA, 80) == 5934
    assert calculate_2(TEST_DATA, 256) == 26984457539

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answer_1 = calculate_2(data, 80)
    answer_2 = calculate_2(data, 256)
    print(f'{answer_1=}')
    print(f'{answer_2=}')
