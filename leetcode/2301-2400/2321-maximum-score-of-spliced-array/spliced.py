# LeetCode #2321: Maximum Score Of Spliced Array -- the ★ arm in Python.
# Swapping a subarray of `nums1` into `nums2` adds the subarray's
# differences to its sum, so the best for each array is its sum plus the
# largest subarray sum of the differences, by Kadane's walk, or nothing.
# Both ways round, the larger. O(n).


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


def numbers(n, top):
    return [next_random() % top + 1 for _ in range(n)]


def main():
    print(maximums_spliced_array([60, 60, 60], [10, 90, 10]))
    print(maximums_spliced_array([20, 40, 20, 70, 30], [50, 20, 50, 40, 20]))
    print(maximums_spliced_array([7, 11, 13], [1, 1, 1]))
    print(maximums_spliced_array([3], [8]))
    print(maximums_spliced_array([5, 1, 5], [1, 9, 1]))
    a = numbers(1000, 10000)
    b = numbers(1000, 10000)
    print(maximums_spliced_array(a, b))
    check = 0
    total = 0
    for _ in range(2000):
        n = next_random() % 30 + 1
        a = numbers(n, 20)
        b = numbers(n, 20)
        score = maximums_spliced_array(a, b)
        check = (check * 31 + score) % 1000000007
        total += score
    print(f"2000 pairs: checksum {check}, {total} in all")


main()
