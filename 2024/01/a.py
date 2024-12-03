
with open('01/input.txt') as ifp:
    input = list(map(lambda x: str(x).strip().split(), ifp.readlines()))

l1 = sorted(list(map(lambda x: int(x[0]), input)), reverse=True)
l2 = sorted(list(map(lambda x: int(x[1]), input)), reverse=True)
assert len(l1) == len(l2)

a = 0
b = 0
for i in range(len(l1)):
    i1 = l1[i]
    i2 = l2[i]
    a += abs(i1 - i2)
    b += i1 * l2.count(i1)

print(a)
print(b)
