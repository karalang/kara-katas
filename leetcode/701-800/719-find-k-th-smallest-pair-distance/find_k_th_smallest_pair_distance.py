# LeetCode #719: Find K-th Smallest Pair Distance -- binary search on
# the distance.
#
# A mirror of find_k_th_smallest_pair_distance.kara (the ★ arm) and its
# harness.


def smallest_distance_pair(nums, k):
    s = sorted(nums)
    n = len(s)
    lo, hi = 0, s[-1] - s[0]
    while lo < hi:
        mid = (lo + hi) // 2
        count = 0
        left = 0
        for right in range(n):
            while s[right] - s[left] > mid:
                left += 1
            count += right - left
        if count >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_nums(seed, n, top):
    out = []
    for _ in range(n):
        hi = next_random(seed)
        lo = next_random(seed)
        out.append((hi * 32768 + lo) % (top + 1))
    return out


def show(nums, k):
    print(f"{nums}, k = {k} -> {smallest_distance_pair(nums, k)}")


def main():
    show([1, 3, 1], 1)
    show([1, 1, 1], 2)
    show([1, 6, 1], 3)
    show([0, 1000000], 1)
    show([5, 5], 1)
    show([9, 4, 7, 1, 10], 1)
    show([9, 4, 7, 1, 10], 5)
    show([9, 4, 7, 1, 10], 10)
    seed = [719]
    a = random_nums(seed, 400, 1000000)
    pairs = 400 * 399 // 2
    print(f"400 numbers to 10^6: k = 1 -> {smallest_distance_pair(a, 1)}, middle -> {smallest_distance_pair(a, pairs // 2)}, last -> {smallest_distance_pair(a, pairs)}")
    b = random_nums(seed, 400, 10)
    print(f"400 numbers to 10: k = 1 -> {smallest_distance_pair(b, 1)}, middle -> {smallest_distance_pair(b, pairs // 2)}, last -> {smallest_distance_pair(b, pairs)}")
    total = 0
    for _ in range(300):
        n = 2 + next_random(seed) % 40
        top = next_random(seed) % 50
        nums = random_nums(seed, n, top)
        k = 1 + next_random(seed) % (n * (n - 1) // 2)
        total = (total * 131 + smallest_distance_pair(nums, k)) % 1000000007
    print(f"300 random arrays: checksum {total}")


main()
