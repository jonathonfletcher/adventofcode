
import os

inputs = dict()
gates = list()
with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as ifp:
    s1, s2 = ifp.read().split(os.linesep * 2)
    for ts in map(lambda x: str(x).strip(), s1.split(os.linesep)):
        sym, val = ts.split(':')
        inputs[sym] = int(val)
        # print(f"|{t}|")
        # towels.add(ts)
        pass
    for c in map(lambda x: str(x).strip(), s2.split(os.linesep)):
        if len(c) > 0:
            sym1, op, sym2, _, sym3 = c.split()
            pass
            # print(f"|{c}|")
            # patterns.append(c)
            gates.append((sym1, sym2, op, sym3))


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
    gates = newgates

zsyms = sorted(list(filter(lambda x: x[0] == 'z', inputs)))

a = 0
for zs in zsyms:
    a |= inputs[zs] << int(zs[1:])
print(f"{a=}")
pass
