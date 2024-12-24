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


def combinations(input: dict, length: int, /) -> list:
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
            if k not in found:
                found.add(k)
    return list(found)


def findlongest(input: dict, ili: int, iri: int, /):
    li, ri = ili, iri
    while li < ri:
        mi = (li + ri) // 2
        print(f"{mi}")
        f = combinations(input, mi)
        print(f"{mi} -> {len(f)}")
        if len(f) > 0:
            li = mi + 1
        else:
            ri = mi - 1
        pass
    return mi - 1


a = 0
af = combinations(input, 3)
print(f"{len(af)=}")
for c in af:
    for i in c:
        if i[0] == 't':
            a += 1
            break
print(f"{a=}")


# # longest = findlongest(input, 3, 15)
# counters = collections.defaultdict(int)
# for k in input.keys():
#     for v in input.values():
#         if k in v:
#             counters[k] += 1
# maxcounter = max(counters.values())


# f = combinations(input, maxcounter)
# if len(f) == 1:
#     b = ','.join(sorted(f[0]))

# print(f"{b=}")

pass
