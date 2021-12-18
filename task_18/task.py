# Mostly thanks to this implementation:
# https://github.com/kupuguy/aoc2021/blob/main/src/day18.py
# I was writing it with a binary tree implementation, but that did not go anywhere.
# I did copy almost all the logic from the link above, but I ended up using my old
# implementation with SnailNode as well. Most of what you see here is not my work.
# My most "significant" contribution here is the docstrings. YAY! 
import os
import json

from typing import Union
from collections import namedtuple
from itertools import permutations


__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]\
'''

SnailNode = namedtuple('SnailNode', ['value', 'depth'])
SnailNum = Union[int, list]
MaybeSnailNodes = Union[list[SnailNode], None]


def decode_input(data: str):
    for line in data.split('\n'):
        yield json.loads(line)

def flatten_snails(snails: SnailNum, depth=0) -> list[SnailNode]:
    '''Generate a flat list of SnailNodes which contain their values and depth.
    
    >>> flatten_snails([[[1, 2], [3, [4, 5]]], [1, 2]])
    [SnailNode(value=1, depth=2),
     SnailNode(value=2, depth=2),
     SnailNode(value=3, depth=2),
     SnailNode(value=4, depth=3),
     SnailNode(value=5, depth=3),
     SnailNode(value=1, depth=1),
     SnailNode(value=2, depth=1)]
    '''
    left, right = snails

    lhs = [SnailNode(left, depth)] if type(left) == int else flatten_snails(left, depth + 1)
    rhs = [SnailNode(right, depth)] if type(right) == int else flatten_snails(right, depth + 1)
    return lhs + rhs

def reconstruct_snails(flat: list[SnailNode]) -> SnailNum:
    '''Given a flattened list of snailnodes, this reconstructs original SnailNum.
    >>> reconstruct_snails([SnailNode(0, 0), SnailNode(1, 1), SnailNode(2, 1)])
    [0, [1, 2]]
    '''
    flat = [(x.value, x.depth) for x in flat]

    while len(flat) > 1:
        for i in range(len(flat) - 1):
            if flat[i][1] == flat[i + 1][1]:
                flat = (
                    flat[:i]
                    + [([flat[i][0], flat[i + 1][0]], flat[i][1] - 1)]
                    + flat[i + 2:]
                )
                break
    return flat[0][0]

def explode_flattened(flat: list[SnailNode]) -> MaybeSnailNodes:
    '''Takes a flattened list of SnailNodes, and explodes node deeper than 4.'''
    for i in range(len(flat)):
        if flat[i].depth == 4:
            if i > 0:
                value = flat[i - 1].value + flat[i].value
                depth = flat[i - 1].depth
                flat[i - 1] = SnailNode(value, depth)
            if i < len(flat) - 2:
                value = flat[i + 1].value + flat[i + 2].value
                depth = flat[i + 2].depth
                flat[i + 2] = SnailNode(value, depth)
            flat[i:i + 2] = [SnailNode(0, flat[i].depth - 1)]
            return flat
    return None

def split_flattened(flat: list[SnailNode]) -> MaybeSnailNodes:
    '''Splits a SnailNode in flattened list into two SnailNodes.'''
    for i in range(len(flat)):
        node = flat[i]
        if node.value >= 10:
            flat[i:i + 1] = [
                SnailNode(node.value // 2, node.depth + 1),
                SnailNode((node.value + 1) // 2, node.depth + 1),
            ]
            return flat
    return None

def reduce_flattened(flat: list[SnailNode]):
    '''Explodes a SnailNum to get another SnailNum.'''
    while True:
        exploded = explode_flattened(flat)
        if exploded:
            flat = exploded
            continue
        splitted = split_flattened(flat)
        if splitted:
            flat = splitted
            continue

        return reconstruct_snails(flat)

def add_snails(numbers: SnailNum) -> SnailNum:
    total = numbers[0]
    for num in numbers[1:]:
        total = reduce_flattened(flatten_snails([total, num]))

    return total

def magnitude(numbers: SnailNum) -> int:
    if type(numbers) == int:
        return numbers
    return 3 * magnitude(numbers[0]) + 2 * magnitude(numbers[1])


def calculate_1(data: str) -> int:
    snail_nums = list(decode_input(data))
    total = add_snails(snail_nums)
    return magnitude(total)


def calculate_2(data: str) -> int:
    snail_nums = list(decode_input(data))

    pairs = permutations(snail_nums, 2)

    return max(map(lambda p: magnitude(add_snails(p)), pairs))



if __name__ == '__main__':
    assert calculate_1(TEST_DATA) == 4140
    assert calculate_2(TEST_DATA) == 3993

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answer_1 = calculate_1(data)
    answer_2 = calculate_2(data)

    print(f'{answer_1=}')
    print(f'{answer_2=}')
