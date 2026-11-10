# LeetCode #2100: Find Good Days to Rob the Bank -- Python mirror of the ★
# arm (good_days.kara): days in a row without a rise before each day and
# without a fall after it, counted in two passes.


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


# ---- test harness -----------------------------------------------------------

seed = 2100


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    hi = next_random()
    return hi * 32768 + next_random()


def show(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


examples = [
    ([5, 3, 3, 3, 5, 6, 2], 2),
    ([1, 1, 1, 1, 1], 0),
    ([1, 2, 3, 4, 5, 6], 2),
    ([7], 0),
    ([7], 1),
    ([3, 2, 1, 2, 3, 2, 1, 2, 3], 2),
    ([4, 4, 0, 4, 4], 2),
]
for security, time in examples:
    print(f"{show(security)} time={time} -> {show(good_days_to_rob_bank(security, time))}")
days = 0
check = 0
for round_ in range(3000):
    n = next_random() % 30 + 1
    top = 4 if round_ % 2 == 0 else 100001
    security = [wide_random() % top for _ in range(n)]
    time = next_random() % 6
    good = good_days_to_rob_bank(security, time)
    days += len(good)
    for d in good:
        check = (check * 31 + d + 1) % 1000000007
    check = (check * 31 + 7) % 1000000007
print(f"3000 schedules: {days} good days, checksum {check}")
n = 100000
valleys = [abs(i % 2000 - 1000) // 2 for i in range(n)]
for time in [0, 1, 300, 999, 1000]:
    good = good_days_to_rob_bank(valleys, time)
    ends = f", first {good[0]}, last {good[-1]}" if good else ""
    print(f"valleys, time={time}: {len(good)} good days{ends}")
level = [100000] * n
good = good_days_to_rob_bank(level, 49999)
print(f"level, time=49999: {len(good)} good days, first {good[0]}, last {good[-1]}")
none = good_days_to_rob_bank(level, 100000)
print(f"level, time=100000: {len(none)} good days")
