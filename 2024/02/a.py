
def row_is_ok(row: list[int], sign: int, /):
    ok_vals = list(map(lambda x: sign * x, [1, 2, 3]))

    for i, iv in enumerate(row):
        if i < 1:
            continue
        pv = row[i - 1]
        if iv - pv not in ok_vals:
            print(f"0: {row=}, {ok_vals=}")
            return 0
    print(f"1: {row=}, {ok_vals=}")
    return 1


with open('02/input.txt') as ifp:
    input = list(map(lambda x: str(x).strip().split(), ifp.readlines()))

a = 0
b = 0
for row in input:
    row = list(map(lambda x: int(x), row))
    is_a = False
    is_b = False
    for v in [1, -1]:
        if row_is_ok(row, v):
            a += 1
            is_a = True
        else:
            for i in range(len(row)):
                rowc = row.copy()
                rowc.pop(i)
                if row_is_ok(rowc, v):
                    b += 1
                    is_b += 1
                    break
        if any([is_a, is_b]):
            break

print(a)
print(a + b)
