"""LeetCode #128: Longest Consecutive Sequence — Python oracle.

Length of the longest run of consecutive integers in an unsorted array, O(n)
via a hash set: a value starts a run iff value-1 is absent; count up from there.
"""


def longest_consecutive(nums):
    s = set(nums)
    best = 0
    for v in s:
        if v - 1 not in s:               # v is a run start
            length = 1
            cur = v
            while cur + 1 in s:
                cur += 1
                length += 1
            if length > best:
                best = length
    return best


def lcg(seed, n, mod):
    out = []
    x = seed
    for _ in range(n):
        x = (x * 1103515245 + 12345) & 0x7FFFFFFF
        out.append(x % mod)
    return out


def main():
    cases = [
        [100, 4, 200, 1, 3, 2],                        # 4  (1,2,3,4)
        [0, 3, 7, 2, 5, 8, 4, 6, 0, 1],                # 9  (0..8)
        [],                                            # 0
        [1, 2, 0, 1],                                  # 3  (0,1,2)
        [9, 1, 4, 7, 3, -1, 0, 5, 8, -1, 6],           # 7  (3..9)
        lcg(1, 500, 200),                              # clustered LCG values
        lcg(42, 800, 1000),
    ]
    MOD = 1000000007
    sink = 0
    for nums in cases:
        n = longest_consecutive(nums)
        print(f"len={len(nums)}: {n}")
        sink = (sink * 1000003 + n) % MOD
    print(f"sink: {sink}")


if __name__ == "__main__":
    main()
