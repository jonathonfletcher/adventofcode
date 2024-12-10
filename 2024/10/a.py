import collections
import itertools
import os


with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as ifp:
    inputs = list(map(lambda x: list(map(int, list(x.strip()))), ifp.readlines()))

heights = collections.defaultdict(set)

for y, row in enumerate(inputs):
    for x, h in enumerate(row):
        heights[int(h)].add((x, y))


def walkup(heights, h, p, /):
    r = set()
    if h < 9:
        x, y = p
        ch = h + 1
        for dx, dy in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
            cp = (x + dx, y + dy)
            if cp in heights[ch]:
                r.update(walkup(heights, ch, cp))
    else:
        if p in heights[h]:
            r.add(p)
    return r


def countup(heights, h, p, /):
    r = 0
    if h < 9:
        x, y = p
        ch = h + 1
        for dx, dy in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
            cp = (x + dx, y + dy)
            if cp in heights[ch]:
                r += countup(heights, ch, cp)
    else:
        r = int(p in heights[h])
    return r


a = 0
b = 0
h = 0
for p in heights[h]:
    tt = walkup(heights, h, p)
    nr = countup(heights, h, p)
    a += len(tt)
    b += nr


print(f"{a=}")
print(f"{b=}")
pass