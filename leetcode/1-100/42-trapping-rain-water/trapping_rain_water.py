"""LeetCode #42: Trapping Rain Water — known-correct reference oracle.

Given non-negative bar heights of unit width, return the total water trapped after rain. The
water over column i is min(left_max[i], right_max[i]) - height[i]: a column holds water up to
the shorter of the tallest wall to its left and the tallest to its right.

Three styles, all returning the IDENTICAL answer for every case (cross-checked below), each
mirroring one Kāra pedagogical file:

  - Style 1 (converging two pointers, O(1) space, ★) — mirror of trapping_rain_water.kara
  - Style 2 (prefix/suffix maxima arrays, O(n) space) — mirror of trapping_rain_water_arrays.kara
  - Style 3 (monotonic stack, horizontal slabs)        — mirror of trapping_rain_water_stack.kara

The output is the bare answer per case, line-for-line diffable against each Kāra mirror's
stdout under both `karac run` and `karac build`.
"""

from __future__ import annotations


# --- Style 1: converging two pointers (mirrors trapping_rain_water.kara, ★) ---------------
#
# Advance the pointer on the shorter outer wall: that side's running max is the binding
# constraint (every bar past the taller side is provably ≥ it), so the column settles with
# one scalar and no far-side lookahead. O(1) space.

def trap_two_pointer(height: list[int]) -> int:
    n = len(height)
    left, right = 0, n - 1
    left_max = right_max = 0
    water = 0
    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                water += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                water += right_max - height[right]
            right -= 1
    return water


# --- Style 2: prefix/suffix maxima arrays (mirrors trapping_rain_water_arrays.kara) -------
#
# Materialize left_max[i] (tallest in 0..=i) and right_max[i] (tallest in i..n), then sum
# min(left_max, right_max) - height over every column. O(n) space; makes the formula literal.

def trap_arrays(height: list[int]) -> int:
    n = len(height)
    if n == 0:
        return 0
    left_max = [0] * n
    right_max = [0] * n
    left_max[0] = height[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i - 1], height[i])
    right_max[n - 1] = height[n - 1]
    for j in range(n - 2, -1, -1):
        right_max[j] = max(right_max[j + 1], height[j])
    return sum(min(left_max[k], right_max[k]) - height[k] for k in range(n))


# --- Style 3: monotonic stack (mirrors trapping_rain_water_stack.kara) --------------------
#
# Stack of indices with non-increasing heights; when a taller bar arrives, pop the floor and
# add the rectangular slab bounded by the new top (left wall) and the incoming bar (right
# wall). Each bar pushed/popped once ⇒ O(n) time, O(n) space.

def trap_stack(height: list[int]) -> int:
    stack: list[int] = []
    water = 0
    for i, h in enumerate(height):
        while stack and h > height[stack[-1]]:
            floor = stack.pop()
            if not stack:
                break
            left = stack[-1]
            width = i - left - 1
            depth = min(h, height[left]) - height[floor]
            water += width * depth
        stack.append(i)
    return water


def report(height: list[int]) -> None:
    a = trap_two_pointer(height)
    b = trap_arrays(height)
    c = trap_stack(height)
    assert a == b == c, (height, a, b, c)
    print(a)


def main() -> None:
    report([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1])
    report([4, 2, 0, 3, 2, 5])
    report([5])
    report([2, 0, 2])
    report([3, 0, 0, 2, 0, 4])
    report([1, 2, 3, 4, 5])
    report([5, 4, 3, 2, 1])
    report([5, 2, 1, 2, 1, 5])


if __name__ == "__main__":
    main()
