"""LeetCode 303 - Range Sum Query, Immutable.

Mirror of range_sum_query.kara: the same prefix array carrying an explicit
leading zero, so that sum_range(l, r) is one subtraction with no special case
at l == 0.
"""


class NumArray:
    """prefix[i] is the total of the first i elements; prefix[0] == 0."""

    def __init__(self, nums: list[int]) -> None:
        prefix = [0]
        for i, v in enumerate(nums):
            prefix.append(prefix[i] + v)
        self.prefix = prefix

    def sum_range(self, left: int, right: int) -> int:
        return self.prefix[right + 1] - self.prefix[left]


def report(nums: list[int], queries: list[int]) -> None:
    na = NumArray(nums)
    body = ", ".join(str(v) for v in nums)
    parts = []
    for q in range(0, len(queries) - 1, 2):
        left, right = queries[q], queries[q + 1]
        parts.append(f"[{left},{right}]={na.sum_range(left, right)}")
    print(f"[{body}] -> " + " ".join(parts))


def main() -> None:
    report([-2, 0, 3, -5, 2, -1], [0, 2, 2, 5, 0, 5, 1, 1])
    report([1, 2, 3, 4, 5], [0, 4, 0, 0, 4, 4, 1, 3])
    report([7], [0, 0])
    report([0, 0, 0, 0], [0, 3, 1, 2])
    report([-1, -2, -3], [0, 2, 1, 2, 2, 2])
    report([100000, -100000, 100000], [0, 2, 0, 1, 1, 2])


if __name__ == "__main__":
    main()
