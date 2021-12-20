

algo = None
image = list()
with open('part0.txt') as ifp:
    for line in [l.strip() for l in ifp.readlines()]:
        if len(line) > 0:
            if algo is None:
                algo = line
            else:
                image.append([x for x in line])

print(len(algo))

for i in range(2):
    
    current_image = []
    current_image.append(['.' for x in range(8+len(image[0]))])
    current_image.append(['.' for x in range(8+len(image[0]))])
    current_image.append(['.' for x in range(8+len(image[0]))])
    current_image.append(['.' for x in range(8+len(image[0]))])
    for row in image:
        current_image.append(['.'] * 4 + row +['.'] * 4)
    current_image.append(['.' for x in range(8+len(image[0]))])
    current_image.append(['.' for x in range(8+len(image[0]))])
    current_image.append(['.' for x in range(8+len(image[0]))])
    current_image.append(['.' for x in range(8+len(image[0]))])

    new_image = [['.' for x in range(8+len(image[0]))]
              for y in range(8+len(image))]

    print(f'{len(image)} -> {len(new_image)}')

    new_image = list()
    for row in current_image:
        new_image.append(['.'] * len(row))

    print()
    for row in current_image:
        print(''.join(row))

    print()
    for row in new_image:
        print(''.join(row))

    lit_pixels = 0
    print(range(1, len(current_image)-1))
    for y in range(1, len(current_image)-1):
        for x in range(1, len(current_image[y])-1):
            thing = ""
            for dy in [-1, 0, 1]:
                thing += ''.join(current_image[y+dy][x-1:x+2])
                # for dx in [-1, 0, 1]:
                #     if y+dy >= 0 and y+dy < len(current_image) and x+dx >= 0 and x+dx < len(current_image[y]):
                #         thing += current_image[y+dy][x+dx]
                #     else:
                #         thing += '.'

            # print(thing)
            # print(f'x:{x}, y:{y} - {thing}')
            thing = int(thing.replace('#', '1').replace('.', '0'), 2)

            # print(f'{x+1},{y+1} = {algo[thing]}')
            npx = algo[thing]
            if npx == '#':
                lit_pixels += 1
            new_image[y][x] = npx

    print()
    for row in new_image:
        print(''.join(row))
    print(lit_pixels)

    image = new_image
