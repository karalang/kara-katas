"""LeetCode 215 — Kth Largest Element, bounded-heap form.

Mirror of kth_largest_heap.kara: keep a min-heap of the k largest values seen
and answer from its root. O(n log k) time, O(k) space, and the input is never
reordered.

heapq is a MIN-heap, which is what this wants directly — the smallest of the k
kept values is both the eviction candidate and, once k are held, the answer.
"""

import heapq


def find_kth_largest(nums, k):
    keep = []
    for v in nums:
        heapq.heappush(keep, v)
        if len(keep) > k:
            heapq.heappop(keep)
    return keep[0] if keep else 0


def report(nums, k):
    print(find_kth_largest(nums, k))


def main():
    report([3, 2, 1, 5, 6, 4], 2)          # 5
    report([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) # 4
    report([1], 1)                         # 1
    report([2, 1], 2)                      # 1
    report([7, 6, 5, 4, 3, 2, 1], 3)       # 5
    report([1, 2, 3, 4, 5, 6], 1)          # 6
    report([5, 5, 5, 5], 2)                # 5
    report([-1, -5, 3, 0, 2], 1)           # 3
    report([-1, -5, 3, 0, 2], 5)           # -5


if __name__ == "__main__":
    main()
