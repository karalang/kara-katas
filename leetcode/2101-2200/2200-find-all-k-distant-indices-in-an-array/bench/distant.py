# benchmark's Python mirror of distant.kara (LeetCode #2200, the ★ arm): the
# key's windows, a `nxt` index.


def find_k_distant_indices(nums, key, k):
    n = len(nums)
    out = []
    nxt = 0
    for j in range(n):
        if nums[j] != key:
            continue
        frm = j - k if j - k > nxt else nxt
        to = j + k if j + k < n - 1 else n - 1
        for i in range(frm, to + 1):
            out.append(i)
        nxt = to + 1
    return out


seed = 2200


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    cases = []
    for c in range(1000):
        top = [50, 200, 1000][c % 3]
        nums = [next_random() % top + 1 for _ in range(1000)]
        key = nums[next_random() % 1000]
        k = next_random() % 20 + 1
        cases.append((nums, key, k))
    check = 0
    for _ in range(600):
        for nums, key, k in cases:
            out = find_k_distant_indices(nums, key, k)
            check = (check * 31 + len(out)) % 1000000007
            if out:
                check = (check * 31 + out[len(out) // 2]) % 1000000007
    print(f"600 passes over 1000 arrays: checksum {check}")


main()
