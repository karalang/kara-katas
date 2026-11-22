# LeetCode #2808: Minimum Seconds to Equalize a Circular Array -- the
# bench in Python: the ★ arm over 20 arrays of 10^5 numbers from 1000
# values, all drawn first, then each answered 20 times.


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
    count = 20
    rounds = 20
    cases = [[wide() % 1000 * 1000003 + 1 for _ in range(100000)] for _ in range(count)]
    total = 0
    check = 0
    for r in range(rounds):
        for nums in cases:
            a = minimum_seconds(nums)
            total += a
            check = (check * 31 + a + r) % 1000000007
    print(f"{count} arrays of 10^5, {rounds} rounds: seconds sum to {total}, checksum {check}")


main()
