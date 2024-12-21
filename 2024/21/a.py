import collections
import functools
import heapq
import itertools
import os
import sys

input = list()
with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as ifp:
    for line in map(str, map(lambda x: str(x).strip(), ifp.readlines())):
        if len(line) > 0:
            input.append(line)


KEYPAD = {
    '7': (0, 0), '8': (1, 0), '9': (2, 0),
    '4': (0, 1), '5': (1, 1), '6': (2, 1),
    '1': (0, 2), '2': (1, 2), '3': (2, 2),
    '0': (1, 3), 'A': (2, 3)
}


DIRPAD = {
    '^': (1, 0), 'A': (2, 0),
    '<': (0, 1), 'v': (1, 1), '>': (2, 1)
}


def make_dirpadpath(path, /):
    dmap = {
        'A': (0, 0),
        '>': (1, 0),
        '<': (-1, 0),
        '^': (0, -1),
        'v': (0, 1)
    }
    dmap = {v: k for k, v in dmap.items()}
    dpath = str()
    for (x0, y0), (x1, y1) in itertools.pairwise(path):
        dxy = (x1 - x0, y1 - y0)
        dpath += dmap[dxy]
    return dpath


@functools.cache
def dirpath_dijkstra(grid, spos, epos, /):
    q = list()
    distance = collections.defaultdict(lambda: sys.maxsize)
    # bestpaths = list()
    bestscore = sys.maxsize

    heapq.heappush(q, [0, [spos], spos, (0, 0)])
    while len(q) > 0:
        score, path, xy, dxy = heapq.heappop(q)

        if xy == epos:
            if score <= bestscore:
                bestscore = score
                # bestpaths.append(make_dirpadpath(path))
                yield make_dirpadpath(path)
            else:
                break

        x, y = xy
        for (dx, dy) in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            nxy = x + dx, y + dy
            if nxy not in grid:
                continue

            nscore = score + 1

            ndxy = (dx, dy)
            if ndxy != dxy:
                nscore += 1000

            if nscore <= distance[(nxy, ndxy)]:
                distance[(nxy, ndxy)] = nscore
                heapq.heappush(q, [nscore, path + [nxy], nxy, ndxy])

    # return bestpaths


@functools.cache
def dirpath_str_counter(line, n, /):
    if n == 0:
        return line

    r = ""
    global DIRPAD
    line = 'A' + line
    for skey, ekey in itertools.pairwise(line):
        shortest = None
        for dirpadpath in dirpath_dijkstra(DIRPAD.values(), DIRPAD[skey], DIRPAD[ekey]):
            pr = dirpath_str_counter(dirpadpath + 'A', n - 1)
            if shortest is None:
                shortest = pr
            elif len(pr) < len(shortest):
                shortest = pr
        if shortest is not None:
            r += shortest
    return r


@functools.cache
def dirpath_len_counter(line, n, /):
    if n == 0:
        return len(line)

    r = 0
    global DIRPAD
    line = 'A' + line
    for skey, ekey in itertools.pairwise(line):
        shortest = sys.maxsize
        for dirpadpath in dirpath_dijkstra(DIRPAD.values(), DIRPAD[skey], DIRPAD[ekey]):
            prlen = dirpath_len_counter(dirpadpath + 'A', n - 1)
            shortest = min(prlen, shortest)
        if shortest < sys.maxsize:
            r += shortest
    return r


def keypad_str_counter(line, n, /):
    r = ""
    global KEYPAD
    line = 'A' + line
    for skey, ekey in itertools.pairwise(line):
        shortest = None
        for dirpadpath in dirpath_dijkstra(KEYPAD.values(), KEYPAD[skey], KEYPAD[ekey]):
            pr = dirpath_str_counter(dirpadpath + 'A', n)
            if shortest is None:
                shortest = pr
            elif len(pr) < len(shortest):
                shortest = pr
        if shortest is not None:
            r += shortest
    return r


def keypad_len_counter(line, n, /):
    r = 0
    global KEYPAD
    line = 'A' + line
    for skey, ekey in itertools.pairwise(line):
        shortest = sys.maxsize
        for dirpadpath in dirpath_dijkstra(KEYPAD.values(), KEYPAD[skey], KEYPAD[ekey]):
            prlen = dirpath_len_counter(dirpadpath + 'A', n)
            shortest = min(prlen, shortest)
        if shortest < sys.maxsize:
            r += shortest
    return r


a = 0
for line in input:
    v = int(line[:-1])
    arstr = len(keypad_str_counter(line, 2))
    ar = keypad_len_counter(line, 2)
    assert ar == arstr
    a += ar * v
print(f"{a=}")

b = 0
for line in input:
    v = int(line[:-1])
    # brstr = len(keypad_str_counter(line, 25))
    br = keypad_len_counter(line, 25)
    b += br * v
print(f"{b=}")

pass
