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


def make_distances(maxjumps, /):
    distances = collections.defaultdict(set)
    mindy = -maxjumps
    maxdy = maxjumps + 1
    for dy in range(mindy, maxdy):
        ady = abs(dy)

        mindx = mindy + ady
        maxdx = maxdy - ady
        for dx in range(mindx, maxdx):
            adx = abs(dx)
            if ady + adx > 1:
                distances[ady + adx].add((dx, dy))

    return distances


def valid_xy(dxy, pxy, trackdict, /):
    px, py = pxy
    pi = trackdict.get(pxy, 0)
    for (dx, dy) in dxy:
        nxy = px + dx, py + dy
        ni = trackdict.get(nxy, 0)
        if ni <= pi:
            continue
        yield ni, nxy


# printgrid(grid, list())
_, track = dijkstra(grid, spos, epos)

trackdict = dict()
for pi, pxy in enumerate(track):
    trackdict[pxy] = pi


a = 0
b = 0
maxjumps = 20
distances = make_distances(maxjumps)

for d in sorted(distances.keys()):

    for pi, pxy in enumerate(track):

        for ni, nxy in valid_xy(distances[d], pxy, trackdict):

            s = ni - pi - d
            if s < 100:
                continue

            b += 1
            if d == 2:
                a += 1

    if d == 2:
        print(f"{a=}")

print(f"{b=}")
pass
