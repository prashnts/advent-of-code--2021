import os

__here__ = os.path.dirname(__file__)

TEST_DATA = [
    'forward 5',
    'down 5',
    'forward 8',
    'up 3',
    'down 8',
    'forward 2',
]

def parse_command(cmd):
    verb, amount_s = cmd.split(' ')
    return verb, int(amount_s)

def calculate_1(cmds):
    hpos, depth = 0, 0
    for cmd, amount in map(parse_command, cmds):
        if cmd == 'forward':
            hpos += amount
        if cmd == 'down':
            depth += amount
        if cmd == 'up':
            depth -= amount
    return hpos * depth

def calculate_2(cmds):
    hpos, depth, aim = 0, 0, 0

    for cmd, amount in map(parse_command, cmds):
        if cmd == 'forward':
            hpos += amount
            depth += (aim * amount)
        if cmd == 'down':
            aim += amount
        if cmd == 'up':
            aim -= amount
    return hpos * depth


if __name__ == '__main__':
    assert calculate_1(TEST_DATA) == 150
    assert calculate_2(TEST_DATA) == 900

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        commands = fp.read().split('\n')

    answer_1 = calculate_1(commands)
    answer_2 = calculate_2(commands)

    print(f'{answer_1=}')
    print(f'{answer_2=}')
