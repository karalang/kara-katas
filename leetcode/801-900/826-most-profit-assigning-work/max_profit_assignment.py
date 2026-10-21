# LeetCode 826 — Most Profit Assigning Work, by two sorted sweeps.
#
# Mirrors max_profit_assignment.kara: sort the jobs by difficulty and the
# workers by ability, and walk the jobs with one pointer as the abilities
# grow, keeping the best profit among the jobs passed.

def max_profit_assignment(difficulty, profit, worker):
    n = len(difficulty)
    jobs = sorted(zip(difficulty, profit))
    nxt = 0
    best = 0
    total = 0
    for ability in sorted(worker):
        while nxt < n and jobs[nxt][0] <= ability:
            best = max(best, jobs[nxt][1])
            nxt += 1
        total += best
    return total

seed = 0
def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536

def fmt(v):
    return "[" + ", ".join(map(str, v)) + "]"

def show(d, p, w):
    print(f"{fmt(d)} {fmt(p)} {fmt(w)} -> {max_profit_assignment(d, p, w)}")

def draw(count, top):
    return [1 + next_random() % top for _ in range(count)]

show([2, 4, 6, 8, 10], [10, 20, 30, 40, 50], [4, 5, 6, 7])
show([85, 47, 57], [24, 66, 99], [40, 25, 25])
show([5], [7], [5])
show([5], [7], [4])
show([1, 2, 3], [30, 20, 10], [3, 3, 1])
show([4, 4, 2], [5, 9, 1], [4, 3, 100000])
show([10, 10, 10], [1, 2, 3], [9, 10, 11])
seed = 826
d = draw(10000, 100000)
p = draw(10000, 100000)
w = draw(10000, 100000)
print(f"10000 random jobs and workers -> {max_profit_assignment(d, p, w)}")
falling = [100001 - x for x in d]
print(f"10000 jobs, profit falling with difficulty -> {max_profit_assignment(d, falling, w)}")
total = 0
check = 0
for _ in range(300):
    n = 1 + next_random() % 12
    m = 1 + next_random() % 12
    dd = draw(n, 30)
    pp = draw(n, 50)
    ww = draw(m, 35)
    r = max_profit_assignment(dd, pp, ww)
    total += r
    check = (check * 131 + r) % 1000000007
print(f"300 random cases: total {total}, checksum {check}")
