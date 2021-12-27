from typing import Final, List, Set, Dict, Tuple, Any
from collections import defaultdict
from functools import total_ordering


@total_ordering
class Point(object):

    def __init__(self, x: int, y: int, z: int) -> None:
        self.x: Final = x
        self.y: Final = y
        self.z: Final = z

    def __repr__(self) -> str:
        p = str(','.join(map(lambda x: str(x), [self.x, self.y, self.z])))
        return f'{self.__class__.__name__}({p})'

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return (self.__class__ == other.__class__
                and self.x == other.x
                and self.y == other.y
                and self.z == other.z)

    def __lt__(self, other):
        return self.x < other.x or self.y < other.y or self.z < other.z


class Rotation(Point):

    c: Final = 0
    s: Final = 1
    rx: Final = [[1, 0, 0], [0, c, -s], [0, s, c]]
    ry: Final = [[c, 0, s], [0, 1, 0], [-s, 0, c]]
    rz: Final = [[c, -s, 0], [s, c, 0], [0, 0, 1]]

    @staticmethod
    def dot(ls, rs):
        return [[sum(ls * rs
                for ls, rs in zip(lsr, rsc))
                for rsc in zip(*rs)]
                for lsr in ls]

    @staticmethod
    def all():

        rotations = list()
        for xr, zr in [[0, 0], [1, 0], [2, 0], [3, 0], [0, 1], [0, 3]]:
            for yr in range(3):
                rotations.append(Rotation(xr, yr, zr))
        return rotations

        # def donr(n, p, r):
        #     for i in range(n):
        #         p = Rotation.dot(p, r)
        #     return p

        # rotations = set()
        # seen_p = set()
        # for nx in range(4):
        #     for ny in range(4):
        #         for nz in range(4):
        #             p = [[1, 2, 3]]
        #             p = donr(nx, p, Rotation.rx)
        #             p = donr(ny, p, Rotation.ry)
        #             p = donr(nz, p, Rotation.rz)
        #             if str(p) not in seen_p:
        #                 # print(f'nx:{nx}, ny:{ny}, nz:{nz}')
        #                 seen_p.add(str(p))
        #                 rotations.add(Rotation(nx, ny, nz))

        # # print(len(seen_p))
        # return sorted(rotations)


class Beacon(Point):

    def __sub__(self, other):
        return self.sub(other)

    def sub(self, other):
        return Point(self.x-other.x, self.y-other.y, self.z-other.z)

    def __add__(self, other: Point):
        return self.add(other)

    def in_range(self, other: Point):
        d = self - other
        return ( abs(d.x) <= 2000 and abs(d.y) <= 2000 and abs(d.z) <= 2000 )

    def add(self, other: Point):
        return Beacon(self.x+other.x, self.y+other.y, self.z+other.z)

    def rotate(self, r: Rotation):

        def donr(n, p, r):
            p = [p]
            for i in range(n):
                p = Rotation.dot(p, r)
            return p[0]

        xyz = [self.x, self.y, self.z]
        xyz = donr(r.x, xyz, Rotation.rx)
        xyz = donr(r.y, xyz, Rotation.ry)
        xyz = donr(r.z, xyz, Rotation.rx)
        return Beacon(*xyz)


@total_ordering
class Scanner(object):

    def __init__(self, name):
        self.name: Final = name
        self.beacons: Final = list()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{self.name}")'

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, __o: object) -> bool:
        return self.name == __o.name

    def __lt__(self, __o: object) -> bool:
        return self.name < __o.name

    def rotated_beacons(self, r: Rotation):
        rb = list()
        for b in self.beacons:
            rb.append(b.rotate(r))
        return rb

    def add_beacon(self, b: Beacon) -> None:
        self.beacons.append(b)

    def rotate(self, r: Rotation):
        ns = Scanner(self.name)
        for b in self.rotated_beacons(r):
            ns.add_beacon(b)
        return ns

    def position(self, p: Point):
        ns = Scanner(self.name)
        for b in self.beacons:
            ns.add_beacon(Beacon(b.x+p.x, b.y+p.y, b.z+p.z))
        return ns


if True:
    found_scanners: Final = set()
    lost_scanners: Final = set()
    scanner_translations: Final = dict()

    with open('eg1.txt') as ifp:
        s = None
        for line in [l.strip() for l in ifp.readlines()]:
            if len(line) > 0:
                if line[0] == '-' and line[-1] == '-':
                    s_name = line.split()[-2]
                    s = Scanner(s_name)
                    if s_name == "0":
                        found_scanners.add(s)
                        scanner_translations[s] = (
                            Rotation(0, 0, 0), Point(0, 0, 0))
                    else:
                        lost_scanners.add(s)
                else:
                    x, y, z = list(map(lambda x: int(x), line.split(',')))
                    s.add_beacon(Beacon(x, y, z))

    rotations: Final = Rotation.all()

    while len(lost_scanners) > 0:
        print()
        print(f'found: {found_scanners}')
        print(f'lost: {lost_scanners}')
        print(f'xforms: {scanner_translations}')

        print(found_scanners)
        for fs in found_scanners:
            fs_r, fs_p = scanner_translations[fs]
            # tfs = fs.position(fp).rotate(fr)
            rfs = fs.rotate(fs_r)

            # in_range_remaining_scanners = set()
            # for rs in remaining_scanners:
            #     for r in rotations:
            #         rrs = rs.rotate(r)
            #         for fsb in rs.beacons:
            #             for rsb in rs.beacons:
            #             if fsb.in_range(rsb):


            rfs = rfs.position(fs_p)

            scanner_found = False
            for ls in lost_scanners:
                print(f'{rfs} -> {ls}')
                for r in rotations:
                    diff_map = defaultdict(int)
                    for fb in rfs.beacons:
                        for lb in ls.rotated_beacons(r):
                            if fb.in_range(lb):
                                bd = fb-lb
                                # print(f'{b0} - {b1} == {b0-b1}')
                                diff_map[bd] += 1

                    # print(diff_map)
                    for k, v in diff_map.items():
                        if v == 12:
                            print(f'{k}: {v}')
                    for k, v in diff_map.items():
                        if v == 12:
                            print(f'{rfs} matched {ls} with {r} and {k}')
                            scanner_found = True
                            scanner_translations[ls] = [r, k]
                            found_scanners.add(ls)
                            lost_scanners.remove(ls)
                    if scanner_found:
                        break
                if scanner_found:
                    break
            if scanner_found:
                break
    print(found_scanners)
    print(scanner_translations)
    print(lost_scanners)
