# LeetCode #1176: Diet Plan Performance -- the mirror of the Kāra ★ arm: one
# window of k days slid across the plan, its sum kept as it goes, each
# window scored as it is reached. With `lit` as its argument it reads the
# statement literally instead: every run of k days summed afresh.
import sys

LIT = len(sys.argv) > 1 and sys.argv[1] == "lit"


def diet_plan_performance(calories, k, lower, upper):
    if LIT:
        points = 0
        for i in range(len(calories) - k + 1):
            t = sum(calories[i:i + k])
            points += -1 if t < lower else 1 if t > upper else 0
        return points
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


def main():
    f = diet_plan_performance
    print(f"example 1: {f([1, 2, 3, 4, 5], 1, 3, 3)}")
    print(f"example 2: {f([3, 2], 2, 0, 1)}")
    print(f"example 3: {f([6, 5, 0, 0], 2, 1, 5)}")
    print(f"one window: {f([4, 4, 4], 3, 13, 20)} {f([4, 4, 4], 3, 1, 11)}")
    print(f"at the bounds: {f([1, 2, 3, 4], 2, 3, 7)}")
    print(f"all zero: {f([0, 0, 0, 0, 0], 2, 0, 0)} {f([0, 0, 0, 0, 0], 2, 1, 1)}")
    check = 0
    points = 0
    for _ in range(300):
        n = 1 + next_random() % 40
        calories = [next_random() % 10 for _ in range(n)]
        k = 1 + next_random() % n
        lower = next_random() % (5 * k + 1)
        upper = lower + next_random() % (4 * k + 1)
        p = f(calories, k, lower, upper)
        points += p
        check = (check * 131 + p + 100000) % 1000000007
    print(f"300 random plans: {points} points, checksum {check}")
    calories = [next_random() % 20001 for _ in range(100000)]
    average = sum(calories) // 100000
    for k in [1, 317, 100000]:
        mean = average * k
        print(f"100000 days, k = {k}: {f(calories, k, mean - 40 * k, mean + 40 * k)}")


main()
