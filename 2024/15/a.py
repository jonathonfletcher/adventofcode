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


def findgroup(warehouse, robot, dxy, gdict, /):
    rx, ry = robot
    dx, dy = dxy
    cx, cy = rx + dx, ry + dy
    if abs(dx) > 0:
        if any([dx > 0 and warehouse[(cx, cy)] == '[', dx < 1 and warehouse[(cx, cy)] == ']']):
            gdict[(cx, cy)] = warehouse[(cx, cy)]
            cx += dx
            gdict[(cx, cy)] = warehouse[(cx, cy)]
            return findgroup(warehouse, (cx, cy), dxy, gdict)
    elif abs(dy) > 0:
        if warehouse[(cx, cy)] in ['[', ']']:
            gdict[(cx, cy)] = warehouse[(cx, cy)]
            if warehouse[(cx, cy)] == '[':
                nx = cx + 1
            elif warehouse[(cx, cy)] == ']':
                nx = cx - 1
            gdict[(nx, cy)] = warehouse[(nx, cy)]
            return findgroup(warehouse, (cx, cy), dxy, gdict) | findgroup(warehouse, (nx, cy), dxy, gdict)
    return gdict


def pushgroup(warehouse, gdict, dxy, /):
    dx, dy = dxy
    ns = dict()
    for (x, y), c in gdict.items():
        ns[(x + dx, y + dy)] = c
    return ns


def groupvalid(warehouse, c_dict, p_dict):
    c_locations = c_dict.keys()
    for xy in p_dict.keys():
        if xy in c_locations:
            continue
        if warehouse[xy] != '.':
            return False
    return True


def update(warehouse, robot, dxy, c_dict, p_dict, /):
    for xy, c in p_dict.items():
        warehouse[xy] = c
    for xy, c in c_dict.items():
        if xy not in p_dict.keys():
            warehouse[xy] = '.'
    if len(findgroup(warehouse, robot, dxy, dict())) > 0:
        barf()
    rx, ry = robot
    dx, dy = dxy
    return warehouse, (rx + dx, ry + dy), True


def push_b(warehouse, robot, dxy, /):
    dx, dy = dxy
    c_dict = findgroup(warehouse, robot, dxy, dict())
    p_dict = pushgroup(warehouse, c_dict, dxy)
    if groupvalid(warehouse, c_dict, p_dict):
        return update(warehouse, robot, dxy, c_dict, p_dict)
    else:
        return warehouse, robot, False


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
    # print(os.linesep)
    # print(f"Move {step}:")
    a_warehouse, a_robot, a_push = move(si, a_warehouse, a_robot, step, push_a)
    # print_warehouse(a_warehouse, a_robot)
    pass
a = gps(a_warehouse)
print(f"{a=}")


b_warehouse, b_robot = make_b(warehouse, robot)
# print_warehouse(b_warehouse, b_robot)
for si, step in enumerate(path):
    # print(os.linesep)
    # print(f"Move {step}:")
    b_warehouse, b_robot, b_push = move(si, b_warehouse, b_robot, step, push_b)
    # print_warehouse(b_warehouse, b_robot)
b = gps(b_warehouse)
print(f"{b=}")

pass