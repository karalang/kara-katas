"""LeetCode #15: 3Sum — sort + two-pointer, O(n^2).

Mirror of three_sum.kara: same sort-then-two-pointer shape, same duplicate
suppression (outer backward-look + inner skip-runs), same output format
(triplet count, then each triplet's three sorted values one per line) so the
two files diff line-for-line.
"""


def three_sum(nums: list[int]) -> list[list[int]]:
    s = sorted(nums)
    n = len(s)
    result: list[list[int]] = []
    i = 0
    while i < n - 2:
        if i > 0 and s[i] == s[i - 1]:
            i += 1
            continue
        if s[i] > 0:
            break
        lo, hi = i + 1, n - 1
        while lo < hi:
            total = s[i] + s[lo] + s[hi]
            if total < 0:
                lo += 1
            elif total > 0:
                hi -= 1
            else:
                result.append([s[i], s[lo], s[hi]])
                lo += 1
                hi -= 1
                while lo < hi and s[lo] == s[lo - 1]:
                    lo += 1
                while lo < hi and s[hi] == s[hi + 1]:
                    hi -= 1
        i += 1
    return result


def report(nums: list[int]) -> None:
    triplets = three_sum(nums)
    print(len(triplets))
    for t in triplets:
        print(t[0])
        print(t[1])
        print(t[2])


def main() -> None:
    report([-1, 0, 1, 2, -1, -4])                       # 2 / -1 -1 2 / -1 0 1
    report([0, 1, 1])                                    # 0
    report([0, 0, 0])                                    # 1 / 0 0 0
    report([0, 0, 0, 0, 0, 0])                           # 1 / 0 0 0
    report([-2, 0, 1, 1, 2, -1, -1])                     # 3
    report([-4, -2, -1, 0, 1, 2, 3, 4, 5])               # 8
    report([1, -1])                                      # 0
    report([1, 2, 3, 4, 5])                              # 0
    report([-3, -1, -1, 0, 1, 2, 2, 3, 4, -2])           # several


if __name__ == "__main__":
    main()
