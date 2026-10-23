# LeetCode #875: Koko Eating Bananas -- Python mirror of the ★ arm (binary
# search on the speed) and its test harness; prints the same output as
# min_eating_speed.kara.


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


# ---- test harness ----------------------------------------------------------

seed = 875


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def up_to(limit):
    hi = next_random()
    return (hi * 32768 + next_random()) % limit + 1


def show(piles, h):
    text = [str(p) for p in piles]
    shown = f"{text[0]}, {text[1]}, ... ({len(text)} piles)" if len(text) > 8 else ", ".join(text)
    print(f"piles = [{shown}], h = {h} -> {min_eating_speed(piles, h)}")


def main():
    show([3, 6, 7, 11], 8)
    show([30, 11, 23, 4, 20], 5)
    show([30, 11, 23, 4, 20], 6)
    show([1], 1)
    show([1000000000], 1)
    show([1000000000], 1000000000)
    show([1000000000], 999999999)
    show([5, 5, 5, 5], 7)
    show([1, 1, 1, 999999999], 10)
    big = [1000000000] * 10000
    show(big, 10000)
    show(big, 1000000000)
    total = 0
    for k in range(3000):
        n = k % 8 + 1
        piles = [next_random() % 20 + 1 for _ in range(n)]
        h = n + next_random() % 30
        total += min_eating_speed(piles, h)
    print(f"3000 sets of 1 to 8 piles: speeds sum to {total}")
    total = 0
    check = 0
    for k in range(20):
        limit = 1000000000 if k % 2 == 0 else 1000
        piles = [up_to(limit) for _ in range(10000)]
        h = 10000 + up_to(1000000000 - 10000 if k % 3 == 0 else 100000) - 1
        answer = min_eating_speed(piles, h)
        total += answer
        check = (check * 131 + answer) % 1000000007
    print(f"20 sets of 10000 piles: speeds sum to {total}, checksum {check}")


main()
