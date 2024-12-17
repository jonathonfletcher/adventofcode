import copy
import dataclasses
import os
import re


@dataclasses.dataclass(frozen=True)
class mstate:
    a: int = 0
    b: int = 0
    c: int = 0
    ip: int = 0
    halt: bool = False


program = None
s = None
with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as ifp:
    registers, program = ifp.read().split(os.linesep * 2)
    regdict = dict()
    for r in map(lambda x: str(x).strip(), registers.split(os.linesep)):
        print(f"|{r}|")
        e = re.compile(r'^Register ([ABC]{1}): (\_?\d+)$')
        m = e.match(r)
        if not m:
            continue
        register, value = m.groups()
        regdict[register.lower()] = int(value)
    s = mstate(**regdict)

    _, program = map(lambda x: str(x).strip(), program.split(':'))


class mops:

    nbits = 3

    def combop(s: mstate, op, /):
        if op < 4:
            return op, s
        elif op == 4:
            return s.a, s
        elif op == 5:
            return s.b, s
        elif op == 6:
            return s.c, s
        elif op == 7:
            return None, dataclasses.replace(s, halt=True)

    def adv(s: mstate, op, /):
        op, s = mops.combop(s, op)
        return dataclasses.replace(s, a=s.a // (2 ** op), ip=s.ip + 2), None

    def bxl(s: mstate, op, /):
        return dataclasses.replace(s, b=s.b ^ op, ip=s.ip + 2), None

    def bst(s: mstate, op, /):
        op, s = mops.combop(s, op)
        return dataclasses.replace(s, b=op % (1 << mops.nbits), ip=s.ip + 2), None

    def jnz(s: mstate, op, /):
        if s.a == 0:
            return dataclasses.replace(s, ip=s.ip + 2), None
        return dataclasses.replace(s, ip=op), None

    def bxc(s: mstate, op, /):
        return dataclasses.replace(s, b=s.b ^ s.c, ip=s.ip + 2), None

    def out(s: mstate, op, /):
        op, s = mops.combop(s, op)
        return dataclasses.replace(s, ip=s.ip + 2), op % (1 << mops.nbits)

    def bdv(s: mstate, op, /):
        op, s = mops.combop(s, op)
        return dataclasses.replace(s, b=s.a // (2 ** op), ip=s.ip + 2), None

    def cdv(s: mstate, op, /):
        op, s = mops.combop(s, op)
        return dataclasses.replace(s, c=s.a // (2 ** op), ip=s.ip + 2), None

    def run(s: mstate, instructions: list, /) -> tuple[mstate, list]:
        dispatch = [mops.adv, mops.bxl, mops.bst, mops.jnz, mops.bxc, mops.out, mops.bdv, mops.cdv]
        output = list()
        while True:
            # print(os.linesep)
            # print(f"-> {s=}")
            s, o = dispatch[instructions[s.ip]](s, instructions[s.ip + 1])
            if o is not None:
                output.append(o)
            s = dataclasses.replace(s, halt=s.halt | (s.ip >= len(instructions)))
            # print(f"-> {s=}")
            if s.halt:
                break

        return s, output


instructions = list(map(int, program.split(',')))
saved_s = copy.deepcopy(s)

s, ao = mops.run(s, instructions)
print(f"a={','.join(map(str, ao))}")
pass


b = -1
hiclist = [0]
for xi in range(len(instructions) - 1, -1, -1):
    t = list()
    for hic in hiclist:
        for loc in range(1 << mops.nbits):
            cc = (hic << mops.nbits) | loc
            s = dataclasses.replace(saved_s, a=cc)
            s, bo = mops.run(s, instructions)
            if instructions[xi] == bo[0]:
                t.append(cc)
    if xi > 0:
        hiclist = t
    else:
        b = min(t)
print(f"{b=}")
pass
