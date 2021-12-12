import os

from collections import defaultdict


__here__ = os.path.dirname(__file__)

TEST_DATA_1 = '''\
start-A
start-b
A-c
A-b
b-d
A-end
b-end\
'''
TEST_DATA_2 = '''\
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc\
'''
TEST_DATA_3 = '''\
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW\
'''

def decode_input(data):
    # Returns the bidirectional adjacency list from data.
    lines = data.split('\n')
    pairs = [x.split('-') for x in lines]

    adj_list = defaultdict(set)

    for lt, rt in pairs:
        adj_list[lt].add(rt)
        adj_list[rt].add(lt)

    return adj_list


def calculate_1(data, can_visit_small_twice):
    graph = decode_input(data)
    is_big_cave = lambda node: node.upper() == node
    is_small_cave = lambda node: node.lower() == node and node not in ['start', 'end']
    paths = []

    # DFS to find all paths.
    def dfs(v, initial_state, can_visit_small_twice):
        state = initial_state[:]
        state.append(v)

        for node in graph[v]:
            if node == 'end':
                state.append('end')
                paths.append(state)
            elif is_big_cave(node):
                dfs(node, state, can_visit_small_twice)
            elif node not in state:
                dfs(node, state, can_visit_small_twice)
            elif is_small_cave(node) and can_visit_small_twice:
                dfs(node, state, False)

    dfs('start', [], can_visit_small_twice)
    return len(paths)


if __name__ == '__main__':
    assert calculate_1(TEST_DATA_1, False) == 10
    assert calculate_1(TEST_DATA_2, False) == 19
    assert calculate_1(TEST_DATA_3, False) == 226
    assert calculate_1(TEST_DATA_1, True) == 36
    assert calculate_1(TEST_DATA_2, True) == 103
    assert calculate_1(TEST_DATA_3, True) == 3509

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answer_1 = calculate_1(data, False)
    answer_2 = calculate_1(data, True)

    print(f'{answer_1=}')
    print(f'{answer_2=}')
