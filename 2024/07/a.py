import itertools
import os


with open(os.path.join(os.path.dirname(__file__), 'test.txt')) as ifp:
    input = list(map(lambda x: list(map(int, x.strip().replace(':', '').split())), ifp.readlines()))


def works(t, vals, ops, /):
    acc = vals[0]
    for vi, v in enumerate(ops):
        if v == '+':
            acc += vals[vi + 1]
        elif v == '*':
            acc *= vals[vi + 1]
        elif v == '|':
            acc = int(str(acc) + str(vals[vi + 1]))
    if acc == t:
        return True
    return False


a = 0
b = 0

for ri, row in enumerate(input):
    t, vals = row[0], row[1:]

    amatch = False
    aposops = sorted(['*+'] * (len(vals) - 1))
    for ops in map(list, itertools.product(*aposops)):
        if works(t, vals, ops):
            amatch = True
            break

    if amatch:
        a += t
        b += t
        continue

    bmatch = False
    bposops = sorted(['*+|'] * (len(vals) - 1))
    for ops in filter(lambda x: x.count('|') > 0, map(list, itertools.product(*bposops))):
        if works(t, vals, ops):
            bmatch = True
            break

    if bmatch:
        b += t
        continue

print(f"{a=}")
print(f"{b=}")

pass
