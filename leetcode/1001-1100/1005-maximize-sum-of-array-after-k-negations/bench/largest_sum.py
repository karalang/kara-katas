# Benchmark: LeetCode #1005 Maximize Sum Of Array After K Negations -- the
# ★ arm, counting, on arrays of 10000 numbers, LeetCode's longest.
# Mirrors largest_sum.kara, .c, .rs and go-seq/.


def largest_sum_after_k_negations(nums, k):
    count = [0] * 201
    for x in nums:
        count[x + 100] += 1
    left = k
    v = -100
    while v < 0 and left > 0:
        flip = min(count[v + 100], left)
        count[v + 100] -= flip
        count[100 - v] += flip
        left -= flip
        v += 1
    total = 0
    for v in range(-100, 101):
        total += v * count[v + 100]
    if left % 2 == 1:
        smallest = 0
        while count[smallest + 100] == 0:
            smallest += 1
        total -= 2 * smallest
    return total


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    rounds = 2500
    n = 10000
    seed = [1005]
    arrays = []
    for t in range(20):
        nums = []
        for _ in range(n):
            size = next_random(seed) % 101
            nums.append(-size if next_random(seed) % 8 < t % 7 + 1 else size)
        arrays.append(nums)
    total = 0
    check = 0
    for r in range(rounds):
        for i in range(20):
            t = (r + i) % 20
            k = 1 + (r * 37 + t * 101) % 10000
            got = largest_sum_after_k_negations(arrays[t], k)
            total += got
            check = (check * 31 + got % 1000000007 + 1000000007) % 1000000007
    print(f"{rounds} rounds over 20 arrays of {n} numbers: answers sum to {total}, checksum {check}")


main()
