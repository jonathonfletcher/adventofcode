import functools
import os


def flip_tile(in_tile):
    return [''.join(reversed(list(x))) for x in in_tile]



def rotate_tile(in_file):
    in_tile = list(list(x) for x in flip_tile(in_file))
    return [
        ''.join([in_tile[len(in_tile) - x -1].pop() for x in range(len(in_tile))])
            for y in range(len(in_tile))]



def tile_variants(in_tile):
    rval = list()
    for _ in range(4):
        if in_tile not in rval:
            rval.append(in_tile)
        if flip_tile(in_tile) not in rval:
            rval.append(flip_tile(in_tile))
        in_tile = rotate_tile(in_tile)
    return rval



def are_adjacent(t1_v, t2_v):
    t1_e = set(sum([[r[0], r[-1]] for r in t1_v], []))
    t2_e = set(sum([[r[0], r[-1]] for r in t2_v], []))
    return len(t1_e.intersection(t2_e)) > 0



## I understood this when I wrote it, but not afterwards...
def find_edge_path(node, goal, neighbours, edges):
    if len(edges) == 0:
        return [goal]
    else:
        for n in edges:
            if n in neighbours[node]:
                return [n] + find_edge_path(n, goal, neighbours, edges.difference({n}))
    return []



def update_grid_cell(grid, row, col, v):
    grid[row] = grid[row][:col] + [v] + grid[row][col+1:]
    return grid



def make_tile_grid(neighbours):
    corner_nodes = list(filter(lambda x: len(neighbours[x]) == 2, neighbours.keys()))
    edge_nodes = list(filter(lambda x: len(neighbours[x]) == 3, neighbours.keys()))
    edge_length = 2 + len(edge_nodes) // 4

    c1 = corner_nodes.pop()
    edge_route = [c1] + find_edge_path(c1, c1, neighbours, set(edge_nodes).union(set(corner_nodes)))

    top_row = edge_route[0:edge_length]
    right_side = list(reversed(edge_route[(1*edge_length)-0:(2*edge_length)-1]))
    bottom_row = list(reversed(edge_route[(2*edge_length)-2:(3*edge_length)-2]))
    left_side = edge_route[(3*edge_length)-4:(4*edge_length)-4]

    grid = [top_row]
    for _ in range(1, len(left_side)-1):
        row = [-1 for y in range(edge_length-2)]
        grid.append([left_side.pop()] + row + [right_side.pop()])
    grid.append(bottom_row)

    sn = set(edge_route)
    for row in range(1, len(grid)-1):
        for col in range(1, len(grid[row])-1):
            p_up = grid[row-1][col]
            p_left = grid[row][col-1]
            c = set(neighbours[p_up]).intersection(neighbours[p_left]).difference(sn)
            if p_up >= 0 and p_left >= 0:
                v = c.pop()
                grid = update_grid_cell(grid, row, col, v)
                sn.add(v)

    return grid



## Figure out which tiles are neighours
def find_neighbours(tiles):
    neighbours = dict()
    variants = dict()
    for t1 in tiles.keys():
        n = set()
        t1_v = tile_variants(tiles[t1])
        for t2 in tiles.keys():
            if t1 == t2:
                continue
            t2_v = variants.get(t2)
            if not t2_v:
                variants[t2] = tile_variants(tiles[t2])
                t2_v = variants.get(t2)
            if are_adjacent(t1_v, t2_v):
                n.add(t2)
        neighbours[t1] = n
    return neighbours



def match_tile_right(t1_v, t2_v):
    t1_v = rotate_tile(t1_v)
    for t_v in tile_variants(t2_v):
        if t1_v[-1] == t_v[0]:
            return rotate_tile(rotate_tile(rotate_tile(t_v)))
    return None



def match_tile_below(t1_v, t2_v):
    for t_v in tile_variants(t2_v):
        if t1_v[-1] == t_v[0]:
            return t_v
    return None



def match_0_0_corner(tiles, corner, right, below):
    for c_v in tile_variants(tiles[corner]):
        r_v = match_tile_right(c_v, tiles[right])
        b_v = match_tile_below(c_v, tiles[below])
        if r_v and b_v:
            return c_v, r_v, b_v
    return None, None, None



def print_image(image):
    for outer_row in image:
        for row in range(len(outer_row[0])):
            print(' '.join([outer_row[x][row] for x in range(len(outer_row))]))
        print('')



