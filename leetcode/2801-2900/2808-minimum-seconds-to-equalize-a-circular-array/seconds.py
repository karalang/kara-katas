# LeetCode #2808: Minimum Seconds to Equalize a Circular Array -- the
# Python mirror of the ★ arm: each value's places gathered, its widest
# gap round the circle halved, and the least of those the answer.


def minimum_seconds(nums):
    n = len(nums)
    places = {}
    for i, v in enumerate(nums):
        places.setdefault(v, []).append(i)
    best = n
    for at in places.values():
        widest = at[0] + n - at[-1]
        for k in range(1, len(at)):
            widest = max(widest, at[k] - at[k - 1])
        best = min(best, widest // 2)
    return best


seed = 2808


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    print(minimum_seconds([1, 2, 1, 2]))
    print(minimum_seconds([2, 1, 3, 3, 2]))
    print(minimum_seconds([5, 5, 5, 5]))
    n = 100000
    print(minimum_seconds([i + 1 for i in range(n)]))
    print(minimum_seconds([7 if i % 3 == 0 else i + 10 for i in range(n)]))
    total = 0
    check = 0
    for _ in range(3000):
        m = next_random() % 12 + 1
        a = minimum_seconds([next_random() % 4 + 1 for _ in range(m)])
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"3000 small arrays: seconds sum to {total}, checksum {check}")
    total = 0
    check = 0
    for t in range(50):
        m = wide() % n + 1
        top = 10 if t % 2 == 0 else 1000000000
        a = minimum_seconds([wide() % top + 1 for _ in range(m)])
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"50 large arrays: seconds sum to {total}, checksum {check}")


main()
