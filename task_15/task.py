import os
import heapq as heap

from collections import Counter, defaultdict
from itertools import zip_longest

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581\
'''

def gen_neighbors(array, x, y):
    '''Generated value and coordinates in NSWE directions.'''
    dirs = [
        (x - 1, y),
        (x + 1, y),
        (x, y - 1),
        (x, y + 1),
    ]
    sx = len(array)
    sy = len(array[0])

    for x, y in dirs:
        if 0 <= x < sx and 0 <= y < sy:
            yield array[x][y], (x, y)


def dijkstra(weights, start_node, end_node):
    '''Modified from the implementation here:
    https://levelup.gitconnected.com/dijkstra-algorithm-in-python-8f0e75e3f16e

    Added a clause for end_node and made the code consistent.
    '''
    visited = set()
    parents_map = {}
    pq = []
    node_costs = defaultdict(lambda: float('inf'))
    node_costs[start_node] = 0
    heap.heappush(pq, (0, start_node))
 
    while pq:
        # go greedily by always extending the shorter cost nodes first
        _, node = heap.heappop(pq)
        if node == end_node:
            break
        visited.add(node)
 
        for weight, adj_node in gen_neighbors(weights, node[0], node[1]):
            if adj_node in visited:
                continue
                
            new_cost = node_costs[node] + weight
            if node_costs[adj_node] > new_cost:
                parents_map[adj_node] = node
                node_costs[adj_node] = new_cost
                heap.heappush(pq, (new_cost, adj_node))
        
    return parents_map, node_costs


def calculate_1(data):
    weights = [list(map(int, list(row))) for row in data.split('\n')]
    x_max, y_max = len(weights), len(weights[0])
    start = (0, 0)
    end = (x_max - 1, y_max - 1)

    _, costs = dijkstra(weights, start, end)

    return costs[end]


def calculate_2(data):
    init_weights = [list(map(int, list(row))) for row in data.split('\n')]

    def repeat_grid(grid, times):
        sx, sy = len(grid), len(grid[0])

        new_grid = [[... for _ in range(sx * times)] for _ in range(sy * times)]

        for x in range(sx * times):
            for y in range(sy * times):
                prev = grid[x % sx][y % sy]
                updated = (prev + (x // sx + y // sy)) % 9
                new_grid[x][y] = 9 if updated == 0 else updated

        return new_grid

    weights = repeat_grid(init_weights, 5)

    x_max, y_max = len(weights), len(weights[0])
    start = (0, 0)
    end = (x_max - 1, y_max - 1)

    _, costs = dijkstra(weights, start, end)

    return costs[end]


if __name__ == '__main__':
    assert calculate_1(TEST_DATA) == 40
    assert calculate_2(TEST_DATA) == 315

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answer_1 = calculate_1(data)
    answer_2 = calculate_2(data)

    print(f'{answer_1=}')
    print(f'{answer_2=}')
