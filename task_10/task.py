import os

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]\
'''

OPENINGS = ['(', '[', '{', '<']
CLOSINGS = [')', ']', '}', '>']
PAIRS = {
    '(': ')', ')': '(',
    '{': '}', '}': '{',
    '[': ']', ']': '[',
    '<': '>', '>': '<',
}
SYNTAX_POINTS = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}
AUTOCOMP_POINTS = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}

def is_corrupted(line):
    '''Simple "stack" based matching of the brackets.

    stack keeps track of previous characters, while we
    try to empty it. In our case it will never be empty
    though, so we just return the stack state.
    '''
    stack = []
    for c in line:
        if c in OPENINGS:
            stack.append(c)
        elif c in CLOSINGS:
            n = PAIRS[stack.pop()]
            if n != c:
                return True, c, stack
    return False, c, stack


def calculate_1(data):
    lines = data.split('\n')
    score = 0

    for line in lines:
        corrupt, char, _ = is_corrupted(line)
        if corrupt:
            score += SYNTAX_POINTS[char]
    return score


def calculate_2(data):
    lines = data.split('\n')

    scores = []

    for line in lines:
        corrupt, _, stack = is_corrupted(line)
        if not corrupt:
            # We can now take the stack and complete it in reverse.
            completion = [PAIRS[s] for s in stack[::-1]]
            score = 0
            for c in completion:
                score *= 5
                score += AUTOCOMP_POINTS[c]
            scores.append(score)

    midpoint = len(scores) // 2
    return sorted(scores)[midpoint]


if __name__ == '__main__':
    assert calculate_1(TEST_DATA) == 26397
    assert calculate_2(TEST_DATA) == 288957

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answer_1 = calculate_1(data)
    answer_2 = calculate_2(data)

    print(f'{answer_1=}')
    print(f'{answer_2=}')
