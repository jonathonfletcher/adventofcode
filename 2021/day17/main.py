import os


def candidates(tgt_min_in, tgt_max_in, noneg):

    def candidate_step(p, v, t_min, t_max, stepn, noneg):
        # print(f'{p:4} {v:4} {t_min:4} {t_max:4}')
        if v < 0:
            if noneg:
                # print(f'{noneg}')
                return False
            elif p < t_min:
                # print(f'{p} {t_min}')
                return False

        if p >= t_min and p <= t_max:
            return True
        else:
            p += v
            v -= 1
            return candidate_step(p, v, t_min, t_max, stepn+1, noneg)

    s = set()
    tgt_min = min(tgt_min_in, tgt_max_in)
    tgt_max = max(tgt_min_in, tgt_max_in)

    tgt_range_end = max(abs(tgt_min_in), abs(tgt_max_in))
    tgt_range_start = 0
    if noneg == False:
        tgt_range_start = tgt_min_in

    for v in range(tgt_range_start, tgt_range_end+1):
        if candidate_step(0, v, tgt_min, tgt_max, 0, noneg):
            s.add(v)
    return s


def hit_target(xv, yv, tgt_min_x, tgt_max_x, tgt_min_y, tgt_max_y , x=0, y=0):
    if x >= tgt_min_x and x <= tgt_max_x and y >= tgt_min_y and y <= tgt_max_y:
        return True
    elif x > tgt_max_x or y < tgt_min_y:
        return False
    else:
        x += xv
        xv -= 1
        y += yv
        yv -= 1
        if xv < 0:
            xv = 0
        return hit_target(xv, yv, tgt_min_x, tgt_max_x, tgt_min_y, tgt_max_y, x, y)


def candidate_height(v, h=0):
    if v <= 0:
        return h
    else:
        h += v
        v -= 1
        return candidate_height(v, h)


input = "target area: x=20..30, y=-10..-5"
tgt_min_x = 20
tgt_max_x = 30
tgt_min_y = -10
tgt_max_y = -5


vx_candidates = candidates(tgt_min_x, tgt_max_x, True)
vy_candidates = candidates(tgt_min_y, tgt_max_y, False)


print(f'part1: {candidate_height(max(vy_candidates))}')


hits = set()
for yv in vy_candidates:
    for xv in vx_candidates:
        if hit_target(xv, yv, tgt_min_x, tgt_max_x, tgt_min_y, tgt_max_y):
            hits.add(f'{xv},{yv}')
print(f'part2: {len(hits)}')

