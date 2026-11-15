# LeetCode #2200: Find All K-Distant Indices in an Array -- Python mirror of
# distant.kara (the ★ arm): one pass over the key's positions, each
# covering the indices up to k on either side, a `nxt` index not yet
# listed keeping an index from being listed twice. O(n).


def find_k_distant_indices(nums, key, k):
    n = len(nums)
    out = []
    nxt = 0
    for j in range(n):
        if nums[j] != key:
            continue
        frm = j - k if j - k > nxt else nxt
        to = j + k if j + k < n - 1 else n - 1
        out.extend(range(frm, to + 1))
        nxt = to + 1
    return out


# ---- test harness ---------------------------------------------------------

seed = 2200


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def fmt(v):
    return "[" + ", ".join(map(str, v)) + "]"


def show(nums, key, k):
    print(f"{fmt(nums)}, key {key}, k {k} -> {fmt(find_k_distant_indices(nums, key, k))}")


def main():
    show([3, 4, 9, 1, 3, 9, 5], 9, 1)
    show([2, 2, 2, 2, 2], 2, 2)
    show([5, 1, 1, 1, 5, 1, 1, 1], 5, 1)
    show([7, 1, 1, 1, 1, 1, 7], 7, 2)
    show([4, 1, 1, 4, 1, 1, 4], 4, 1)
    show([1, 2, 3], 3, 5)
    listed = 0
    check = 0
    for rnd in range(3000):
        n = next_random() % 50 + 1
        top = [2, 5, 1000][rnd % 3]
        nums = [next_random() % top + 1 for _ in range(n)]
        key = nums[next_random() % n]
        k = next_random() % n + 1
        out = find_k_distant_indices(nums, key, k)
        listed += len(out)
        for i in out:
            check = (check * 31 + i + 1) % 1000000007
        check = (check * 31 + len(out)) % 1000000007
    print(f"3000 arrays: {listed} listed, checksum {check}")
    wide = [next_random() % 100 + 1 for _ in range(1000)]
    out = find_k_distant_indices(wide, 7, 3)
    print(f"1000 numbers, key 7, k 3: {len(out)} listed, sum {sum(out)}")


main()
