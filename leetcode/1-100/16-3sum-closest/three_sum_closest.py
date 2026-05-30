"""LeetCode #16: 3Sum Closest — sort + two-pointer, O(n^2).

Mirror of three_sum_closest.kara: same sort + two-pointer shape, same `best`
seeding (smallest-three sum), same exact-hit return, same first-seen tie
behavior, and same output format (one integer — the closest sum — per case)
so diff <(./bin) <(python3 …) matches line-for-line across all nine cases.
"""


def three_sum_closest(nums: list[int], target: int) -> int:
    s = sorted(nums)
    n = len(s)
    best = s[0] + s[1] + s[2]
    i = 0
    while i < n - 2:
        lo, hi = i + 1, n - 1
        while lo < hi:
            total = s[i] + s[lo] + s[hi]
            if total == target:
                return total
            if abs(total - target) < abs(best - target):
                best = total
            if total < target:
                lo += 1
            else:
                hi -= 1
        i += 1
    return best


def report(nums: list[int], target: int) -> None:
    print(three_sum_closest(nums, target))


def main() -> None:
    report([-1, 2, 1, -4], 1)                              # 2
    report([0, 0, 0], 0)                                   # 0
    report([1, 1, 1, 0], -100)                             # 2
    report([1, 2, 3], 6)                                   # 6
    report([-1, -2, -3], 0)                                # -6
    report([-3, -2, -1, 0, 1, 2, 3], 4)                    # 4
    report([5, 5, 5], 100)                                 # 15
    report([-100, -50, 1, 2, 3], -150)                     # -149
    report([-1, -1, 1, 1], 0)                              # -1


if __name__ == "__main__":
    main()
