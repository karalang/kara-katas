# LeetCode #1169 mirror of the Kāra ★ arm: the transactions grouped by name,
# and every pair in a group compared.
import sys


def invalid_transactions(transactions):
    by_name = {}
    rows = []
    for i, t in enumerate(transactions):
        name, time, amount, city = t.split(',')
        rows.append((name, int(time), int(amount), city))
        by_name.setdefault(name, []).append(i)
    out = []
    for i, (name, time, amount, city) in enumerate(rows):
        bad = amount > 1000
        if not bad:
            for j in by_name[name]:
                if abs(rows[j][1] - time) <= 60 and rows[j][3] != city:
                    bad = True
                    break
        if bad:
            out.append(transactions[i])
    return out


def literal(transactions):
    rows = [t.split(',') for t in transactions]
    out = []
    for i, (n, t, a, c) in enumerate(rows):
        if int(a) > 1000 or any(j != i and rows[j][0] == n and abs(int(rows[j][1]) - int(t)) <= 60 and rows[j][3] != c for j in range(len(rows))):
            out.append(transactions[i])
    return out


F = literal if len(sys.argv) > 1 and sys.argv[1] == 'lit' else invalid_transactions
state = [1169]


def rnd():
    state[0] = (state[0] * 1103515245 + 12345) % 2147483648
    return state[0] // 65536


def digest(lines):
    h = 0
    for line in lines:
        for b in line.encode():
            h = (h * 131 + b) % 1000000007
        h = (h * 131 + 10) % 1000000007
    return h


def show(ts):
    got = sorted(F(ts))
    print(f"{len(ts)} -> {len(got)}: {', '.join(got)}")


show(["alice,20,800,mtv", "alice,50,100,beijing"])
show(["alice,20,800,mtv", "alice,50,1200,mtv"])
show(["alice,20,800,mtv", "bob,50,1200,mtv"])
show(["ann,0,5,rome", "ann,60,5,oslo", "ann,121,5,rome"])
show(["ann,10,1000,rome", "ann,10,1001,rome", "bo,10,5,rome", "bo,10,5,rome"])
show(["ann,5,1,rome", "ann,5,1,rome", "ann,65,1,oslo", "cy,5,1,oslo"])
show(["zed,1000,2000,x"])
names = ["ann", "bo", "cy", "dee"]
cities = ["rome", "oslo", "lima", "pune"]
count = 0
check = 0
for i in range(300):
    n = 1 + rnd() % 40
    span = 200 if i % 2 == 0 else 1001
    ts = []
    for _ in range(n):
        name = names[rnd() % 3]
        time = rnd() % span
        amount = rnd() % 2001 if rnd() % 4 == 0 else rnd() % 1001
        city = cities[rnd() % 3]
        ts.append(f"{name},{time},{amount},{city}")
    got = sorted(F(ts))
    count += len(got)
    check = (check * 31 + digest(got)) % 1000000007
print(f"300 random lists: {count} invalid, checksum {check}")
ts = []
for _ in range(1000):
    ts.append(f"p{rnd() % 100},{rnd() % 1001},{rnd() % 1101},{cities[rnd() % 2]}")
got = sorted(invalid_transactions(ts))
print(f"1000 transactions by 100 names: {len(got)} invalid, checksum {digest(got)}")
ts = [f"ann,{i},5,rome" for i in range(999)] + ["ann,500,5,oslo"]
got = sorted(invalid_transactions(ts))
print(f"one name, one city but one: {len(got)} invalid, checksum {digest(got)}")
