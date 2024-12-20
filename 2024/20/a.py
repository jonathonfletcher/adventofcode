import collections
import heapq
import os
import sys

grid = dict()
spos = None
epos = None
with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as ifp:
    for y, row in enumerate(ifp.read().split(os.linesep)):
        for x, c in enumerate(row):
            grid[(x, y)] = c
            if c == 'S':
                spos = (x, y)
            elif c == 'E':
                epos = (x, y)


def printgrid(grid, path, /):
    maxx = 1 + max(map(lambda xy: xy[0], grid.keys()))
    maxy = 1 + max(map(lambda xy: xy[1], grid.keys()))
    for y in range(maxy):
        line = ""
        for x in range(maxx):
            if (x, y) in path:
                line += 'o'
            else:
                line += grid[(x, y)]
        print(line)


def dijkstra(grid, spos, epos, /, cxy=None):
    q = list()
    distance = collections.defaultdict(lambda: sys.maxsize)

    heapq.heappush(q, [0, [spos], spos])
    while len(q) > 0:
        score, path, xy = heapq.heappop(q)

        if xy == epos:
            return score, path

        x, y = xy
        dm = 1
        if cxy == xy:
            dm = 2
        for (dx, dy) in [[dm * 1, 0], [dm * -1, 0], [0, dm * 1], [0, dm * -1]]:
            nxy = x + dx, y + dy
            if nxy not in grid:
                continue
            if grid[nxy] == '#':
                continue

            nscore = score + dm * 1
            if nscore < distance[nxy]:
                distance[nxy] = nscore
                heapq.heappush(q, [nscore, path + [nxy], nxy])

    return sys.maxsize, list()


# printgrid(grid, list())
_, track = dijkstra(grid, spos, epos)


trackdict = dict()
for pi, pxy in enumerate(track):
    trackdict[pxy] = pi


a = 0
b = 0
maxjumps = 20
for pi, (px, py) in enumerate(track):

    if all([pi > 0, pi % 100 == 0]):
        print(f"{100. * pi / len(track):2.0f}%")

    mindy = -maxjumps
    maxdy = maxjumps + 1
    for dy in range(mindy, maxdy):
        ady = abs(dy)

        mindx = -maxjumps + ady
        maxdx = maxjumps + 1 - ady
        for dx in range(mindx, maxdx):
            adx = abs(dx)

            nxy = px + dx, py + dy
            ni = trackdict.get(nxy, 0)
            if ni <= pi:
                continue

            d = ady + adx
            s = ni - pi - d
            if s < 100:
                continue

            b += 1
            if d == 2:
                a += 1

print(f"{a=}")
print(f"{b=}")
pass
