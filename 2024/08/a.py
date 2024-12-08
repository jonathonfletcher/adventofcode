import os
import collections
import itertools

with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as ifp:
    input = list(map(list, map(lambda x: x.strip(), ifp.readlines())))

maxx = 0
maxy = len(input)
antennas = collections.defaultdict(set)
antinodes = set()
bantinodes = set()

for y, row in enumerate(input):
    maxx = len(row)
    for x, c in enumerate(row):
        if c in ['.', '#']:
            continue
        antennas[c].add((x, y))

for c, l in antennas.items():
    for a1, a2 in itertools.permutations(l, 2):
        dx, dy = a2[0] - a1[0], a2[1] - a1[1]

        nx, ny = a2
        nx, ny = nx + dx, ny + dy
        if nx in range(maxx) and ny in range(maxy):
            antinodes.add((nx, ny))

        nx, ny = a2
        while nx in range(maxx) and ny in range(maxy):
            bantinodes.add((nx, ny))
            nx, ny = nx + dx, ny + dy


a = len(antinodes)
print(f"{a=}")

b = len(bantinodes)
print(f"{b=}")

pass