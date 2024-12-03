import functools
import os
import re

with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as ifp:
    input = list(map(lambda x: x.strip(), ifp.readlines()))

all_ex = re.compile(r'mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don\'t\(\)')
dd_ex = re.compile(r'do\(\)|don\'t\(\)')
a_sum = 0
b_sum = 0
dd = True
for line in input:
    while len(line) > 0:
        m: re.Match = re.search(all_ex, line)
        if not m:
            break
        dd_m = re.search(dd_ex, m.group())
        if dd_m:
            dd = bool(len(dd_m.group()) == 4)
        else:
            v = functools.reduce(lambda x, y: x * y, map(int, m.groups()), 1)
            a_sum += v
            b_sum += v * int(dd)
        line = line[m.span()[-1]:]

print(a_sum)
print(b_sum)
