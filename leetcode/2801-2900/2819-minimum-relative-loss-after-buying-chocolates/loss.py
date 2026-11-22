# LeetCode #2819: Minimum Relative Loss After Buying Chocolates -- the
# Python mirror of the ★ arm: the prices sorted, prefix sums, and for each
# query a binary search for how many of the m to take from the cheap end.


def minimum_relative_losses(prices, queries):
    s = sorted(prices)
    n = len(s)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + s[i]
    out = []
    for k, m in queries:
        lo, hi = 0, m
        while lo < hi:
            mid = (lo + hi) // 2
            if s[mid] + s[n - m + mid] < 2 * k:
                lo = mid + 1
            else:
                hi = mid
        dear = prefix[n] - prefix[n - m + lo]
        out.append(prefix[lo] + 2 * k * (m - lo) - dear)
    return out


# ---- the harness: the same in every arm --------------------------------

seed = 2819


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def fold(check, answers):
    for a in answers:
        check = (check * 31 + a) % 1000000007
    return check


def show(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


def main():
    print(show(minimum_relative_losses([1, 9, 22, 10, 19], [[18, 4], [5, 2]])))
    print(show(minimum_relative_losses([1, 5, 4, 3, 7, 11, 9], [[5, 4], [5, 7], [7, 3], [4, 5]])))
    print(show(minimum_relative_losses([5, 6, 7], [[10, 1], [5, 3], [3, 3]])))
    print(show(minimum_relative_losses([7], [[7, 1], [3, 1]])))
    rising = [i * 1000 + 1 for i in range(2000)]
    asked = [[q * 10000 + 1, 1000] for q in range(200)]
    print(fold(0, minimum_relative_losses(rising, asked)))
    check = 0
    for _ in range(3000):
        n = next_random() % 10 + 1
        prices = [next_random() % 30 + 1 for _ in range(n)]
        queries = []
        for _ in range(3):
            k = next_random() % 30 + 1
            queries.append([k, next_random() % n + 1])
        check = fold(check, minimum_relative_losses(prices, queries))
    print(f"3000 small shops: checksum {check}")
    check = 0
    for _ in range(50):
        n = next_random() % 1000 + 1
        prices = [wide() % 1000000000 + 1 for _ in range(n)]
        queries = []
        for _ in range(50):
            k = wide() % 1000000000 + 1
            queries.append([k, next_random() % n + 1])
        check = fold(check, minimum_relative_losses(prices, queries))
    print(f"50 large shops: checksum {check}")


main()
