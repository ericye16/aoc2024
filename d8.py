from collections import defaultdict
import math

inpt = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""
inpt = open("d8.txt").read()

inpt = inpt.splitlines()

def parsemap(inpt: list[str]) -> dict[str, list[tuple[int, int]]]:
    d = defaultdict(list)
    for i, line in enumerate(inpt):
        for j, char in enumerate(line):
            if char != '.':
                d[char].append((i, j))
    return d

m = parsemap(inpt)
def generate_antinodes(a: tuple[int, int], b: tuple[int, int]) -> list[tuple[int, int]]:
    vec = (b[0] - a[0], b[1] - a[1])
    l = []
    l.append((b[0] + vec[0], b[1] + vec[1]))
    l.append((a[0] - vec[0], a[1] - vec[1]))
    return l

antinodes = []
for ant, l in m.items():
    for i, a in enumerate(l):
        for b in l[i+1:]:
            for an in generate_antinodes(a, b):
                antinodes.append(an)

# print(antinodes)


antinodes_s = set()
for an in antinodes:
    if an[0] >= 0 and an[0] < len(inpt) and an[1] >= 0 and an[1] < len(inpt[0]):
        antinodes_s.add(an)
print(len(antinodes_s))
# print(m)


def generate_an2(a: tuple[int, int], b: tuple[int, int], bound1, bound2) -> list[tuple[int, int]]:
    vec = (b[0] - a[0], b[1] - a[1])
    gcd = math.gcd(vec[0], vec[1])
    vec = (vec[0] // gcd, vec[1] // gcd)
    l = []
    st = a
    while st[0] >= 0 and st[0] < bound1 and st[1] >= 0 and st[1] < bound2:
        l.append(st)
        st = (st[0] + vec[0], st[1] + vec[1])
    st = a
    while st[0] >= 0 and st[0] < bound1 and st[1] >= 0 and st[1] < bound2:
        l.append(st)
        st = (st[0] - vec[0], st[1] - vec[1])
    return l

antinodes = []
for ant, l in m.items():
    for i, a in enumerate(l):
        for b in l[i+1:]:
            for an in generate_an2(a, b, len(inpt), len(inpt[0])):
                antinodes.append(an)

for i in range(len(inpt)):
    for j in range(len(inpt[0])):
        if (i, j) in antinodes:
            print('#', end='')
        else:
            print(inpt[i][j], end='')
    print()

antinodes_s = set()
for an in antinodes:
    if an[0] >= 0 and an[0] < len(inpt) and an[1] >= 0 and an[1] < len(inpt[0]):
        antinodes_s.add(an)
print(len(antinodes_s))