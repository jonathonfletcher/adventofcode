import collections
import itertools
import os
import re

robots = list()
with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as ifp:
    e = re.compile(r'[pv]=(-?\d+),(-?\d+)', re.VERBOSE)
    for pterm, vterm in map(lambda x: str(x).split(), map(lambda x: str(x).strip(), ifp.readlines())):
        pm = e.search(pterm)
        p = tuple(map(int, pm.groups()))
        vm = e.match(vterm)
        v = tuple(map(int, vm.groups()))
        robots.append((p, v))


def quarters(sx, sy, /):
    qx = sx // 2
    qy = sy // 2

    quarters = list()
    for qdx, qdy in itertools.product(range(2), range(2)):

        x0 = qdx * (qx + 1)
        x1 = x0 + qx

        y0 = qdy * (qy + 1)
        y1 = y0 + qy

        quarters.append(((x0, x1), (y0, y1)))
    return quarters


def locations(space, robots, seconds, /):
    sx, sy = space
    nrobots = collections.defaultdict(int)
    for (px, py), (dx, dy) in robots:
        nx = (px + (dx * seconds)) % sx
        ny = (py + (dy * seconds)) % sy
        nrobots[(nx, ny)] += 1
    return nrobots


def parta(space, robots, seconds, /):
    nrobots = locations(space, robots, seconds)

    a = 1
    for (x0, x1), (y0, y1) in quarters(*space):
        qsum = 0
        for (rx, ry), rc in nrobots.items():
            if all([
                rx >= x0, rx < x1,
                ry >= y0, ry < y1
            ]):
                qsum += rc
        a *= qsum

    return a


def print_space(space, points, /):
    sx, sy = space
    for y in range(sy):
        line = ""
        for x in range(sx):
            if (x, y) in points:
                line += '#'
            else:
                line += ' '
        print(line)
    pass


def isbox(space, points):
    sx, sy = space
    ydict = collections.defaultdict(int)
    xdict = collections.defaultdict(int)

    for x, y in itertools.product(range(sx), range(sy)):
        if (x, y) in points:
            ydict[y] += 1
            xdict[x] += 1

    maxx = max(xdict.values())
    nmaxx = len(list(filter(lambda x: xdict[x] == maxx, xdict.keys())))
    maxy = max(ydict.values())
    nmaxy = len(list(filter(lambda y: ydict[y] == maxy, ydict.keys())))

    return all([maxx == maxy, nmaxx == nmaxy, maxx > 30, nmaxx == 2])


def partb(space, robots, /):
    for seconds in itertools.count(1):
        nrobots = locations(space, robots, seconds)
        if isbox(space, nrobots.keys()):
            print_space(space, nrobots.keys())
            return seconds
    return -1


space = (101, 103)
# space = (11, 7)

a = parta(space, robots, 100)
print(f"{a=}")

b = partb(space, robots)
print(f"{b=}")

pass
