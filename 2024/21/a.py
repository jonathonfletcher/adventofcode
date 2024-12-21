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


def dirpath_dijkstra(grid, spos, epos, /):
    q = list()
    distance = collections.defaultdict(lambda: sys.maxsize)
    bestpaths = list()
    bestscore = sys.maxsize

    dirmap = {
        '>': (1, 0),
        '<': (-1, 0),
        '^': (0, -1),
        'v': (0, 1)
    }

    heapq.heappush(q, [0, "", spos, (0, 0)])
    while len(q) > 0:
        score, path, xy, dxy = heapq.heappop(q)

        if xy == epos:
            if score <= bestscore:
                bestscore = score
                bestpaths.append(path)
            else:
                break

        x, y = xy
        for v, (dx, dy) in dirmap.items():
            nxy = x + dx, y + dy
            if nxy not in grid:
                continue

            nscore = score + 1

            ndxy = (dx, dy)
            if ndxy != dxy:
                nscore += 1000

            if nscore <= distance[(nxy, ndxy)]:
                distance[(nxy, ndxy)] = nscore
                heapq.heappush(q, [nscore, path + v, nxy, ndxy])

    return bestpaths


@functools.cache
def dirpath_len_counter(line, n, /):
    if n == 0:
        return len(line)

    r = 0
    global DIRPAD
    for skey, ekey in itertools.pairwise('A' + line):
        shortest = sys.maxsize
        for dirpadpath in dirpath_dijkstra(DIRPAD.values(), DIRPAD[skey], DIRPAD[ekey]):
            prlen = dirpath_len_counter(dirpadpath + 'A', n - 1)
            shortest = min(prlen, shortest)
        if shortest < sys.maxsize:
            r += shortest
    return r


def keypad_len_counter(line, n, /):

    r = 0
    global KEYPAD
    for skey, ekey in itertools.pairwise('A' + line):
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
    ar = keypad_len_counter(line, 2)
    a += ar * v
print(f"{a=}")

b = 0
for line in input:
    v = int(line[:-1])
    br = keypad_len_counter(line, 25)
    b += br * v
print(f"{b=}")

pass
