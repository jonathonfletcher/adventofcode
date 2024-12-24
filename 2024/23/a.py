import collections
import itertools
import os

input = collections.defaultdict(set)
with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as ifp:
    for line in map(str, map(lambda x: str(x).strip(), ifp.readlines())):
        if len(line) > 0:
            a, b = line.split('-')
            input[a].add(b)
            input[b].add(a)

input = {k: frozenset(v.union({k})) for k, v in input.items()}


def combinations(input: dict, length: int, /) -> frozenset:
    found = set()
    for k in itertools.combinations(input.keys(), length):
        ok = True
        for kk in itertools.combinations(k, length - 1):
            k0 = set(k) - set(kk)
            for ik in kk:
                if not k0.issubset(input[ik]):
                    ok = False
                    break
            if not ok:
                break
        if ok:
            k = frozenset(k)
            if k not in found:
                found.add(k)
    return frozenset(found)


def findlongest(sv: frozenset, ss: frozenset, ds: frozenset, prefix: frozenset) -> tuple[int, frozenset]:

    if len(prefix) > len(sv):
        return -1, prefix

    ml, mp = len(prefix), prefix
    for ssk in frozenset(ss.difference(ds).difference(prefix)):
        newprefix = frozenset(prefix).union({ssk})
        newsv = frozenset({svx for svx in sv if set(newprefix).issubset(svx)})

        rl, rp = findlongest(newsv, ss, ds, newprefix)
        if rl > ml:
            ml, mp = rl, rp
        else:
            ds = frozenset(ds.union({ssk}))

    return ml, mp


a = 0
for c in combinations(input, 3):
    for i in c:
        if i[0] == 't':
            a += 1
            break
print(f"{a=}")


b = frozenset()
for k, v in input.items():
    sv = frozenset({svx for svx in input.values() if k in svx})
    rl, rp = findlongest(sv, v, set(), {k})
    if len(rp) > len(b):
        b = frozenset(rp)
print(f"b={','.join(sorted(b))}")

pass
