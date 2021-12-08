from collections import defaultdict


class P1(object):

    def __init__(self):
        self.counter = 0
        self.length_mapping = {
            2:1,
            3:7,
            4:4,
            7:8
        }

    def add(self, inputs, outputs):
        for o in outputs:
            if len(o) in self.length_mapping.keys():
                self.counter += 1

    @property
    def value(self):
        return self.counter


class P2(P1):

    def deduce_inputs(self, inputs):
        found = {}
        segments = {}
        remaining = list()
        for i in inputs:
            x = self.length_mapping.get(len(i))
            if x is not None:
                found[x] = i
            remaining.append(i)

        remaining = sorted(remaining, key=lambda x: len(x))

        if found.get(1):
            for seg in found[1]:
                c = 0
                for e in remaining:
                    if not set([seg]).issubset(set(e)):
                        c+=1
                if 1 == c:
                    segments['f'] = seg
                    for e in remaining:
                        if not set([seg]).issubset(set(e)):
                            found[2] = e
                            break
                elif 2 == c:
                    segments['c'] = seg

            if found.get(7):
                b_seg = set(found[7])-set(found[1])
                if 1 == len(b_seg):
                    segments['a'] = b_seg.pop()

            for e in remaining:
                if not 5 == len(e):
                    continue
                if e in found.values():
                    continue

                seg_c = segments['c']
                seg_f = segments['f']
                if set([seg_c]).issubset(set(e)):
                    found[3] = e
                elif set([seg_f]).issubset(set(e)):
                    found[5] = e
                    i = set(e).intersection(set(found[2])).intersection(set(found[4]))
                    if 1 == len(i):
                        segments['d'] = i.pop()

            if found.get(4):
                e = set(found[4])
                for k in ['c', 'd', 'f']:
                    v = segments.get(k)
                    if v is not None:
                        e = e - set([v])
                if 1 == len(e):
                    segments['b'] = e.pop()

            if found.get(3) and found.get(5):
                e = set(found[3]).intersection(set(found[5]))
                for k, v in segments.items():
                    e = e - set([v])
                if 1 == len(e):
                    segments['g'] = e.pop()

            for r in remaining:
                if not 7 == len(r):
                    continue
                e = set(r)
                for k, v in segments.items():
                    e = e - set([v])
                if 1 == len(e):
                    segments['e'] = e.pop()

            for r in remaining:
                if not 6 == len(r):
                    continue
                d_seg = set([segments['d']])
                e_seg = set([segments['e']])
                if d_seg.union(e_seg).issubset(set(r)):
                    found[6] = r
                elif d_seg.issubset(set(r)):
                    found[9] = r
                elif e_seg.issubset(set(r)):
                    found[0] = r

            if False:
                rfound = {str(v):str(k) for k, v in found.items()}
                rsegments = {str(v):str(k) for k, v in segments.items()}
                for r in remaining:
                    row = list()
                    for e in list("ABCDEFG"):
                        v = " "
                        if set([e]).issubset(set(r)):
                            v = e
                        row.append(f'{rsegments.get(v,"")}-{v}')
                    row.append(str(len(r)))
                    row.append(rfound.get(r, ""))
                    print("\t".join(row))
            
            return {str(v):int(k) for k, v in found.items()}


    def add(self, inputs, outputs):
        found = self.deduce_inputs(inputs)
        if 10 == len(found):
            # print(outputs)
            # print(found)
            v = 0
            for o in outputs:
                v *= 10
                v += found[o]
            print(f'{outputs} - {v}')
            self.counter += v


if __name__ == '__main__':
    with open("part1.txt") as ifp:

        p1 = P1()
        p2 = P2()

        for line in list(map(lambda x: x.strip().upper(), ifp.readlines())):

            inputs, outputs = list(map(lambda x: x.strip(), line.split('|')))

            inputs = list(map(lambda x: ''.join(sorted(list(x))), inputs.split()))
            outputs = list(map(lambda x: ''.join(sorted(list(x))), outputs.split()))

            p1.add(inputs, outputs)
            p2.add(inputs, outputs)

        print(p1.value)
        print(p2.value)
