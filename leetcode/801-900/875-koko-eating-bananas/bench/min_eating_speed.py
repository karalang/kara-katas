# LeetCode #875 bench: Python mirror of min_eating_speed.kara (the ★ arm,
# binary search on the speed) on the same 600 searches.


def min_eating_speed(piles, h):
    lo = 1
    hi = max(1, max(piles))
    while lo < hi:
        k = (lo + hi) // 2
        if hours(piles, k) <= h:
            hi = k
        else:
            lo = k + 1
    return lo


def hours(piles, k):
    total = 0
    for p in piles:
        total += (p + k - 1) // k
    return total


seed = 875


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def up_to(limit):
    a = next_random()
    b = next_random()
    return (a * 32768 + b) % limit + 1


def main():
    pile_sets = []
    for k in range(20):
        limit = 1000000000 if k % 2 == 0 else 1000000
        pile_sets.append([up_to(limit) for _ in range(10000)])
    total = 0
    check = 0
    for k in range(600):
        h = 10000 + up_to(1000000000 - 10000 if k % 3 == 0 else 1000000) - 1
        answer = min_eating_speed(pile_sets[k % 20], h)
        total += answer
        check = (check * 131 + answer) % 1000000007
    print(f"600 searches over 10000 piles: speeds sum to {total}, checksum {check}")


main()
