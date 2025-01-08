inp = open("d1.txt").read()
l = []
r = []
for row in inp.splitlines():
    if not row:
        continue
    a, b = [int(x) for x in row.split("   ")]
    l.append(a)
    r.append(b)

sim_score = 0
for ll in l:
    c = r.count(ll)
    if c:
        print(ll, c, c * ll)
    sim_score += c * ll

print(sim_score)