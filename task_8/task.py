import os

from collections import Counter


__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce\
'''

SEGMENT_MAPPING = {
    0: ['a', 'b', 'c', 'e', 'f', 'g'],
    1: ['c', 'f'],
    2: ['a', 'c', 'd', 'e', 'g'],
    3: ['a', 'c', 'd', 'f', 'g'],
    4: ['b', 'c', 'd', 'f'],
    5: ['a', 'b', 'd', 'f', 'g'],
    6: ['a', 'b', 'd', 'e', 'f', 'g'],
    7: ['a', 'c', 'f'],
    8: ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
    9: ['a', 'b', 'c', 'd', 'f', 'g'],
}


def decode_input(data):
    lines = data.split('\n')
    for line in lines:
        signals, digits = line.split(' | ')
        yield (signals.split(' '), digits.split(' '))


def calculate_1(data):
    unique_segments = [2, 4, 3, 7]  # corresponds to 1, 4, 7, 8 digits
    decoder = decode_input(data)
    n_uniques = 0

    for signals, digits in decoder:
        dig_lens = list(map(len, digits))
        for seg in unique_segments:
            n_uniques += dig_lens.count(seg)

    return n_uniques


def calculate_2(data):
    '''
    For more fun check out: The Broken Digital Clock problem:
    https://andersource.dev/2021/04/29/faulty_digital_clock.html

    Seven
    Segments
    Mapping ->>  --a--
                b|   |c
                 |-d-|
                e|   |f
                 --g--

    tl;dr: We basically process signals and get the correct mapping.

    The correct mapping is given by using some facts:
    -> 1, 4, 7, 8 are always unique.
    -> Segment a is determined by set difference between 7 and 1.
    -> 2, 3, 5 signals are of length 5.
    -> 0, 6, 9 signals are of length 6.
    -> In 2, 3, 5 combined, a, d, and g will be counted thrice. (adg)
    -> Segment bd is determined from set diff of four and one.
    -> Segment dg is determined from adg - a.
    -> Segment be is determined from bcef - cf (1).
    -> Segments d, b, e, g, can then be derived.
    -> We can determine 6 now by checking where d and e is both present
       in length 6 items.
    -> Using six we can get c and f.

    Finally we do a translation between encoded digits and numbers based on
    this information.
    We can use the SEGMENT_MAPPING to map the sequence of digits into numbers.
    '''
    def pull_element(iset):
        '''Pulls one element from a given iterator.
        Asserts if there is only one item in the iterator.
        '''
        elements = list(iset)
        assert len(elements) == 1
        return elements[0]

    def decode_number(digit, mapping):
        translate = lambda imap: ''.join(sorted([mapping[i] for i in imap]))
        new_mapping = {translate(v): k for k, v in SEGMENT_MAPPING.items()}
        digit_sorted = ''.join(sorted(digit))
        return new_mapping[digit_sorted]


    decoder = decode_input(data)
    output_sums = 0

    for signals, digits in decoder:
        # Take unique numbers.
        one   = pull_element(filter(lambda x: len(x) == 2, signals))
        four  = pull_element(filter(lambda x: len(x) == 4, signals))
        seven = pull_element(filter(lambda x: len(x) == 3, signals))
        eight = pull_element(filter(lambda x: len(x) == 7, signals))

        l_fives = list(filter(lambda x: len(x) == 5, signals)) # Two, Five, or Three
        l_six = list(filter(lambda x: len(x) == 6, signals)) # Six, Nine or Zero
        l_fives_s = ''.join(l_fives)

        seg_a = set(seven) - set(one)

        seg_bd = set.symmetric_difference(set(four), set(one))
        seg_dg = set([x for x in l_fives_s if l_fives_s.count(x) == 3]) - seg_a
        seg_be = set([x for x in l_fives_s if l_fives_s.count(x) != 3]) - set(one)

        seg_d = set.intersection(seg_dg, seg_bd)
        seg_b = set.intersection(seg_be, seg_bd)
        seg_e = seg_be - seg_b
        seg_g = seg_dg - seg_d

        a = pull_element(seg_a)
        b = pull_element(seg_b)
        d = pull_element(seg_d)
        e = pull_element(seg_e)
        g = pull_element(seg_g)

        six = [x for x in l_six if d in x and e in x][0]

        seg_c = set(eight) - set(six)
        seg_f = set(one) - seg_c

        c = pull_element(seg_c)
        f = pull_element(seg_f)

        mapping = {'a': a, 'b': b, 'c': c, 'd': d, 'e': e, 'f': f, 'g': g}

        decoded = [decode_number(dig, mapping) for dig in digits]

        output_sums += int(''.join(map(str, decoded)))
    return output_sums


if __name__ == '__main__':
    assert calculate_1(TEST_DATA) == 26
    assert calculate_2(TEST_DATA) == 61229

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answer_1 = calculate_1(data)
    answer_2 = calculate_2(data)

    print(f'{answer_1=}')
    print(f'{answer_2=}')
