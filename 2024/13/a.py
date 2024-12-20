import functools
import itertools
import os
import re

input = list()
with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as ifp:
    machine = dict()
    bre = re.compile(r'Button ([AB]): X\+(\d+), Y\+(\d+)')
    pre = re.compile(r'Prize: X=(\d+), Y=(\d+)')
    for line in map(lambda x: str(x).strip(), ifp.readlines()):
        bm = bre.match(line)
        pm = pre.match(line)
        if bm:
            mg = bm.groups()
            machine[mg[0]] = (int(mg[1]), int(mg[2]))
        elif pm:
            mg = pm.groups()
            machine['P'] = (int(mg[0]), int(mg[1]))
        elif len(line) == 0:
            input.append(machine)
            machine = dict()
    input.append(machine)


def paper(ax, ay, bx, by, px, py):
    nb = ((ax * py) - (ay * px)) / ((ax * by) - (ay * bx))
    if int(nb) != nb:
        return 0

    na = (px - (bx * nb)) / ax
    if int(na) != na:
        return 0

    return 3 * int(na) + int(nb)


# @functools.cache
# def xyf(ax, ay, bx, by, px, py, na, nb, /):
#     return all([
#         ax * na + bx * nb == px,
#         ay * na + by * nb == py,
#     ])


a = 0
b = 0
error = 10000000000000
for machine in input:
    button_a = machine['A']
    button_b = machine['B']
    prize = machine['P']

    ax, bx, px = button_a[0], button_b[0], prize[0]
    ay, by, py = button_a[1], button_b[1], prize[1]

    # cost = -1
    # machinef = functools.partial(xyf, ax, ay, bx, by, px, py)
    # for na, nb in itertools.product(range(100), range(100)):
    #     if machinef(na, nb):
    #         cost = na * 3 + nb
    #         break
    # cost = max(0, cost)

    a += paper(ax, ay, bx, by, px, py)
    b += paper(ax, ay, bx, by, px + error, py + error)


print(f'{a=}')
print(f'{b=}')
pass
