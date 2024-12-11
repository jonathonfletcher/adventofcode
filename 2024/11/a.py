import functools
import os

with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as ifp:
    input = list(map(lambda x: list(map(int, x.strip().split())), ifp.readlines()))


@functools.cache
def count(v, iterations, /):
    if iterations == 0:
        return 1
    if v == 0:
        return count(1, iterations - 1)
    elif len(str(v)) % 2 == 0:
        sv = str(v)
        nv1, nv2 = int(sv[:len(sv) // 2]), int(sv[len(sv) // 2:])
        return count(nv1, iterations - 1) + count(nv2, iterations - 1)
    else:
        return count(v * 2024, iterations - 1)


a = 0
b = 0

for v in input[0]:
    a += count(v, 25)
    b += count(v, 75)

print(f"{a=}")
print(f"{b=}")

pass
