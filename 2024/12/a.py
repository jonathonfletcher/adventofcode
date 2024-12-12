import collections
import itertools
import os

with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as ifp:
    input = list(map(lambda x: list(x.strip()), ifp.readlines()))


input_topology = dict()
for y, row in enumerate(input):
    for x, st in enumerate(row):
        input_topology[(x, y)] = st


neighbours = [(-1, 0), (0, -1), (1, 0), (0, 1)]
corners = {
    (-1, -1): {(-1, 0), (0, -1)},
    (-1, 1): {(-1, 0), (0, 1)},
    (1, -1): {(1, 0), (0, -1)},
    (1, 1): {(1, 0), (0, 1)},
}

plotcounter = itertools.count()
region_topology = collections.defaultdict(lambda: -1)
regions = collections.defaultdict(lambda: (-1, '', 0, 0, 0))
for sxy, st in input_topology.items():
    if region_topology[sxy] >= 0:
        continue

    pn = next(plotcounter)
    region_topology[sxy] = pn
    _, _, pa, pp, pc = regions[pn]

    to_check = [sxy]
    while len(to_check) > 0:
        xy = to_check.pop(0)
        pa += 1
        x, y = xy

        outsides = set()
        for dx, dy in neighbours:
            nxy = (x + dx, y + dy)
            nt = input_topology.get(nxy)
            if nt and nt == st:
                if region_topology[nxy] < 0:
                    to_check.append(nxy)
                    region_topology[nxy] = pn
            else:
                outsides.add((dx, dy))
                pp += 1

        insides = set(neighbours).difference(outsides)
        for c, e in corners.items():
            if outsides.intersection(e) == e:
                pc += 1
            if insides.intersection(e) == e:
                cx, cy = c
                exy = (x + cx, y + cy)
                nt = input_topology.get(exy)
                if nt != st:
                    pc += 1

    regions[pn] = (pn, st, pa, pp, pc)


a = 0
b = 0

for pn, pt, pa, pp, pc in regions.values():
    a += pa * pp
    b += pa * pc

print(f"{a=}")
print(f"{b=}")

pass
