import os

warehouse = dict()
robot = None
with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as ifp:
    grid, path = ifp.read().split(os.linesep * 2)
    path = path.replace(os.linesep, '')
    for y, row in enumerate(grid.split(os.linesep)):
        for x, c in enumerate(row):
            if c == '@':
                robot = (x, y)
                c = '.'
            warehouse[(x, y)] = c


def print_warehouse(warehouse, robot, /):
    maxx = 1 + max(map(lambda xy: xy[0], warehouse.keys()))
    maxy = 1 + max(map(lambda xy: xy[1], warehouse.keys()))
    for y in range(maxy):
        line = ""
        for x in range(maxx):
            if (x, y) == robot:
                line += '@'
            else:
                line += warehouse[(x, y)]
        print(line)

    pass


def push_a(warehouse, robot, dxy, /):
    rx, ry = robot
    dx, dy = dxy
    bx, by = rx + dx, ry + dy

    obx, oby = bx, by
    while warehouse[(bx, by)] != '#':
        bx, by = bx + dx, by + dy
        if warehouse[(bx, by)] == '.':
            t = warehouse[(bx, by)]
            warehouse[(bx, by)] = warehouse[(obx, oby)]
            warehouse[(obx, oby)] = t
            robot = (obx, oby)
            return warehouse, robot, True

    return warehouse, robot, False


def push_bx(warehouse, robot, dx, /):

    def find_bx(warehouse, robot, dx, /):
        rx, ry = robot
        bx = rx + dx

        if warehouse[(bx, ry)] == '.':
            return {bx}, bx
        elif warehouse[(bx, ry)] == '#':
            return set(), bx
        else:
            return find_bx(warehouse, (bx, ry), dx)

    rx, ry = robot
    sx, bx = find_bx(warehouse, robot, dx)
    while len(sx) > 0 and abs(rx - bx) > 1:
        t = warehouse[(bx, ry)]
        for i in range(2):
            warehouse[(bx, ry)] = warehouse[(bx - dx, ry)]
            bx -= dx
        warehouse[(bx, ry)] = t
        sx, bx = find_bx(warehouse, robot, dx)

    if len(sx) > 0:
        rx += dx

    return warehouse, (rx, ry), len(sx) > 0


def push_by(warehouse, robot, dy, /):

    def find_by(warehouse, robot, dy, /):
        rx, ry = robot
        by = ry + dy

        if warehouse[(rx, by)] == '.':
            return {rx}, by
        elif warehouse[(rx, by)] == '#':
            return set(), by
        else:
            nx = 0
            if warehouse[(rx, by)] == '[':
                nx = rx + 1
            elif warehouse[(rx, by)] == ']':
                nx = rx - 1

            nxs, nby = find_by(warehouse, (nx, by), dy)
            rxs, rby = find_by(warehouse, (rx, by), dy)
            pass

            if nby == rby:
                nnx = nxs.union(rxs)
                if len(nnx) > 0 and len(nnx) % 2 == 0:
                    return nnx, nby
            elif dy > 0:
                if nby > rby and len(nxs) > 0 and len(nxs) % 2 == 0:
                    return nxs, nby
                elif rby > nby and len(rxs) > 0 and len(rxs) % 2 == 0:
                    return rxs, rby
            elif dy < 0:
                if nby < rby and len(nxs) > 0 and len(nxs) % 2 == 0:
                    return nxs, nby
                elif rby < nby and len(rxs) > 0 and len(rxs) % 2 == 0:
                    return rxs, rby

            return set(), by

    rx, ry = robot
    sx, by = find_by(warehouse, robot, dy)
    while len(sx) > 0 and abs(ry - by) > 1:
        for x in sx:
            t = warehouse[(x, by)]
            warehouse[(x, by)] = warehouse[(x, by - 1 * dy)]
            warehouse[(x, by - 1 * dy)] = t
        sx, by = find_by(warehouse, robot, dy)

    if len(sx) > 0:
        ry += dy

    return warehouse, (rx, ry), len(sx) > 0


def push_b(warehouse, robot, dxy, /):
    dx, dy = dxy
    if dx != 0:
        return push_bx(warehouse, robot, dx)
    elif dy != 0:
        return push_by(warehouse, robot, dy)
    else:
        barf()


def move(si, warehouse, robot, step, pushf, /):
    mmap = {'v': (0, 1), '^': (0, -1), '<': (-1, 0), '>': (1, 0)}
    rdx, rdy = mmap[step]

    if si == 312:
        pass

    rx, ry = robot
    nrx, nry = rx + rdx, ry + rdy
    if warehouse[(nrx, nry)] == '.':
        return warehouse, (nrx, nry), False
    elif warehouse[(nrx, nry)] == '#':
        return warehouse, robot, False
    else:
        return pushf(warehouse, robot, (rdx, rdy))


def make_b(warehouse, robot, /):
    b_warehouse = dict()
    for (x, y), c in warehouse.items():
        if c in ['.', '#']:
            b_warehouse[(2 * x, y)] = c
            b_warehouse[(2 * x + 1, y)] = c
        elif c in ['O']:
            b_warehouse[(2 * x, y)] = '['
            b_warehouse[(2 * x + 1, y)] = ']'
    rx, ry = robot
    return b_warehouse, (2 * rx, ry)


def gps(warehouse):
    v = 0
    for (x, y), c in warehouse.items():
        if c in ['O', '[']:
            v += 100 * y + x
    return v


a_warehouse = warehouse.copy()
a_robot = robot
# print_warehouse(a_warehouse, a_robot)
for si, step in enumerate(path):
    a_warehouse, a_robot, a_push = move(si, a_warehouse, a_robot, step, push_a)
    # print(os.linesep)
    # print(f"Move {step}:")
    # print_warehouse(a_warehouse, a_robot)
    pass
a = gps(a_warehouse)
print(f"{a=}")


b_warehouse, b_robot = make_b(warehouse, robot)
# print_warehouse(b_warehouse, b_robot)
for si, step in enumerate(path):
    b_warehouse, b_robot, b_push = move(si, b_warehouse, b_robot, step, push_b)
    # print(os.linesep)
    # print(f"Move {step}:")
    # print_warehouse(b_warehouse, b_robot)
b = gps(b_warehouse)
print(f"{b=}")

pass