import os
import itertools
import collections

with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as ifp:
    input = list(map(list, map(lambda x: x.strip(), ifp.readlines())))

pos = (0, 0)
obstacles = set()
maxx = 0
maxy = len(input)

for y, row in enumerate(input):
    maxx = len(row)
    for x, c in enumerate(row):
        if c == '#':
            obstacles.add((x, y))
        elif c == '^':
            pos = (x, y)


def path(obstacles, maxx, maxy, pos, /):
    direction = 0
    moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    x, y = pos
    locations = set()
    nrepeat = 0
    maxrepeat = 0
    while x in range(maxx) and y in range(maxy):

        maxrepeat = maxx * 2 if direction in [0, 2] else maxy * 2
        if nrepeat > maxrepeat:
            break

        if (x, y) in locations:
            nrepeat += 1
        else:
            nrepeat = 0

        locations.add((x, y))

        nx = x + moves[direction][0]
        ny = y + moves[direction][1]

        if (nx, ny) in obstacles:
            direction = (direction + 1) % len(moves)
        else:
            x = nx
            y = ny

    return locations, nrepeat > maxrepeat


apath, _ = path(obstacles, maxx, maxy, pos)
a = len(apath)
print(f"{a=}")

b = 0
for x, y in apath:
    if (x, y) in obstacles or (x, y) == pos:
        continue
    obstacles.add((x, y))
    _, stuck = path(obstacles, maxx, maxy, pos)
    if stuck:
        b += 1
    obstacles.discard((x, y))
print(f"{b=}")
