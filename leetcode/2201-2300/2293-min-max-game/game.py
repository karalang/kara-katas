# LeetCode #2293: Min Max Game -- the ★ arm's Python mirror. Play the
# rounds in place on the first half of the array.


def min_max_game(nums):
    a = list(nums)
    n = len(a)
    while n > 1:
        n //= 2
        for i in range(n):
            a[i] = min(a[2 * i], a[2 * i + 1]) if i % 2 == 0 else max(a[2 * i], a[2 * i + 1])
    return a[0]


# ---- test harness ---------------------------------------------------------

seed = 2293


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    cases = [
        [1, 3, 5, 2, 4, 8, 2, 2],
        [3],
        [7, 2],
        [1, 2, 3, 4, 5, 6, 7, 8],
        [8, 7, 6, 5, 4, 3, 2, 1],
        [4, 4, 4, 4],
        [1000000000, 1, 1, 1000000000],
    ]
    for nums in cases:
        print(f"{len(nums)} numbers: {min_max_game(nums)}")
    check = 0
    total = 0
    for _ in range(3000):
        n = 1 << (next_random() % 11)
        nums = []
        for _ in range(n):
            hi = next_random()
            nums.append((hi * 32768 + next_random()) % 1000000000 + 1)
        last = min_max_game(nums)
        check = (check * 31 + last) % 1000000007
        total += last
    print(f"3000 arrays: checksum {check}, sum {total}")


main()
