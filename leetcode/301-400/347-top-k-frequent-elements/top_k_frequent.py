"""LeetCode 347 — Top K Frequent Elements (reference oracle).

Same tally / keys-walk / (count desc, value asc) ordering as the Kara version.
"""


def top_k_frequent(nums, k):
    counts = {}
    for v in nums:
        counts[v] = counts.get(v, 0) + 1
    vals = list(counts.keys())
    vals.sort(key=lambda v: (-counts[v], v))
    return vals[:k]


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
