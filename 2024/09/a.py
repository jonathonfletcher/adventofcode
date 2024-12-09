import os

with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as ifp:
    input = map(list, map(lambda x: x.strip(), ifp.readlines()))


def ldisk(disk, /) -> list[int]:
    l = []
    for fileno, length in disk:
        l.append([fileno] * length)
    return sum(l, [])


def asmoosh(listdisk: list, /):
    lhsi = 0
    rhsi = len(listdisk)
    while lhsi < rhsi:
        for li in range(lhsi, rhsi):
            if listdisk[li] < 0:
                break
        for ri in range(rhsi - 1, li - 1, -1):
            if listdisk[ri] >= 0:
                break
        if ri <= li:
            return listdisk

        listdisk[li] = listdisk[ri]
        listdisk[ri] = -1

        lhsi = li + 1
        rhsi = ri

    return listdisk


def bsmoosh(listdisk: list, /):
    freelist = list()
    filelist = list()
    cfn = -1
    cli = 0
    for i in range(len(listdisk)):
        if i == 0:
            cli = i
            cfn = listdisk[i]
        elif cfn != listdisk[i]:
            if cfn < 0:
                freelist.append((cfn, i - cli, cli))
            else:
                filelist.append((cfn, i - cli, cli))
            cli = i
            cfn = listdisk[i]
    if cli > 0:
        if cfn < 0:
            freelist.append((cfn, 1 + (i - cli), cli))
        else:
            filelist.append((cfn, 1 + (i - cli), cli))

    for file in reversed(filelist):
        _, file_len, file_start = file
        if file_len <= 0:
            continue

        for i, free in enumerate(freelist):
            _, free_len, free_start = free

            if free_start >= file_start:
                break

            if free_len < file_len:
                continue

            for ii in range(file_len):
                listdisk[free_start + ii] = listdisk[file_start + ii]
                listdisk[file_start + ii] = -1
            freelist[i] = (-1, free_len - file_len, free_start + file_len)
            break
    return listdisk




row = list(map(int, next(input)))
tupledisk = list()
fileno = 0
for li, l in enumerate(row):
    if li % 2 == 0:
        tupledisk.append((fileno, l))
        fileno += 1
    else:
        tupledisk.append((-1, l))


listdisk = ldisk(tupledisk)
# print(f"{listdisk}")


a = 0
adisk = asmoosh(listdisk.copy())
for i, v in enumerate(adisk):
    if v < 0:
        continue
    a += i * v
print(f"{a=}")

b = 0
bdisk = bsmoosh(listdisk.copy())
for i, v in enumerate(bdisk):
    if v < 0:
        continue
    b += i * v
print(f"{b=}")

pass
