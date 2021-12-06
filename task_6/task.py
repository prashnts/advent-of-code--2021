import os
import time

__here__ = os.path.dirname(__file__)

TEST_DATA = '3,4,3,1,2'

def next_gen(timer):
    next_timer = timer - 1
    if next_timer == -1:
        next_timer = 6
    return next_timer

gen_map = {
    0: 6,
    1: 0,
    2: 1,
    3: 2,
    4: 3,
    5: 4,
    6: 5,
    7: 6,
    8: 7,
}


def calculate_1(data, days):
    # Slow solution.
    initial_state = list(map(int, data.split(',')))
    state = initial_state[:]

    for gen in range(days):
        print(gen)
        next_state = [next_gen(t) for t in state]
        next_state.extend([8] * state.count(0))
        state = next_state

    return len(state)


def calculate_2(data, days):
    # "Faster" solution.
    initial_state = list(map(int, data.split(',')))
    state = initial_state[:]
    SPLIT_AT = 100_000_000

    def solve_batch(initial_state, iters, depth, order):
        print(order, iters, depth)
        state = initial_state[:]
        for gen in range(iters):
            zeros = 0
            for i, timer in enumerate(state):
                if timer == 0:
                    zeros += 1
                state[i] = gen_map[state[i]]
            state.extend((8,) * zeros)

            if len(state) > SPLIT_AT:
                split_at = len(state) // 2
                batch_1 = state[:split_at]
                batch_2 = state[split_at:]
                remaining_gens = iters - gen - 1

                return solve_batch(batch_1, remaining_gens, depth + 1, order + '<- ') + solve_batch(batch_2, remaining_gens, depth + 1, order + '-> ')
        return len(state)

    return solve_batch(state, days, 0, '.')


if __name__ == '__main__':
    assert calculate_2(TEST_DATA, 18) == 26
    assert calculate_2(TEST_DATA, 80) == 5934
    assert calculate_2(TEST_DATA, 80) == 5934
    # assert calculate_2(TEST_DATA, 256) == 26984457539

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answer_1 = calculate_1(data, 80)
    answer_2 = calculate_2(data, 256)
    print(f'{answer_1=}')
    print(f'{answer_2=}')
