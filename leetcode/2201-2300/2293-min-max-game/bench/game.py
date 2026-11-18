# LeetCode #2293: Min Max Game -- the bench, the ★ arm's Python mirror.
# The rounds played in place on a copy of the array.


def min_max_game(nums):
    a = list(nums)
    n = len(a)
    while n > 1:
        n //= 2
        for i in range(n):
            a[i] = min(a[2 * i], a[2 * i + 1]) if i % 2 == 0 else max(a[2 * i], a[2 * i + 1])
    return a[0]


# ---- bench harness ---------------------------------------------------------

seed = 2293


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = []
    for _ in range(200):
        nums = []
        for _ in range(1024):
            hi = next_random()
            nums.append((hi * 32768 + next_random()) % 1000000000 + 1)
        arrays.append(nums)
    check = 0
    for _ in range(50):
        total = 0
        for nums in arrays:
            total += min_max_game(nums)
        check = (check * 31 + total) % 1000000007
    print(f"50 passes over 200 arrays of 1024: checksum {check}")


main()
