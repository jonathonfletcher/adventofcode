

def do_explode(l):
    d = -1
    for i in range(len(l)):
        e = l[i]
        # print(f'  {i:4} {e} {d:4}')
        if e == '[':
            d += 1
        elif e == ']':
            d -= 1
        elif e != ',' and d == 4:
            for li in range(i-1, -1, -1):
                if l[li] not in ['[', ']', ',']:
                    break
            if li > 0:
                l[li] += l[i]
            for ri in range(i+4, len(l)):
                if l[ri] not in ['[', ']', ',']:
                    break
            if ri < len(l)-1:
                l[ri] += l[i+2]
            return l[:i-1] + [0] + l[i+4:]
    return None


def do_split(l):
    for i in range(len(l)):
        e = l[i]
        if e not in ['[', ']', ',']:
            if e > 9:
                le = e // 2
                re = e - le
                return l[:i] + ['[', le, ',', re, ']'] + l[i+1:]
    return None


def do_reduce(l):
    while True:
        # print(''.join(map(lambda x: str(x), l)))
        el = do_explode(l)
        if not el:
            el = do_split(l)
            if not el:
                return l
        l = el


def do_add(lhs, rhs):
    return ['['] + lhs + [','] + rhs + [']']


def do_mag(l):
    if len(l) > 1:
        for i in range(len(l)):
            if l[i] not in [ '[', ']',',']:
                lhs = l[i]
                rhs = l[i+2]
                if rhs not in ['[', ']', ',']:
                    ne = 3 * lhs + 2 * rhs
                    ll = l[:i-1]
                    rl = l[i+4:]
                    return do_mag(ll + [ ne ] + rl)
    return l.pop()


def string_to_list(s):
    l = list()
    for e in s:
        if e in ['[', ']', ',']:
            l.append(e)
        elif e >= '0' and e <= '9':
            l.append(int(e))
    return l


parts = list()
with open('part1.txt') as ifp:
    pl = None
    for ins in [l.strip() for l in ifp.readlines()]:
        parts.append(ins)
        inl = string_to_list(ins)
        if pl is not None:
            inl = do_add(pl, inl)
        pl = do_reduce(inl)
    print(''.join(map(lambda x: str(x), pl)))
    print(do_mag(pl))


max_l = None
max_r = None
max_m = 0

for li in range(len(parts)):
    for ri in range(len(parts)):
        if li == ri:
            continue
    
        ls = string_to_list(parts[li])
        rs = string_to_list(parts[ri])

        m = do_mag(do_reduce(do_add(ls, rs)))
        if m > max_m:
            max_l = parts[li]
            max_r = parts[ri]
            max_m = m
        m = do_mag(do_reduce(do_add(rs, ls)))
        if m > max_m:
            max_l = parts[ri]
            max_r = parts[li]
            max_m = m

print(f'{max_l}')
print(f'{max_r}')
print(f'{max_m}')
