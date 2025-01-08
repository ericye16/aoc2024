from functools import cache
from collections import defaultdict
initial = [125, 17]

initial = open("d11.txt").read().strip().split(" ")
initial = [int(x) for x in initial]

def iterate(inp):
    l = []
    for x in inp:
        if x == 0:
            l.append(1)
        elif len(str(x)) % 2 == 0:
            ll = len(str(x))
            l.append(int(str(x)[:ll // 2], 10))
            l.append(int(str(x)[ll // 2:], 10))
        else:
            l.append(x * 2024)
    return l

@cache
def cached_iterate(x):
    if x == 0:
        return [1]
    elif len(str(x)) % 2 == 0:
        ll = len(str(x))
        return [int(str(x)[:ll // 2], 10), int(str(x)[ll // 2:], 10)]
    else:
        return [x * 2024]

x = initial
# print(x)
# for it in range(25):
#     print("iteration: %d" % it)
#     x = iterate(x)
#     print(x)

# print(len(x))

x = initial

xd = defaultdict(int)
for xx in x:
    xd[xx] += 1

def iterate_cached(xd):
    new_outputs = defaultdict(int)
    for k, v in xd.items():
        for x in cached_iterate(k):
            new_outputs[x] += v
    return new_outputs

def lenitems(d):
    return sum(d.values())

for it in range(75):
    print("iteration: %d" % it)
    xd = iterate_cached(xd)
    print(lenitems(xd))