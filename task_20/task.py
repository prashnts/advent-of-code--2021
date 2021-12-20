import os

from typing import Iterator


__here__ = os.path.dirname(__file__)

with open(os.path.join(__here__, 'test_data.txt'), 'r') as fp:
    TEST_DATA = fp.read()


class ImageTile:
    __slots__ = ('bitmap', 'background')

    def __init__(self, bitmap: list[list[str]], background='.'):
        self.background = background
        self.bitmap = self._pad_bitmap(bitmap, background)

    def _pad_bitmap(self, bitmap, background):
        # expand the bitmap. by 1 in each direction.
        sx, sy = len(bitmap), len(bitmap[0])

        bmp = [[background for _ in range(sx + 2)] for _ in range(sy + 2)]
        for x in range(sx):
            for y in range(sy):
                bmp[x + 1][y + 1] = bitmap[x][y]

        return bmp

    @property
    def shape(self) -> tuple[int, int]:
        return len(self.bitmap), len(self.bitmap[0])

    def surroundings(self, x: int, y: int) -> Iterator[str]:
        dirs = [
            (x - 1, y - 1),
            (x,     y - 1),
            (x + 1, y - 1),
            (x - 1, y),
            (x,     y),
            (x + 1, y),
            (x - 1, y + 1),
            (x,     y + 1),
            (x + 1, y + 1),
        ]

        for ax, ay in dirs:
            if ax >= 0 and ay >= 0:
                try:
                    yield self.bitmap[ay][ax]
                except IndexError:
                    yield self.background
            else:
                yield self.background

    def enhance_pixel(self, algo: str, x: int, y: int) -> str:
        subtile = list(self.surroundings(x, y))
        enhancement_num = ''.join(subtile).replace('#', '1').replace('.', '0')
        return algo[int(enhancement_num, base=2)]

    def enhance(self, algo: str, inplace=False) -> 'ImageTile':
        sx, sy = self.shape
        bmp = [[self.background for _ in range(sx)] for _ in range(sy)]

        for x in range(sx):
            for y in range(sy):
                px = self.enhance_pixel(algo, x, y)
                bmp[y][x] = px

        bg = '1' if self.background == '#' else '0'
        next_background = algo[int(bg * 9, base=2)]

        if inplace:
            self.background = next_background
            self.bitmap = self._pad_bitmap(bmp, next_background)
            return self

        return ImageTile(bmp, next_background)

    @property
    def repr(self) -> str:
        img = '\n'.join([''.join(row) for row in self.bitmap])
        blocky = img.replace('#', '\033[33m#').replace('.', '\033[36m⋅')
        return f'{blocky}\033[0m'

    @property
    def n_lit_pixels(self) -> int:
        return sum([row.count('#') for row in self.bitmap])

    def __repr__(self) -> str:
        return f'<ImageTile shape={self.shape}>'



def decode_input(data: str):
    lines = data.split('\n')
    enhancement_algo = lines.pop(0)

    lines.pop(0)    # skip empty line

    bitmap = []
    for line in lines:
        bitmap.append(list(line))

    return enhancement_algo, ImageTile(bitmap)


def calculate_1(data: str, iters: int) -> int:
    enhancement_algo, img = decode_input(data)

    for _ in range(iters):
        img = img.enhance(enhancement_algo, inplace=False)

    return img.n_lit_pixels


if __name__ == '__main__':
    assert calculate_1(TEST_DATA, 2) == 35
    assert calculate_1(TEST_DATA, 50) == 3351

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answer_1 = calculate_1(data, 2)
    answer_2 = calculate_1(data, 50)

    print(f'{answer_1=}')
    print(f'{answer_2=}')
