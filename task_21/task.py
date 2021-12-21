import re

from functools import lru_cache
from collections import namedtuple
from itertools import cycle, product


TEST_DATA = '''\
Player 1 starting position: 4
Player 2 starting position: 8\
'''
INPUT = '''\
Player 1 starting position: 1
Player 2 starting position: 3\
'''

class DeterministicDice:
    def __init__(self):
        self._dice = cycle(range(1, 101))
        self.rolls = 0

    def roll(self):
        self.rolls += 1
        return next(self._dice)

    def roll_three(self):
        return sum([self.roll(), self.roll(), self.roll()])


class Player:
    __slots__ = ('id', 'position', 'score')

    def __init__(self, _id, position, score=0):
        self.id = _id
        self.position = position
        self.score = score

    def __repr__(self):
        return f'<Player id={self.id} position={self.position} score={self.score}>'


class Board:
    def __init__(self, p1, p2, dice):
        self.players = [p1, p2]
        self.dice = dice
        self.current_player = 0

    def turn(self):
        p = self.players[self.current_player]
        roll = self.dice.roll_three()
        next_pos = (p.position + roll) % 10
        if next_pos == 0:
            # wrap around
            next_pos = 10
        # save score and position
        p.score += next_pos
        p.position = next_pos
        # Switch places. (toggle between 0 and 1)
        self.current_player ^= 1

    def simulate_turns(self, target_score):
        p1, p2 = self.players
        while (p1.score < target_score and p2.score < target_score):
            self.turn()


QuantumBoardState = namedtuple('QuantumBoardState', ['a_pos', 'a_score', 'b_pos', 'b_score'])


def decode_input(data: str):
    lines = data.split('\n')
    pattern = r'Player (\d+) starting position: (\d+)'

    p1 = Player(*map(int, re.match(pattern, lines.pop(0)).groups()))
    p2 = Player(*map(int, re.match(pattern, lines.pop(0)).groups()))

    return p1, p2


def calculate_1(data: str) -> int:
    p1, p2 = decode_input(data)
    dice = DeterministicDice()
    board = Board(p1, p2, dice)
    board.simulate_turns(target_score=1000)
    if p1.score >= 1000:
        return p2.score * dice.rolls
    return p1.score * dice.rolls


def calculate_2(data: str) -> int:
    p1, p2 = decode_input(data)
    target_score = 21

    # Dammit. I see lanternfish.
    # We no longer have much use for the object oriented solution.
    # Define state of the board using tuples.
    # Then, recurse with all the possible board and dice states.
    # Save repetitive computation with a cache.
    # Et voila!

    ROLLS = []
    for dies in product(range(1, 4), range(1, 4), range(1, 4)):
        ROLLS.append(sum(dies))

    @lru_cache(maxsize=None)
    def play(state: QuantumBoardState) -> tuple[int, int]:
        if state.a_score >= 21:
            return (1, 0)   # Current Player wins
        if state.b_score >= 21:
            return (0, 1)   # Other Player wins

        curr_wins, other_wins = 0, 0

        for roll in ROLLS:
            pos = (state.a_pos + roll) % 10
            if pos == 0:
                new_pos = 10
            else:
                new_pos = pos
            new_score = state.a_score + new_pos

            next_state = QuantumBoardState(state.b_pos, state.b_score, new_pos, new_score)

            ow, cw = play(next_state)
            curr_wins += cw
            other_wins += ow

        return curr_wins, other_wins

    initial_state = QuantumBoardState(p1.position, 0, p2.position, 0)
    wins = play(initial_state)
    return max(wins)


if __name__ == '__main__':
    assert calculate_1(TEST_DATA) == 739785
    assert calculate_2(TEST_DATA) == 444356092776315

    answer_1 = calculate_1(INPUT)
    answer_2 = calculate_2(INPUT)

    print(f'{answer_1=}')
    print(f'{answer_2=}')
