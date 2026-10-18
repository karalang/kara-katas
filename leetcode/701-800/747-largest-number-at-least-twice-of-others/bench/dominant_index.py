# LeetCode 747 — Largest Number At Least Twice of Others, bench: the ★
# arm (one pass) on millions of 50-value lists cut from a random pool.
# Mirrors dominant_index.kara.


def dominant_index(nums):
    best = 0
    second = -1
    for i in range(1, len(nums)):
        if nums[i] > nums[best]:
            second = nums[best]
            best = i
        elif nums[i] > second:
            second = nums[i]
    return best if nums[best] >= 2 * second else -1


seed = 747


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    queries = 2000000
    pool_len = 100000
    n = 50
    pool = [next_random() % 52 for _ in range(pool_len)]
    nums = [0] * n
    found = 0
    total = 0
    for q in range(queries):
        start = next_random() % (pool_len - n)
        for j in range(n):
            nums[j] = pool[start + j]
        nums[q % n] = 100
        got = dominant_index(nums)
        if got != -1:
            found += 1
            total += got
    print(f"{queries} lists of 50 values: {found} have a dominant value, indices sum to {total}")


main()
