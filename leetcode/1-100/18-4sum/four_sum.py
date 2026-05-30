"""LeetCode #18: 4Sum — sort + two nested fixes + two-pointer, O(n^3).

Mirror of four_sum.kara: same sort-then-two-pointer shape, same four-level
duplicate suppression (two backward-look outer skips + inner skip-runs),
same min/max-sum pruning, and same output format (quadruplet count, then
each quadruplet's four sorted values one per line) so the two files diff
line-for-line across all nine cases.
"""


def four_sum(nums: list[int], target: int) -> list[list[int]]:
    s = sorted(nums)
    n = len(s)
    result: list[list[int]] = []
    a = 0
    while a < n - 3:
        if a > 0 and s[a] == s[a - 1]:
            a += 1
            continue
        # Smallest quadruplet starting at `a` already overshoots ⇒ done.
        if s[a] + s[a + 1] + s[a + 2] + s[a + 3] > target:
            break
        # Largest quadruplet starting at `a` still undershoots ⇒ skip `a`.
        if s[a] + s[n - 1] + s[n - 2] + s[n - 3] < target:
            a += 1
            continue
        b = a + 1
        while b < n - 2:
            if b > a + 1 and s[b] == s[b - 1]:
                b += 1
                continue
            if s[a] + s[b] + s[b + 1] + s[b + 2] > target:
                break
            if s[a] + s[b] + s[n - 1] + s[n - 2] < target:
                b += 1
                continue
            lo, hi = b + 1, n - 1
            while lo < hi:
                total = s[a] + s[b] + s[lo] + s[hi]
                if total < target:
                    lo += 1
                elif total > target:
                    hi -= 1
                else:
                    result.append([s[a], s[b], s[lo], s[hi]])
                    lo += 1
                    hi -= 1
                    while lo < hi and s[lo] == s[lo - 1]:
                        lo += 1
                    while lo < hi and s[hi] == s[hi + 1]:
                        hi -= 1
            b += 1
        a += 1
    return result


def report(nums: list[int], target: int) -> None:
    quads = four_sum(nums, target)
    print(len(quads))
    for q in quads:
        print(q[0])
        print(q[1])
        print(q[2])
        print(q[3])


def main() -> None:
    report([1, 0, -1, 0, -2, 2], 0)                     # 3
    report([2, 2, 2, 2, 2], 8)                           # 1 / 2 2 2 2
    report([0, 0, 0, 0], 0)                              # 1 / 0 0 0 0
    report([1, 2, 3, 4], 10)                             # 1 / 1 2 3 4
    report([1, 2, 3, 4], 100)                            # 0
    report([-3, -2, -1, 0, 1, 2, 3], 0)                  # several
    report([1, 1, 1, 1, 1, 1], 4)                        # 1 / 1 1 1 1
    report([1, 2, 3], 6)                                 # 0
    report([-2, -1, -1, 1, 1, 2], 0)                     # several, dedup-heavy


if __name__ == "__main__":
    main()
