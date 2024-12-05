import os

por = set()
updates = list()
with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as ifp:
    state = 0
    for line in map(lambda x: x.strip(), ifp.readlines()):
        if len(line) == 0:
            state += 1
        elif state == 0:
            por.add(tuple(map(int, line.split('|'))))
        elif state == 1:
            updates.append(list(map(int, line.split(','))))


def inorder(por: set, u: list) -> bool:
    for oi in range(len(u)):
        for ii in range(oi + 1, len(u)):
            if (u[oi], u[ii]) in por and oi > ii:
                return False
            elif (u[ii], u[oi]) in por and oi < ii:
                return False
    return True


def reorder(por: set, u: list) -> list:
    if inorder(por, u):
        return u

    for oi in range(len(u) - 1, 0, -1):
        for ii in range(oi - 1, -1, -1):
            if (u[oi], u[ii]) in por:
                tu = u.copy()
                tu[oi] = u[ii]
                tu[ii] = u[oi]
                return reorder(por, tu)
    return u


a_sum = 0
b_sum = 0
for u in updates:
    if inorder(por, u):
        a_sum += u[len(u) // 2]
    else:
        fu = reorder(por, u)
        b_sum += fu[len(fu) // 2]

print(f"{a_sum=}")
print(f"{b_sum=}")
pass
