# LeetCode #2321: Maximum Score Of Spliced Array -- the bench, the ★ arm
# in Python. Each array's sum plus the largest subarray sum of the
# differences the other array would bring, by Kadane's walk, both ways
# round. O(n).


def best_gain(into, frm):
    best = 0
    here = 0
    for i in range(len(into)):
        here = max(here + frm[i] - into[i], 0)
        best = max(best, here)
    return best


def maximums_spliced_array(nums1, nums2):
    sum1 = sum(nums1)
    sum2 = sum(nums2)
    return max(sum1 + best_gain(nums1, nums2), sum2 + best_gain(nums2, nums1))


seed = 2321


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 100000
    firsts = []
    seconds = []
    for _ in range(10):
        firsts.append([next_random() % 10000 + 1 for _ in range(n)])
        seconds.append([next_random() % 10000 + 1 for _ in range(n)])
    check = 0
    for _ in range(200):
        for k in range(10):
            i = next_random() % n
            firsts[k][i] = next_random() % 10000 + 1
            check = (check * 31 + maximums_spliced_array(firsts[k], seconds[k])) % 1000000007
    print(f"200 passes over 10 pairs of 10^5 numbers: checksum {check}")


main()
