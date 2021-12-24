

class P(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return ( self.__class__ == other.__class__ 
            and self.x == other.x
            and self.y == other.y )
    def __repr__(self):
        return f'{self.__class__.__name__}({self.x},{self.y})'
    def __hash__(self):
        return hash(str(self))


def print_image(image):
    output_mapping = { 0: '.', 1: '#'}
    img_x = list(set(map(lambda x: x.x, image.keys())))
    img_y = list(set(map(lambda x: x.y, image.keys())))
    for y in range(min(img_y), max(img_y)+1):
        print_line = ""
        for x in range(min(img_x), max(img_x)+1):
            print_line += output_mapping.get((image.get(P(x, y), 0)))
        print(print_line)


algo = None
image = {}
input_mapping = { '#': 1, '.': 0 }
with open('part1.txt') as ifp:
    y=0
    for line in [l.strip() for l in ifp.readlines()]:
        if len(line) > 0:
            if algo is None:
                algo = list(map(lambda x: input_mapping[x], line))
            else:
                x = 0
                for v in line:
                    image[P(x,y)] = input_mapping[v]
                    x += 1
                y += 1


for iteration in range(50):
    current_x = list(set(map(lambda x: x.x, image.keys())))
    current_y = list(set(map(lambda x: x.y, image.keys())))
    current_image_default = 0

    new_image = dict()
    new_image_lit = 0

    if algo[0] > 0 and algo[-1] < 1:
        current_image_default = algo[0]
        if not iteration % 2:
            current_image_default = algo[-1]
    # print(f'{1+iteration} {current_image_default}')

    for y in range(min(current_y)-2, max(current_y)+3):
        for x in range(min(current_x)-2, max(current_x)+3):
            algo_offset = 0
            for dy in [ -1, 0, 1 ]:
                for dx in [ -1, 0, 1 ]:
                    ov = image.get(P(x+dx, y+dy), current_image_default)
                    algo_offset <<= 1
                    algo_offset += ov
            nv = algo[algo_offset]
            new_image[P(x,y)] = nv
            new_image_lit += nv

    # print_image(new_image)
    if iteration in [ 1, 49 ]:
        print(f'{1+iteration} {new_image_lit}')

    image = new_image

