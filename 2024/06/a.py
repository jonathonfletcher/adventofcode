import datetime
import functools
import os


def ftime(func):

    @functools.wraps(func)
    def wrapfn(*args, **kwargs):
        st = datetime.datetime.now(tz=datetime.UTC)
        f_rval = func(*args, **kwargs)
        et = datetime.datetime.now(tz=datetime.UTC)
        print(f'{"<" * 5} {func.__qualname__!r} {et - st}')
        return f_rval

    return wrapfn


with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as ifp:
    input = list(map(list, map(lambda x: x.strip(), ifp.readlines())))

pos = (0, 0)
obstacles = set()
maxx = 0
maxy = len(input)

for y, row in enumerate(input):
    maxx = len(row)
    for x, c in enumerate(row):
        if c == '#':
            obstacles.add((x, y))
        elif c == '^':
            pos = (x, y)


def path(obstacles, maxx, maxy, pos, /):
    direction = 0
    moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    locations = set()
    isloop = False
    x, y = pos
    while x in range(maxx) and y in range(maxy) and not isloop:

        if (x, y, direction) in locations:
            return locations, True

        locations.add((x, y, direction))

        nx = x + moves[direction][0]
        ny = y + moves[direction][1]

        if (nx, ny) in obstacles:
            direction = (direction + 1) % len(moves)
        else:
            x = nx
            y = ny

    return locations, False


@ftime
def parta():
    apath, _ = path(obstacles, maxx, maxy, pos)
    apath = set(map(lambda x: (x[0], x[1]), apath))
    return len(apath)


a = parta()
print(f"{a=}")


@ftime
def partb():

    # def _up(obstacles, xx, yy, /):
    #     return any(filter(lambda x: x[1] == yy + 1 and x[0] > xx, obstacles))
    # def _down(obstacles, xx, yy, /):
    #     return any(filter(lambda x: x[1] == yy - 1 and x[0] < xx, obstacles))
    # def _right(obstacles, xx, yy, /):
    #     return any(filter(lambda x: x[0] == xx - 1 and x[1] > yy, obstacles))
    # def _left(obstacles, xx, yy, /):
    #     return any(filter(lambda x: x[0] == xx + 1 and x[1] < yy, obstacles))

    # vmap = {
    #     0: _up,
    #     2: _down,
    #     1: _right,
    #     3: _left
    # }

    b = 0
    bpath, _ = path(obstacles, maxx, maxy, pos)
    seenpath = set()
    for x, y, d in bpath:
        if any([(x, y) in obstacles, (x, y) in seenpath, (x, y) == pos]):
            continue
        seenpath.add((x, y))

        # if not vmap[d](obstacles, x, y):
        #     continue

        obstacles.add((x, y))
        _, stuck = path(obstacles, maxx, maxy, pos)
        if stuck:
            b += 1
        obstacles.discard((x, y))
    return b


b = partb()
print(f"{b=}")
