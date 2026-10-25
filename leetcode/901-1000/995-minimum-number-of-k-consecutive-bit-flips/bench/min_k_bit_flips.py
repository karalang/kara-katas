# Benchmark: LeetCode #995 Minimum Number of K Consecutive Bit Flips --
# the ★ arm, the greedy with a running parity, on random arrays of
# 100000 bits, LeetCode's largest. Mirrors min_k_bit_flips.kara, .rs, .c
# and go-seq/.


def min_k_bit_flips(nums, k):
    n = len(nums)
    ends = [False] * (n + 1)
    flipped = False
    flips = 0
    for i in range(n):
        if ends[i]:
            flipped = not flipped
        if (nums[i] == 1) == flipped:
            if i + k > n:
                return -1
            flips += 1
            flipped = not flipped
            ends[i + k] = True
    return flips


seed = 995


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds = 50
    # ten arrays of random bits and ten of ones put through random flips
    # of 1 to 100 bits, which can be made all ones again
    arrays = []
    for a in range(20):
        if a % 2 == 0:
            nums = [next_random() % 2 for _ in range(100000)]
        else:
            k = 1 + next_random() % 100
            nums = [1] * 100000
            for i in range(100000 - k + 1):
                if next_random() % 4 == 0:
                    for j in range(i, i + k):
                        nums[j] = 1 - nums[j]
        arrays.append((nums, k if a % 2 == 1 else 1 + next_random() % 100))
    stuck = 0
    total = 0
    check = 0
    for r in range(rounds):
        for i in range(20):
            nums, k = arrays[(r + i) % 20]
            got = min_k_bit_flips(nums, k)
            if got < 0:
                stuck += 1
            else:
                total += got
            check = (check * 31 + got + 2) % 1000000007
    print(f"{rounds} rounds over 20 arrays of 100000 bits: {stuck} impossible, {total} flips, checksum {check}")


main()
