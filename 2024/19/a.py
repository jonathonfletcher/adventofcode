import os

towels = set()
patterns = list()
with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as ifp:
    ts, cs = ifp.read().split(os.linesep * 2)
    for ts in map(lambda x: str(x).strip(), ts.split(',')):
        # print(f"|{t}|")
        towels.add(ts)
    for c in map(lambda x: str(x).strip(), cs.split(os.linesep)):
        if len(c) > 0:
            # print(f"|{c}|")
            patterns.append(c)


CACHE = dict()


def can(t, cs, /):
    global CACHE
    cn = CACHE.get(t)
    if cn is None:
        if len(t) == 0:
            cn = 1
        else:
            cn = 0
            for c in cs:
                if t.find(c) == 0:
                    cn += can(t[len(c):], cs)
        CACHE[t] = cn
    return cn


a = 0
b = 0

for p in patterns:
    n = can(p, towels)
    if n > 0:
        # print(os.linesep)
        # print(f"{t} ({n})")
        a += 1
        b += n

print(f"{a=}")
print(f"{b=}")

pass
