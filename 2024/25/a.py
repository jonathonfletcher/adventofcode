import itertools
import os

locks = list()
keys = list()
with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as ifp:
    for blob in ifp.read().split(os.linesep * 2):
        lines = blob.strip().split(os.linesep)
        islock = len(list(filter(lambda x: x == '#', list(lines[0])))) == len(lines[0])
        assert len(lines) == 7

        heights = [0] * len(lines[0])
        for y, row in enumerate(lines[1:-1]):
            for x, c in enumerate(row):
                if c == '#':
                    heights[x] += 1
        if islock:
            locks.append(heights)
        else:
            keys.append(heights)

print(len(keys))
print(len(locks))

a = 0
for k, l in itertools.product(keys, locks):
    c = list(zip(k, l))
    if all(list(map(lambda x: sum(x) <= 5, c))):
        a += 1
print(f"{a=}")
pass

