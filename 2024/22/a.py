import collections
import functools
import os


class SN:

    @functools.cache
    def _next(s):

        a = s * 64
        a = a ^ s
        a = a % 16777216

        b = a // 32
        b = b ^ a
        b = b % 16777216

        c = b * 2048
        c = c ^ b
        c = c % 16777216

        return c

    def __init__(self, secret: int, /, stopn: int = 2000) -> None:
        self.stopn = stopn
        self.seed = secret
        self.iterations = 0
        self.secret = secret
        self.px = secret % 10
        self.pdpxq = list()
        self.q = list()
        self.seenseq = set()
        self.sequences = collections.defaultdict(set)
        pass

    def __iter__(self):
        return self

    def __next__(self):
        if self.iterations >= self.stopn:
            raise StopIteration

        ppx = self.px

        self.secret = SN._next(self.secret)

        self.iterations += 1

        px = self.secret % 10
        dpx = px - ppx
        self.px = px

        self.pdpxq.append(dpx)
        while len(self.pdpxq) > 5:
            self.pdpxq = self.pdpxq[1:]

        seq = None
        firstseq = False
        if len(self.pdpxq) >= 5:
            seq = tuple(self.pdpxq[1:])
            if seq not in self.seenseq:
                firstseq = True
                self.seenseq.add(seq)
                self.sequences[px].add(seq)

        if not firstseq:
            seq = None

        return self.iterations, self.secret, self.px, seq


input = list()
with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as ifp:
    for line in map(str, map(lambda x: str(x).strip(), ifp.readlines())):
        if len(line) > 0:
            input.append(line)


a = 0
buyers = list()
payoffs = collections.defaultdict(int)
for line in input:
    line = int(line)
    iterator = SN(line)
    buyers.append(iterator)
    for n, seq, px, pdpxq in iterator:
        if pdpxq:
            payoffs[pdpxq] += px
    a += seq
print(f"{a=}")

b = max(payoffs.values())
print(f"{b=}")
pass
