"""LeetCode 347 — Top K Frequent Elements, bounded-heap form.

Mirror of top_k_frequent_heap.kara: tally, then keep at most k candidates in a
min-heap ordered weakest-first, evicting whenever it overflows. O(d log k).

The Kāra version spells the comparison out in a hand-written `Ord` on a
`Weakest` struct. This mirror uses the key `(count, -value)` instead, which
gives the identical weakest-first order — lowest count first, larger value
first on a tie — because Python's ints are unbounded and the negation is safe.
The Kāra side cannot do that: `-i64.MIN` overflows and Kāra traps integer
overflow by default, the same reason kata #295's mirrors diverge here.
"""

import heapq
from collections import Counter


def top_k_frequent(nums, k):
    counts = Counter(nums)
    best = []
    for value, count in counts.items():
        heapq.heappush(best, (count, -value))
        if len(best) > k:
            heapq.heappop(best)
    # Ascending is weakest-first, so the answer is this reversed.
    ranked = sorted(best)
    return [-neg_value for _count, neg_value in reversed(ranked)]


def show(nums, k):
    got = top_k_frequent(nums, k)
    print(f"k={k} -> [{','.join(str(v) for v in got)}]")


def main():
    show([1, 1, 1, 2, 2, 3], 2)
    show([1], 1)
    show([4, 1, -1, 2, -1, 2, 3], 2)
    show([5, 5, 4, 4, 3, 3], 3)
    show([7, 7, 8], 5)


if __name__ == "__main__":
    main()
