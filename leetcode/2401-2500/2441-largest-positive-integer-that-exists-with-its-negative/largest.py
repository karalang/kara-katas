# LeetCode #2441: Largest Positive Integer That Exists With Its Negative
# -- Python mirror of the ★ arm (largest.kara): a table of 2001 flags,
# offset by 1000, and the largest magnitude whose negative was seen.


def find_max_k(nums):
    seen = [False] * 2001
    best = -1
    for x in nums:
        if seen[1000 - x]:
            best = max(best, abs(x))
        seen[1000 + x] = True
    return best


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def nonzero(m):
    v = 1 + next_random() % m
    return v if next_random() % 2 == 0 else -v


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    global seed
    for nums in ([-1, 2, -3, 3], [-1, 10, 6, 7, -7, 1], [-10, 8, 6, 7, -2, -3],
                 [1000, -1000], [-1000], [4, 4, 4, -3]):
        print(f"{show(nums)}: {find_max_k(nums)}")
    seed = 2441
    paired = []
    for v in range(1, 501):
        paired.append(v)
        paired.append(499 if v == 500 else -v)
    print(f"paired: {find_max_k(paired)}")
    random = [nonzero(1000) for _ in range(1000)]
    print(f"random: {find_max_k(random)}")
    check = 0
    total = 0
    for _ in range(3000):
        length = 1 + next_random() % 10
        nums = [nonzero(6) for _ in range(length)]
        answer = find_max_k(nums)
        check = (check * 31 + answer + 1) % 1000000007
        total += answer
    print(f"3000 random: checksum {check}, total {total}")


main()
