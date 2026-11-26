# LeetCode #1480: Running Sum of 1d Array -- Python mirror of
# running_sum.kara: one pass, each sum the one before it and the value at
# its place


def running_sum(nums):
    sums = []
    total = 0
    for x in nums:
        total += x
        sums.append(total)
    return sums


# ---- test harness ---------------------------------------------------------

seed = 1480


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    hi = next_random()
    return hi * 32768 + next_random()


def draw(n, top):
    return [wide_random() % (2 * top + 1) - top for _ in range(n)]


def show(v):
    return "[" + ",".join(str(x) for x in v) + "]"


def main():
    print(show(running_sum([1, 2, 3, 4])))
    print(show(running_sum([1, 1, 1, 1, 1])))
    print(show(running_sum([3, 1, 2, 10, 1])))
    print(show(running_sum([-7])))
    print(show(running_sum([5, -5, 5, -5, 0])))
    up = running_sum([1000000] * 1000)
    down = running_sum([-1000000] * 1000)
    swing = running_sum([1000000 if i % 2 == 0 else -1000000 for i in range(1000)])
    print(f"1000 values: {up[999]} {down[999]} {swing[998]} {swing[999]}")
    check = 0
    count = 0
    for _ in range(3000):
        n = 1 + next_random() % 1000
        top = wide_random() % 1000001
        for x in running_sum(draw(n, top)):
            check = (check * 31 + x + 1000000007) % 1000000007
            count += 1
    print(f"3000 random arrays: {count} sums, checksum {check}")


main()
