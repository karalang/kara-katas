# LeetCode #1052: Grumpy Bookstore Owner -- Python mirror of grumpy.kara.
#
# The same slide: the calm minutes' customers counted once, and a window of
# the technique's length slid along the day keeping the most it saves.


def max_satisfied(customers, grumpy, minutes):
    base = 0
    saved = 0
    best = 0
    for i in range(len(customers)):
        if grumpy[i] == 0:
            base += customers[i]
        else:
            saved += customers[i]
        if i >= minutes and grumpy[i - minutes] == 1:
            saved -= customers[i - minutes]
        best = max(best, saved)
    return base + best


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_day(n, most, grumpy_one_in):
    customers = []
    grumpy = []
    for _ in range(n):
        customers.append(next_random() % (most + 1))
        grumpy.append(1 if next_random() % grumpy_one_in == 0 else 0)
    minutes = next_random() % n + 1
    return customers, grumpy, minutes


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    global seed
    examples = [
        ([1, 0, 1, 2, 1, 1, 7, 5], [0, 1, 0, 1, 0, 1, 0, 1], 3),
        ([1], [0], 1),
        ([4], [1], 1),
        ([2, 6, 6, 9], [0, 0, 1, 1], 1),
        ([3, 3, 3], [1, 1, 1], 3),
        ([3, 3, 3], [1, 1, 1], 2),
        ([0, 0, 0], [1, 1, 1], 2),
        ([5, 1, 1, 1, 5], [1, 0, 0, 0, 1], 4),
        ([1, 2, 3, 4, 5], [1, 0, 1, 0, 1], 2),
        ([10, 1, 7], [0, 0, 0], 2),
    ]
    for customers, grumpy, minutes in examples:
        print(f"{show(customers)} {show(grumpy)} {minutes} -> {max_satisfied(customers, grumpy, minutes)}")
    seed = 1052
    total = 0
    check = 0
    for _ in range(3000):
        n = next_random() % 10 + 1
        customers, grumpy, minutes = random_day(n, 5, 2)
        answer = max_satisfied(customers, grumpy, minutes)
        total += answer
        check = (check * 131 + answer) % 1000000007
    print(f"3000 random days of 1 to 10 minutes: total {total}, checksum {check}")
    total = 0
    check = 0
    for _ in range(300):
        n = next_random() % 1000 + 1
        customers, grumpy, minutes = random_day(n, 1000, 3)
        answer = max_satisfied(customers, grumpy, minutes)
        total += answer
        check = (check * 131 + answer) % 1000000007
    print(f"300 random days of 1 to 1000 minutes: total {total}, checksum {check}")
    customers, grumpy, _ = random_day(20000, 1000, 2)
    for minutes in [1, 100, 20000]:
        print(f"20000 minutes, a technique of {minutes} -> {max_satisfied(customers, grumpy, minutes)}")


main()
