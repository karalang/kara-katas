# LeetCode #2100: Find Good Days to Rob the Bank -- Python mirror of the ★
# arm's benchmark (good_days.kara): the same 100 schedules of 10^5 days,
# the two runs counted in two passes.


def good_days_to_rob_bank(security, time):
    n = len(security)
    before = [0] * n
    after = [0] * n
    for i in range(1, n):
        if security[i] <= security[i - 1]:
            before[i] = before[i - 1] + 1
    for i in range(n - 2, -1, -1):
        if security[i] <= security[i + 1]:
            after[i] = after[i + 1] + 1
    return [i for i in range(n) if before[i] >= time and after[i] >= time]


seed = 2100


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


total = 0
check = 0
for _ in range(100):
    guards = 50000
    security = []
    for _ in range(100000):
        guards = min(max(guards + next_random() % 3 - 1, 0), 100000)
        security.append(guards)
    time = next_random() % 8
    good = good_days_to_rob_bank(security, time)
    total += len(good)
    for d in good:
        check = (check * 31 + d + 1) % 1000000007
print(f"100 answers: {total} good days, checksum {check}")
