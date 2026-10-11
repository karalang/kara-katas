# LeetCode #373: Find K Pairs with Smallest Sums -- mirror of k_smallest_pairs.kara.

import heapq


def k_smallest_pairs(nums1, nums2, k):
    out = []
    if not nums1 or not nums2:
        return out
    fronts = [(nums1[i] + nums2[0], i, 0) for i in range(min(len(nums1), k))]
    heapq.heapify(fronts)
    while len(out) < k and fronts:
        _, i, j = heapq.heappop(fronts)
        out.append((nums1[i], nums2[j]))
        if j + 1 < len(nums2):
            heapq.heappush(fronts, (nums1[i] + nums2[j + 1], i, j + 1))
    return out


def show(label, nums1, nums2, k):
    print(f"{label}: {k_smallest_pairs(nums1, nums2, k)}")


def main():
    show("example 1", [1, 7, 11], [2, 4, 6], 3)
    show("example 2", [1, 1, 2], [1, 2, 3], 2)
    show("k above the pair count", [1, 2], [3], 3)
    show("k = 1", [-5, 0, 5], [-3, 3], 1)
    show("every pair", [1, 2], [10, 20], 4)
    show("negative values", [-10, -4, 0], [-7, -2, 8], 5)
    show("all equal", [3, 3, 3], [4, 4], 4)
    show("one row", [2], [1, 3, 5, 7], 3)
    show("one column", [1, 3, 5, 7], [2], 3)
    show("values at the bounds", [-1000000000, 1000000000], [-1000000000, 1000000000], 3)
    seed = 373
    checksum = 0
    pairs = 0
    for _ in range(300):
        seed = (seed * 1103515245 + 12345) % 2147483648
        n1 = 1 + (seed // 65536) % 300
        seed = (seed * 1103515245 + 12345) % 2147483648
        n2 = 1 + (seed // 65536) % 300
        seed = (seed * 1103515245 + 12345) % 2147483648
        k = 1 + (seed // 65536) % 2000
        nums1 = []
        nums2 = []
        v = -5000
        for _ in range(n1):
            seed = (seed * 1103515245 + 12345) % 2147483648
            v += (seed // 65536) % 40
            nums1.append(v)
        v = -5000
        for _ in range(n2):
            seed = (seed * 1103515245 + 12345) % 2147483648
            v += (seed // 65536) % 40
            nums2.append(v)
        out = k_smallest_pairs(nums1, nums2, k)
        pairs += len(out)
        for u, w in out:
            checksum = (checksum * 31 + u + 20000) % 1000000007
            checksum = (checksum * 31 + w + 20000) % 1000000007
    print(f"300 random cases: {pairs} pairs, checksum {checksum}")


main()
