import collections
import os
import heapq
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


def nrotations(fxy, txy):
    rcount = 0
    while fxy != txy:
        x, y = fxy
        fxy = -y, x
        rcount += 1
    if rcount == 3:
        rcount = 1
    return rcount


def dijkstra(grid, spos, epos, /):
    q = list()
    distance = collections.defaultdict(lambda: sys.maxsize)
    bestscore = sys.maxsize
    allxy = set()

    heapq.heappush(q, [0, [spos], spos, (1, 0)])
    while len(q) > 0:
        score, spath, xy, dir = heapq.heappop(q)

        if xy == epos:
            if score <= bestscore:
                bestscore = score
                allxy.update(spath)
                pass

        x, y = xy
        for (dx, dy) in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            nxy = x + dx, y + dy
            if grid[nxy] == '#':
                continue

            pt = nrotations(dir, (dx, dy))
            nscore = score + pt * 1000 + 1
            if nscore <= distance[(nxy, (dx, dy))]:
                distance[(nxy, (dx, dy))] = nscore
                heapq.heappush(q, [nscore, spath + [nxy], nxy, (dx, dy)])

    return bestscore, len(allxy)


# printgrid(grid, list())
score, count = dijkstra(grid, spos, epos)

a = score
print(f"{a=}")

b = count
print(f"{b=}")

pass
