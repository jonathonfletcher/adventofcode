from typing import List


def read_input(ifp):
    grid = list()
    for line in [x.strip() for x in ifp.readlines()]:
        grid.append(list(line.strip()))
    return grid



def shiftright(grid):
    newgrid = [list(x) for x in grid]
    maxy = len(grid)
    maxx = len(grid[0])
    delta = 0
    y = 0
    while y < maxy:
        x = 0
        while x < maxx:
            nx = (x+1)%maxx
            if grid[y][x] == '>' and grid[y][nx] == '.':
                newgrid[y][nx] = grid[y][x]
                newgrid[y][x] = '.'
                x += 2
                delta += 1
                continue
            else:
                x += 1
                continue
        y += 1
    return newgrid



def shiftdown(grid):
    newgrid = [list(x) for x in grid]
    maxy = len(grid)
    maxx = len(grid[0])
    delta = 0
    x = 0
    while x < maxx:
        y = 0
        while y < maxy:
            ny = (y+1)%maxy
            if grid[y][x] == 'v' and grid[ny][x] == '.':
                newgrid[ny][x] = grid[y][x]
                newgrid[y][x] = '.'
                y += 2
                delta += 1
                continue
            else:
                y += 1
                continue
        x += 1
    return newgrid



def day25(grid:List[List[str]]):
    print(f'{len(grid)} / {len(grid[0])}')
    newgrid = grid
    grid = list()
    counter = 0
    while newgrid != grid:
        grid = newgrid
        newgrid = shiftdown(shiftright(grid))
        # print(f' {grid}')
        # print(f':{newgrid}')
        counter+= 1
    print(counter)
    return



if __name__ == '__main__':
    with open("part1.txt") as ifp:
        grid = read_input(ifp)
        day25(grid)
