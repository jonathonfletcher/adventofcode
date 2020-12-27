


def xform(subject_number, loop_size):
    in_value = 1
    for _ in range(loop_size):
        in_value = ( in_value * subject_number ) % 20201227 
    return in_value


def find_loop_size(pk, subject_number=7):
    loop_size = 0
    in_value = 1
    while True:
        loop_size += 1
        in_value = ( in_value * subject_number ) % 20201227 
        if in_value == pk:
            break
    return loop_size
        

public_keys = [5764801, 5764801]
loop_sizes = [find_loop_size(pk) for pk in public_keys]

loop_sizes = list(reversed(loop_sizes))
for i in range(len((public_keys))):
    k = xform(public_keys[i], loop_sizes[i])
    print("{}".format(k))


