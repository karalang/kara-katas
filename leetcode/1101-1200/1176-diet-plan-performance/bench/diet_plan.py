# LeetCode #1176: Diet Plan Performance -- the ★ arm's bench in Python: one
# window of k days slid across the plan, its sum kept as it goes, each
# window scored as it is reached. The same plan and the same 2000 calls.


def diet_plan_performance(calories, k, lower, upper):
    points = 0
    total = 0
    for i, c in enumerate(calories):
        total += c
        if i >= k:
            total -= calories[i - k]
        if i >= k - 1:
            if total < lower:
                points -= 1
            elif total > upper:
                points += 1
    return points


seed = 1176


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


calories = [next_random() % 20001 for _ in range(100000)]
calls = 2000
check = 0
for _ in range(calls):
    k = 1 + next_random() % 100000
    mean = 10000 * k
    spread = next_random() % 100 * k
    p = diet_plan_performance(calories, k, mean - spread, mean + spread)
    check = (check * 131 + p + 100000) % 1000000007
print(f"{calls} calls: checksum {check}")
