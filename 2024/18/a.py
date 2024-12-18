import collections
import heapq
import os
import sys

blocks = list()
gridsize = 71
blockcount = 1024
with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as ifp:
    for x, y in map(lambda x: list(map(int, x.strip().split(','))), ifp.readlines()):
        blocks.append((x, y))

spos = (0, 0)
epos = (gridsize - 1, gridsize - 1)


def printgrid(blocks, mm, /):
    for y in range(mm):
        line = ""
        for x in range(mm):
            if (x, y) in blocks:
                line += '#'
            else:
                line += '.'
        print(line)


def dijkstra(blocks, mm, spos, epos, /):
    q = list()
    distance = collections.defaultdict(lambda: sys.maxsize)
    bestscore = sys.maxsize
    bestpath = None

    heapq.heappush(q, [0, [spos], spos])
    while len(q) > 0:
        score, path, xy = heapq.heappop(q)

        if xy == epos:
            if score <= bestscore:
                bestscore = score
                bestpath = path
                break

        x, y = xy
        for (dx, dy) in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            nxy = x + dx, y + dy
            if not all([nxy[0] in range(mm), nxy[1] in range(mm), nxy not in blocks]):
                continue

            nscore = score + 1
            if nscore < distance[nxy]:
                distance[nxy] = nscore
                heapq.heappush(q, [nscore, path + [nxy], nxy])

    return bestscore, bestpath


def findstoppingblock(blocks, mm, spos, epos, /):
    li, ri = 0, len(blocks) - 1
    while li < ri:
        mi = (li + ri) // 2
        _, p = dijkstra(blocks[:mi], mm, spos, epos)
        if p:
            li = mi + 1
        else:
            ri = mi - 1
        pass
    return blocks[mi + 1]


# printgrid(blocks[:blockcount], gridsize)
ascore, apath = dijkstra(blocks[:blockcount], gridsize, spos, epos)
print(f"a={ascore}")
pass

bblock = findstoppingblock(blocks, gridsize, spos, epos)
print(f"b={','.join(map(str, list(bblock)))}")
pass
