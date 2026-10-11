# Benchmark for #373 -- mirror of k_smallest_pairs.kara.

import heapq


def k_smallest_pairs(nums1, nums2, k):
    out = []
    if not nums1 or not nums2:
        return out
    fronts = []
    for i in range(min(len(nums1), k)):
        heapq.heappush(fronts, (nums1[i] + nums2[0], i, 0))
    while len(out) < k and fronts:
        _, i, j = heapq.heappop(fronts)
        out.append((nums1[i], nums2[j]))
        if j + 1 < len(nums2):
            heapq.heappush(fronts, (nums1[i] + nums2[j + 1], i, j + 1))
    return out


def rem(a, m):
    # Kāra's % truncates toward zero, as C, Rust and Go do.
    r = abs(a) % m
    return -r if a < 0 else r


def main():
    seed = 373
    checksum = 0
    nums1 = [0] * 100000
    nums2 = [0] * 100000
    for _ in range(20):
        v = -1000000000
        for i in range(100000):
            seed = (seed * 1103515245 + 12345) % 2147483648
            v += (seed // 65536) % 20000
            nums1[i] = v
        v = -1000000000
        for i in range(100000):
            seed = (seed * 1103515245 + 12345) % 2147483648
            v += (seed // 65536) % 20000
            nums2[i] = v
        for u, w in k_smallest_pairs(nums1, nums2, 10000):
            checksum = (checksum * 31 + rem(u + w, 1000000007) + 2000000000) % 1000000007
    print(f"checksum {checksum}")


main()