def shrink_image(in_image, add_space=False):
    out_image = list()
    for outer_row_idx in range(len(image)):
        outer_row = image[outer_row_idx]

        fr, tr = 1, len(outer_row[0])-1
        # if outer_row_idx == 0:
        #     fr -= 1
        # elif outer_row_idx == len(image)-1:
        #     tr += 1

        for inner_row_idx in range(fr, tr):
            img_row = list()
            for inner_col_idx in range(len(outer_row)):
                fc, tc = 1, len(outer_row[0])-1
                # if inner_col_idx == 0:
                #     fc -= 1
                # elif inner_col_idx == len(outer_row)-1:
                #     tc += 1

                img_row.append(outer_row[inner_col_idx][inner_row_idx][fc:tc])

            if add_space:
                out_image.append(' '.join(img_row))
            else:
                out_image.append(''.join(img_row))
        if add_space:
            out_image.append('')
    return out_image



def make_image(tiles, tile_grid):
    image = [[None for x in range(len(tile_grid))] for y in range(len(tile_grid))]

    ## Find the top-left corner
    r0_0, r0_1, r1_0 = match_0_0_corner(tiles, tile_grid[0][0], tile_grid[0][1], tile_grid[1][0])
    image = update_grid_cell(image, 0, 0, r0_0)
    image = update_grid_cell(image, 0, 1, r0_1)
    image = update_grid_cell(image, 1, 0, r1_0)

    ## Match up the left column
    for row in range(2, len(image)):
        t2 = tile_grid[row][0]
        r = match_tile_below(image[row-1][0], tiles[t2])
        image = update_grid_cell(image, row, 0, r)

    ## Match up the rows, based on the left column
    for row in range(len(image)):
        for col in range(1, len(image[row])):
            t2 = tile_grid[row][col]
            r = match_tile_right(image[row][col-1], tiles[t2])
            image = update_grid_cell(image, row, col, r)

    return image



def read_input(filename):
    tiles = dict()
    with open(filename) as ifp:
        tile_id = None
        tile = list()
        for line in [x.strip() for x in ifp.readlines()]:
            if line.find('Tile') == 0:
                tile_id = int(line.split(' ')[1].split(':')[0])
            elif len(line) == 0:
                if tile_id is not None and len(tile) > 0:
                    tiles[tile_id] = tile
                    tile_id = None
                    tile = list()
            else:
                tile.append(line)
        if tile_id is not None and len(tile) > 0:
            tiles[tile_id] = tile
            tile_id = None
            tile = list()
    return tiles



def sea_monster_coordinates():
    monster_pattern = [
        '                  # ',
        '#    ##    ##    ###',
        ' #  #  #  #  #  #   ',
        ]
    monster_coordinates = list()
    for row in range(len(monster_pattern)):
        for col in range(len(monster_pattern[row])):
            if monster_pattern[row][col] == '#':
                monster_coordinates.append([row, col])
    return monster_coordinates



def evaluate_roughness(image, monster_coordinates=sea_monster_coordinates()):
    max_row = max([x[0] for x in monster_coordinates])
    max_col = max([x[1] for x in monster_coordinates])

    monster_count = 0
    for row in range(len(image)-max_row):
        for col in range(len(image[0])-max_col):
            found_monster = True
            for (m_row, m_col) in monster_coordinates:
                if image[row+m_row][col+m_col] != '#':
                    found_monster = False
                    break
            if found_monster:
                monster_count+=1
    roughness = 0
    if monster_count > 0:
        pre_monster_roughness = functools.reduce(lambda x, y: x+y, list(map(lambda lx: len(lx), [list(filter(lambda x: x=='#', row)) for row in image])), 0)
        roughness = pre_monster_roughness - monster_count * len(monster_coordinates)
        # print(functools.reduce(lambda x, y: x+y, list(map(lambda lx: len(lx), [list(filter(lambda x: x=='#', row)) for row in image])), 0))
    return roughness



tiles = read_input("input.txt")


neighbours = find_neighbours(tiles)


## Part A: The corners only have *two* neighbours
corner_nodes = list(filter(lambda x: len(neighbours[x]) == 2, neighbours.keys()))
print(80 * "=")
if len(corner_nodes) == 4:
    print("result_a: {}".format(functools.reduce(lambda x, y: x*y, corner_nodes, 1)))
print(80 * "=")


tile_grid = make_tile_grid(neighbours)
# for row in tile_grid:
#     print(row)


image = make_image(tiles, tile_grid)
# print_image(image)


image = shrink_image(image)
# for row in image:
#     print("{}".format(row))


print(80 * "=")
for v in tile_variants(image):
    roughness = evaluate_roughness(v)
    if roughness > 0:
        print("result_b: {}".format(roughness))
        break
print(80 * "=")

