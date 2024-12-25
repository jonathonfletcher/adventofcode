import itertools
import os

inputs = dict()
outputs = set()
gates = list()
with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as ifp:
    s1, s2 = ifp.read().split(os.linesep * 2)
    for ts in map(lambda x: str(x).strip(), s1.split(os.linesep)):
        sym, val = ts.split(':')
        inputs[sym] = int(val)
        pass
    for carrybits in map(lambda x: str(x).strip(), s2.split(os.linesep)):
        if len(carrybits) > 0:
            sym1, op, sym2, _, sym3 = carrybits.split()
            pass
            ss = sorted([sym1, sym2])
            gates.append((ss[0], ss[1], op, sym3))
            if sym3[0] == 'z':
                outputs.add(sym3)


# def ha(x, y):
#     return {
#         (0, 0): (0, 0),
#         (0, 1): (1, 0),
#         (1, 0): (1, 0),
#         (1, 1): (0, 1)
#     }.get((x, y))


# def fa(x, y, c):
#     return {
#         (0, 0, 0): (0, 0),
#         (0, 0, 1): (1, 0),
#         (0, 1, 0): (1, 0),
#         (0, 1, 1): (0, 1),
#         (1, 0, 0): (1, 0),
#         (1, 0, 1): (0, 1),
#         (1, 1, 0): (0, 1),
#         (1, 1, 1): (1, 1)
#     }.get((x, y, c))


def evaluate(gates: list, inputs: dict, /) -> dict:
    ok = True
    while len(gates) > 0:
        newgates = list()
        allsyms = frozenset(inputs.keys())
        for sym1, sym2, op, sym3 in gates:
            if sym1 in allsyms and sym2 in allsyms:
                if op == 'AND':
                    inputs[sym3] = inputs[sym1] & inputs[sym2]
                elif op == 'OR':
                    inputs[sym3] = inputs[sym1] | inputs[sym2]
                elif op == 'XOR':
                    inputs[sym3] = inputs[sym1] ^ inputs[sym2]
            else:
                newgates.append((sym1, sym2, op, sym3))
        if gates == newgates:
            gates = list()
            ok = False
        else:
            gates = newgates
    return ok, inputs


def getint(inputs, sym, /):
    v = 0
    for syminput in sorted(list(filter(lambda x: x[0] == sym, inputs))):
        v |= inputs[syminput] << int(syminput[1:])
    return v


aok, ainputs = evaluate(gates.copy(), inputs.copy())
a = getint(ainputs, 'z')
print(f"{a=}")
pass


# https://www.reddit.com/r/adventofcode/comments/1hla5ql/2024_day_24_part_2_a_guide_on_the_idea_behind_the/

def badoutputs(inputs: dict, outputs: dict, gates: list, /) -> set:
    zlist = sorted(list(map(lambda x: int(x[1:]), outputs)), reverse=True)
    highz = f"z{zlist[0]:2d}"
    r = set()
    for sym1, sym2, op, sym3 in gates:

        if op != 'XOR' and sym3 != highz and sym3[0] == 'z':
            r.add(sym3)
            continue

        if op == 'XOR' and all([sym1[0] not in {'x', 'y', 'z'}, sym2[0] not in {'x', 'y', 'z'}, sym3[0] not in {'x', 'y', 'z'}]):
            r.add(sym3)
            continue

    return r


def swapoutput(gates: list, a: str, b: str):
    newgates = list()
    for sym1, sym2, op, sym3 in gates:
        if sym3 == a:
            newgates.append((sym1, sym2, op, b))
        elif sym3 == b:
            newgates.append((sym1, sym2, op, a))
        else:
            newgates.append((sym1, sym2, op, sym3))
    return newgates


real_x = getint(inputs, 'x')
real_y = getint(inputs, 'y')
want_z = real_x + real_y

bgates = gates.copy()
bad_outputs = badoutputs(inputs, outputs, bgates)

# Find the 3 pairs from badoutpus

keep_maxz = -1
keep_swaps = None
for sa1, sb1 in itertools.combinations(bad_outputs, 2):
    for sa2, sb2 in itertools.combinations(bad_outputs.difference({sa1, sb1}), 2):
        for sa3, sb3 in itertools.combinations(bad_outputs.difference({sa1, sb1, sa2, sb2}), 2):
            tgates = swapoutput(bgates, sa1, sb1)
            tgates = swapoutput(tgates, sa2, sb2)
            tgates = swapoutput(tgates, sa3, sb3)

            tok, tinputs = evaluate(tgates.copy(), inputs.copy())
            if not tok:
                continue

            tz = getint(tinputs, 'z')
            txor = want_z ^ tz

            # print(bin(xor))
            # print([(sa1, sb1), (sa2, sb2), (sa3, sb3)])

            for z in range(64):
                if txor & (1 << z) == (1 << z):
                    print(z)
                    break
            if z > keep_maxz:
                keep_maxz = z
                keep_swaps = [(sa1, sb1), (sa2, sb2), (sa3, sb3)]
pass



bgates = gates.copy()
for sa, sb in keep_swaps:
    bgates = swapoutput(bgates, sa, sb)
tok, tinputs = evaluate(bgates.copy(), inputs.copy())
pass

# look at the adder for input / output number keep_maxz
pass


# swap the last pair
more_keep_swaps = [('rvf', 'tpc')]
for sa, sb in more_keep_swaps:
    bgates = swapoutput(bgates, sa, sb)
tok, tinputs = evaluate(bgates.copy(), inputs.copy())


# confirm the xor is 0

tz = getint(tinputs, 'z')
txor = want_z ^ tz
assert txor == 0

all_swaps = keep_swaps + more_keep_swaps
b = set()
for swap in all_swaps:
    b.update(set(swap))
print(f"b={','.join(sorted(b))}")
pass
