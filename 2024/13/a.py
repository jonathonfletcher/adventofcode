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



def argh(ax, ay, bx, by, px, py):

    #  ax * na + bx * nb == px
    #  ay * na + by * nb == py
    #
    #  https://www.wolframalpha.com
    #  A1 * x + A2 * y = A3, B1 * x + B2 * y = B3, A1 > 0, A2 > 0, A3 > 0, B1 > 0, B2 > 0, B3 > 0
    #
    #  x = na
    #  y = nb
    #  A1 = ax
    #  A2 = bx
    #  A3 = px
    #  B1 = ay
    #  B2 = by
    #  B3 = py

    common_divisor = (bx * ay) - (ax * by)
    x = ((bx * py) - (px * by)) / common_divisor
    y = ((px * ay) - (ax * py)) / common_divisor

    if all([int(x) == x, int(y) == y]):
        return 3 * int(x) + int(y)

    return 0


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

    a += argh(ax, ay, bx, by, px, py)
    b += argh(ax, ay, bx, by, px + error, py + error)


print(f'{a=}')
print(f'{b=}')
pass
