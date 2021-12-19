

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
            # print(l[i:i+3])
            for li in range(i-1, -1, -1):
                if l[li] not in ['[', ']', ',']:
                    break
            if li > 0:
                le = l[li]
                # print(f'l {li:4} {le} {e}')
                l[li] += l[i]
            for ri in range(i+4, len(l)):
                if l[ri] not in ['[', ']', ',']:
                    break
            if ri < len(l)-1:
                re = l[ri]
                # print(f'l {ri:4} {re} {e}')
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
    print()    
    while True:
        print(''.join(map(lambda x: str(x), l)))
        el = do_explode(l)
        if not el:
            el = do_split(l)
            if not el:
                return l
        l = el


def do_add(lhs, rhs):
    return ['['] + lhs + [','] + rhs + [']']


def do_mag(l):
    print(''.join(map(lambda x: str(x), l)))
    if len(l) > 1:
        for i in range(len(l)):
            if l[i] not in [ '[', ']',',']:
                lhs = l[i]
                rhs = l[i+2]
                if rhs not in ['[', ']', ',']:
                    print(f'{i:4}/{len(l)} {lhs} {rhs}')
                    ne = 3 * lhs + 2 * rhs

                    ll = l[:i-1]
                    rl = l[i+4:]
                    # print(f'{type(ll)} {ll}')
                    # print(f'{type(ne)} {ne}')
                    # print(f'{type(rl)} {rl}')
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


with open('part0.txt') as ifp:
    pl = None
    for ins in [l.strip() for l in ifp.readlines()]:
        inl = string_to_list(ins)
        if pl is not None:
            inl = do_add(pl, inl)
        pl = do_reduce(inl)
    print(''.join(map(lambda x: str(x), pl)))
    print(do_mag(pl))


