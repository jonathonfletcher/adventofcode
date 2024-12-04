import os
import itertools
import collections

with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as ifp:
    input = list(map(list, map(lambda x: x.strip(), ifp.readlines())))


find_word = 'XMAS'


maxy = len(input)
maxx = 0
locations = collections.defaultdict(set)
for yi, row in enumerate(input):
    maxx = max(maxx, len(row))
    for xi, c in enumerate(row):
        if c in find_word:
            locations[c].add((xi, yi))

directions = set(itertools.product([-1, 0, 1], [-1, 0, 1]))
directions.discard((0, 0))


a_sum = 0
for dx, dy in directions:

    startloc = None
    for ci, c in enumerate(list(find_word)):
        if ci == 0:
            startloc = locations[c]
        else:
            newloc = set()
            for lx, ly in startloc:
                nx = lx + dx
                ny = ly + dy
                if (nx, ny) in locations[c]:
                    newloc.add((nx, ny))
            startloc = newloc
            pass
        if len(startloc) == 0:
            break
    pass
    a_sum += len(startloc)


b_sum = 0
m_locations = locations['M']
s_locations = locations['S']
for x, y in locations['A']:

    """
        M.M
        S.S

        S.M
        S.M

        S.S
        M.M

        M.S
        M.S
    """

    if any([
        all([
            (x - 1, y - 1) in m_locations, (x + 1, y - 1) in m_locations,
            (x - 1, y + 1) in s_locations, (x + 1, y + 1) in s_locations
        ]),
        all([
            (x - 1, y - 1) in s_locations, (x + 1, y - 1) in m_locations,
            (x - 1, y + 1) in s_locations, (x + 1, y + 1) in m_locations
        ]),
        all([
            (x - 1, y - 1) in s_locations, (x + 1, y - 1) in s_locations,
            (x - 1, y + 1) in m_locations, (x + 1, y + 1) in m_locations
        ]),
        all([
            (x - 1, y - 1) in m_locations, (x + 1, y - 1) in s_locations,
            (x - 1, y + 1) in m_locations, (x + 1, y + 1) in s_locations
        ]),
    ]):
        b_sum += 1

print(f"{a_sum=}")
print(f"{b_sum=}")
